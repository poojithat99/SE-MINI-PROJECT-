"""Dependency-light regression tests for backend lifecycle edge cases.

The functions under test are compiled from their real source definitions with
external services mocked. These checks are intentionally not full API tests;
they run even where optional AI and authentication packages are unavailable.
"""

import ast
import asyncio
import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import Mock


ROOT = Path(__file__).resolve().parents[1]


def load_function(relative_path, function_name, namespace):
    """Execute a real function body with framework/IO dependencies injected."""
    source = ROOT / relative_path
    tree = ast.parse(source.read_text(encoding="utf-8"))
    node = next(
        child for child in tree.body
        if isinstance(child, (ast.FunctionDef, ast.AsyncFunctionDef))
        and child.name == function_name
    )
    node.decorator_list = []
    module = ast.Module(body=[node], type_ignores=[])
    ast.fix_missing_locations(module)
    exec(compile(module, str(source), "exec"), namespace)
    return namespace[function_name]


class FakeUpload:
    filename = "document.txt"

    async def read(self, size):
        return b"A real document with text."

    async def close(self):
        pass


class FakeDatabase:
    """Represents a committed row that rollback cannot remove."""

    def __init__(self):
        self.rows = []
        self.current = None

    def add(self, document):
        self.current = document

    def commit(self):
        if self.current is not None and self.current not in self.rows:
            self.current.id = 42
            self.rows.append(self.current)
        self.current = None

    def refresh(self, document):
        pass

    def rollback(self):
        self.current = None

    def get(self, model, document_id):
        return next((row for row in self.rows if row.id == document_id), None)

    def delete(self, document):
        self.rows.remove(document)


class TestUploadFailureCompensation(unittest.TestCase):
    def setup_handler(self, service_upload, record_audit):
        db = FakeDatabase()
        cleanup = Mock()
        cleanup_service = Mock()
        namespace = {
            "UploadFile": FakeUpload,
            "Session": FakeDatabase,
            "File": lambda *args, **kwargs: None,
            "Form": lambda *args, **kwargs: None,
            "Depends": lambda dependency: None,
            "get_current_user": lambda: None,
            "get_db": lambda: None,
            "Path": Path,
            "MAX_FILE_SIZE": 10 * 1024 * 1024,
            "account_identity_id": lambda account: account["id"],
            "document_owner": lambda db, account: SimpleNamespace(id=1),
            "Document": SimpleNamespace,
            "save_file": lambda content, name: "stored-test.txt",
            "delete_file": cleanup,
            "service_upload_document": service_upload,
            "process_document": Mock(),
            "record_audit_event": record_audit,
            "delete_user_document": cleanup_service,
            "logger": Mock(),
            "document_json": lambda doc: {"id": doc.id},
            "add_service_metadata": lambda data, account, service: data,
        }
        handler = load_function("src/api/documents.py", "upload_document", namespace)
        return handler, db, cleanup, cleanup_service

    def test_secondary_upload_failure_removes_committed_primary_row(self):
        def broken_service(**kwargs):
            raise ValueError("secondary upload failed")

        handler, db, delete_file, delete_service = self.setup_handler(
            broken_service, Mock()
        )
        with self.assertRaisesRegex(ValueError, "secondary upload failed"):
            asyncio.run(handler(FakeUpload(), None, None, {"id": 7}, db))
        self.assertEqual(db.rows, [])
        delete_file.assert_called_once_with("stored-test.txt")
        delete_service.assert_not_called()

    def test_later_failure_cleans_both_records_using_correct_vector_id(self):
        handler, db, delete_file, delete_service = self.setup_handler(
            Mock(return_value={"id": 99}),
            Mock(side_effect=RuntimeError("audit unavailable")),
        )
        with self.assertRaisesRegex(RuntimeError, "audit unavailable"):
            asyncio.run(handler(FakeUpload(), None, None, {"id": 7}, db))
        self.assertEqual(db.rows, [])
        delete_service.assert_called_once_with(7, 99, index_document_id=42)
        delete_file.assert_called_once_with("stored-test.txt")


class TestTextDocumentCategory(unittest.TestCase):
    def setup_handler(self):
        edit = Mock()
        upload = Mock(return_value={"id": 15})
        process = Mock()
        namespace = {
            "TextDocumentInput": object,
            "Depends": lambda dependency: None,
            "get_current_user": lambda: None,
            "HTTPException": type("HTTPException", (Exception,), {
                "__init__": lambda self, status_code, detail: (
                    setattr(self, "status_code", status_code),
                    setattr(self, "detail", detail),
                    Exception.__init__(self, detail),
                )[-1]
            }),
            "resolve_owner": lambda account: {"id": 7, "username": "qa"},
            "upload_document": upload,
            "edit_user_document": edit,
            "process_document": process,
            "get_user_document": lambda owner, doc_id: {
                "id": doc_id, "title": "Note", "extracted_text": "Hello"
            },
            "record_audit_event": Mock(),
        }
        handler = load_function(
            "src/api/text_documents.py", "create_text_document", namespace
        )
        return handler, upload, edit, process

    def test_selected_category_is_saved_before_ai_processing(self):
        handler, upload, edit, process = self.setup_handler()
        result = handler(
            SimpleNamespace(title="Note", content="Hello", category=" Education "),
            {"id": 7},
        )
        edit.assert_called_once_with(7, 15, {"category": "Education"})
        process.assert_called_once_with(15, 7)
        self.assertEqual(result["title"], "Note")

    def test_omitted_category_keeps_auto_classification(self):
        handler, upload, edit, process = self.setup_handler()
        handler(SimpleNamespace(title="Note", content="Hello", category=None), {"id": 7})
        edit.assert_not_called()
        process.assert_called_once_with(15, 7)

    def test_overlong_category_is_rejected_before_creating_a_document(self):
        handler, upload, edit, process = self.setup_handler()
        with self.assertRaises(Exception) as caught:
            handler(SimpleNamespace(title="Note", content="Hello", category="x" * 101), {"id": 7})
        self.assertEqual(caught.exception.status_code, 400)
        upload.assert_not_called()
        edit.assert_not_called()


class TestServiceVectorCleanup(unittest.TestCase):
    def test_service_deletion_supports_public_vector_id(self):
        with tempfile.TemporaryDirectory() as directory:
            stored = Path(directory) / "note.txt"
            stored.write_text("Note", encoding="utf-8")
            delete_index = Mock()
            delete_record = Mock(return_value={"id": 99})
            handler = load_function(
                "src/services/document_service.py", "delete_user_document",
                {
                    "get_document": lambda doc_id, owner_id: {
                        "storage_path": str(stored)
                    },
                    "delete_document_index": delete_index,
                    "delete_document": delete_record,
                    "Path": Path,
                },
            )
            handler(7, 99, index_document_id=42)
            delete_index.assert_called_once_with(42, 7)
            delete_record.assert_called_once_with(99, 7)
            self.assertFalse(stored.exists())


if __name__ == "__main__":
    unittest.main()

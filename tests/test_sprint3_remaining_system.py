"""Sprint 3 end-to-end and storage regression evidence on disposable CI data.

An explicitly expected-failing deletion test records a known unmet STP contract;
it does NOT count as a passing acceptance test.
"""
import os
import re
import uuid
import unittest
from io import BytesIO
from pathlib import Path

os.environ.setdefault("JWT_SECRET_KEY", "ci-only-test-secret-not-for-deployment")

from fastapi.testclient import TestClient
from jose import jwt
from pypdf import PdfWriter
from src.main import app
from src.services.document_service import list_user_documents, get_user_document, delete_user_document
from backend.app.storage.file_storage import save_file, get_file, delete_file


class Sprint3AdditionalSystemChecks(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.context = TestClient(app)
        cls.client = cls.context.__enter__()

    @classmethod
    def tearDownClass(cls):
        cls.context.__exit__(None, None, None)

    def user(self):
        username = "stp_" + uuid.uuid4().hex[:12]
        password = "ExampleSecure123"
        reg = self.client.post("/api/auth/register", json={
            "username": username, "email": username + "@example.org", "password": password
        })
        self.assertEqual(reg.status_code, 201, reg.text)
        login = self.client.post("/api/auth/login", json={
            "username": username, "password": password
        })
        self.assertEqual(login.status_code, 200, login.text)
        token = login.json()["access_token"]
        owner = int(jwt.get_unverified_claims(token)["sub"])
        return {"Authorization": "Bearer " + token}, owner

    def post_file(self, headers, filename, contents, title):
        return self.client.post("/api/documents", headers=headers,
            data={"title": title},
            files={"file": (filename, contents, "application/octet-stream")})

    def test_stored_file_has_generated_name_and_safe_root(self):
        original = "..\\..\\static\\poojitha_test.txt"
        stored = save_file(b"Sprint 3 safe storage fixture", original)
        try:
            relative = Path(stored)
            resolved = get_file(stored)
            self.assertFalse(relative.is_absolute())
            self.assertEqual(relative.parts[0], "storage")
            self.assertRegex(resolved.name, r"^[0-9a-fA-F-]{36}\\.txt$")
            self.assertNotIn("static", str(resolved))
            self.assertEqual(resolved.read_bytes(), b"Sprint 3 safe storage fixture")
            with self.assertRaises(ValueError):
                get_file("../outside.txt")
        finally:
            delete_file(stored)

    def test_renamed_executable_is_rejected_by_signature(self):
        with self.assertRaises(ValueError):
            save_file(b"MZ\\x00\\x00a fake executable", "../../renamed.pdf")

    def test_keyword_search_is_case_insensitive_and_requires_all_terms(self):
        headers, _ = self.user()
        doc = self.post_file(headers, "stp_neural.txt",
             b"Neural networks identify patterns in machine learning data.",
             "Sprint3 Neural Search")
        self.assertEqual(doc.status_code, 201, doc.text)
        doc_id = doc.json()["id"]
        try:
            valid = self.client.get("/api/search/keyword",
                headers=headers, params={"q": "nEuRaL nEtWoRkS"})
            self.assertEqual(valid.status_code, 200, valid.text)
            self.assertIn(doc_id, [item["id"] for item in valid.json()["items"]])
            missed = self.client.get("/api/search/keyword",
                headers=headers, params={"q": "neural unbelievablyabsent"})
            self.assertEqual(missed.status_code, 200, missed.text)
            self.assertEqual(missed.json()["total"], 0)
        finally:
            self.client.delete(f"/api/documents/{doc_id}", headers=headers)

    def test_pdf_corrupt_encrypted_and_image_only_end_failed_with_reason(self):
        headers, owner = self.user()
        cases = [("corrupt", b"%PDF-1.4\\nBROKEN")]
        out = BytesIO()
        writer = PdfWriter()
        writer.add_blank_page(width=100, height=100)
        writer.write(out)
        cases.append(("image_only", out.getvalue()))
        out = BytesIO()
        writer = PdfWriter()
        writer.add_blank_page(width=100, height=100)
        writer.encrypt("test-only-password")
        writer.write(out)
        cases.append(("encrypted", out.getvalue()))
        for label, data in cases:
            with self.subTest(label=label):
                name = "qa3_" + label + ".pdf"
                title = "Sprint3 Broken " + label
                resp = self.post_file(headers, name, data, title)
                self.assertEqual(resp.status_code, 201, resp.text)
                doc_id = resp.json()["id"]
                try:
                    self.assertEqual(resp.json().get("processing_status"), "Failed")
                    entries = list_user_documents(owner, limit=100)["items"]
                    matching = [d for d in entries if d["original_filename"] == name and d["title"] == title]
                    self.assertEqual(len(matching), 1)
                    detail = get_user_document(owner, matching[0]["id"])
                    self.assertEqual(detail["processing_status"], "Failed")
                    self.assertTrue(detail.get("processing_error"), detail)
                    self.assertEqual(self.client.get("/health").status_code, 200)
                finally:
                    self.client.delete(f"/api/documents/{doc_id}", headers=headers)

    def test_failed_pdf_does_not_break_following_api_calls(self):
        headers, _ = self.user()
        bad = self.post_file(headers, "corrupted.pdf", b"%PDF-1.4\\nDAMAGED",
                             "Sprint3 corrupt resilience")
        self.assertEqual(bad.status_code, 201, bad.text)
        self.assertEqual(bad.json().get("processing_status"), "Failed")
        self.assertEqual(self.client.get("/health").status_code, 200)
        self.assertEqual(self.client.get("/api/documents", headers=headers).status_code, 200)
        self.client.delete("/api/documents/" + str(bad.json()["id"]), headers=headers)

    @unittest.expectedFailure
    def test_public_delete_removes_secondary_service_record(self):
        """EXPECTED FAILURE — documents route only removes primary row/file (known cleanup gap)."""
        headers, owner = self.user()
        doc = self.post_file(headers, "cleanup_regression.txt",
             b"Document lifecycle indexing and complete deletion consistency.",
             "Sprint3 deletion integrity")
        self.assertEqual(doc.status_code, 201, doc.text)
        public_id = doc.json()["id"]
        service_id = None
        try:
            docs = list_user_documents(owner, limit=100)["items"]
            matches = [d for d in docs if d["original_filename"] == "cleanup_regression.txt"
                       and d["title"] == "Sprint3 deletion integrity"]
            self.assertEqual(len(matches), 1)
            service_id = matches[0]["id"]
            result = self.client.delete(f"/api/documents/{public_id}", headers=headers)
            self.assertEqual(result.status_code, 204, result.text)
            after = list_user_documents(owner, limit=100)["items"]
            self.assertNotIn(service_id, [d["id"] for d in after],
                             "Secondary database record remains after public deletion")
        finally:
            if service_id is not None:
                try:
                    delete_user_document(owner, service_id, index_document_id=public_id)
                except FileNotFoundError:
                    pass

    @unittest.expectedFailure
    def test_public_document_default_page_size_matches_stp_ten(self):
        """EXPECTED FAILURE — source defaults to 20 whereas STP TC-Doc-07 requires 10."""
        headers, _ = self.user()
        resp = self.client.get("/api/documents", headers=headers)
        self.assertEqual(resp.status_code, 200, resp.text)
        self.assertEqual(resp.json().get("limit"), 10)


if __name__ == "__main__":
    unittest.main(verbosity=2)

"""Regression tests for resource-light Render startup on small instances."""
import subprocess
import sys
import unittest
from unittest.mock import Mock, patch

from src.services import vector_store_service


class TestLazyAIStartup(unittest.TestCase):
    def test_importing_fastapi_app_does_not_import_torch_or_chromadb(self):
        # Use a fresh Python process: previous tests may have loaded the
        # model/index and populated sys.modules in this runner already.
        command = [
            sys.executable,
            "-c",
            (
                "import sys; from src.main import app; "
                "assert 'torch' not in sys.modules, 'Torch imported at startup'; "
                "assert 'chromadb' not in sys.modules, 'Chroma imported at startup'; "
                "assert app.title == 'AI-CMS API'"
            ),
        ]
        result = subprocess.run(
            command, capture_output=True, text=True, timeout=45, check=False
        )
        self.assertEqual(
            result.returncode, 0, result.stderr or result.stdout
        )

    def test_vector_collection_initializes_on_first_actual_use(self):
        mock_collection = Mock()
        with patch.object(
            vector_store_service, "_get_collection", return_value=mock_collection
        ) as loader:
            vector_store_service.delete_document_index(42, 7)

        loader.assert_called_once()
        mock_collection.delete.assert_called_once_with(
            where={
                "$and": [
                    {"owner_id": "7"},
                    {"document_id": "42"},
                ]
            }
        )


if __name__ == "__main__":
    unittest.main()

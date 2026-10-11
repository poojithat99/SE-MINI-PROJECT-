
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


class TestRepositoryStructure(unittest.TestCase):

    def test_readme_exists(self):
        self.assertTrue((ROOT / "README.md").is_file())

    def test_three_project_documents_exist(self):
        documents = list(ROOT.glob("*.docx"))
        self.assertGreaterEqual(
            len(documents),
            3,
            "Expected SRS, SAD, and STP Word documents."
        )


if __name__ == "__main__":
    unittest.main()

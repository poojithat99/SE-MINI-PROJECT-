"""Checks for explicit production CORS configuration."""
import os
import unittest
from unittest.mock import patch

from src.cors import LOCAL_ORIGINS, get_allowed_origins


class TestCORSConfiguration(unittest.TestCase):
    def test_local_frontend_origins_remain_allowed(self):
        self.assertEqual(get_allowed_origins(""), list(LOCAL_ORIGINS))

    def test_production_frontend_origin_is_added(self):
        result = get_allowed_origins("https://ai-cms-frontend.onrender.com/")
        self.assertIn("https://ai-cms-frontend.onrender.com", result)
        self.assertIn("http://localhost:5173", result)

    def test_duplicate_and_multiple_origins(self):
        result = get_allowed_origins(
            " https://app.example.org, https://app.example.org/,"
            "https://preview.example.org "
        )
        self.assertEqual(result.count("https://app.example.org"), 1)
        self.assertIn("https://preview.example.org", result)

    def test_environment_variable_used_when_argument_not_passed(self):
        with patch.dict(os.environ, {
            "AI_CMS_CORS_ORIGINS": "https://example.org"
        }):
            self.assertIn("https://example.org", get_allowed_origins())

    def test_rejects_wildcards_paths_and_invalid_schemes(self):
        invalid = [
            "*", "https://*.example.org", "ftp://example.org",
            "https://example.org/api", "https://example.org?x=1",
            "https://name:password@example.org", "https://example.org:bad",
        ]
        for value in invalid:
            with self.subTest(origin=value):
                with self.assertRaises(ValueError):
                    get_allowed_origins(value)


if __name__ == "__main__":
    unittest.main()

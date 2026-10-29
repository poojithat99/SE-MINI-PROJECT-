"""Regression tests for login identifier and JWT configuration."""
import os
import unittest
from types import SimpleNamespace
from unittest.mock import patch

from src.services import auth_service
from src.api.auth import LoginRequest, login
from fastapi import HTTPException


class TestLoginRegressions(unittest.TestCase):
    def setUp(self):
        self.user = SimpleNamespace(
            id=17,
            username="registered_username",
            email="person@example.com",
            password_hash="mocked-hash",
            role="User",
            is_active=True,
        )

    def test_username_login_still_works(self):
        with patch.dict(os.environ, {"JWT_SECRET_KEY": "test-only-jwt-secret"}), \
             patch.object(auth_service, "find_user_by_username", return_value=self.user) as lookup, \
             patch.object(auth_service, "find_user_by_email") as email_lookup, \
             patch.object(auth_service.bcrypt, "checkpw", return_value=True):
            result = auth_service.login_user("registered_username", "SecurePass123")
            self.assertTrue(result["access_token"])
            lookup.assert_called_once_with("registered_username")
            email_lookup.assert_not_called()

    def test_email_login_falls_back_to_email_lookup(self):
        with patch.dict(os.environ, {"JWT_SECRET_KEY": "test-only-jwt-secret"}), \
             patch.object(auth_service, "find_user_by_username", return_value=None), \
             patch.object(auth_service, "find_user_by_email", return_value=self.user) as email_lookup, \
             patch.object(auth_service.bcrypt, "checkpw", return_value=True):
            result = auth_service.login_user("PERSON@EXAMPLE.COM", "SecurePass123")
            self.assertTrue(result["access_token"])
            email_lookup.assert_called_once_with("person@example.com")

    def test_missing_secret_does_not_issue_token(self):
        with patch.dict(os.environ, {"JWT_SECRET_KEY": ""}), \
             patch.object(auth_service, "find_user_by_username", return_value=self.user), \
             patch.object(auth_service.bcrypt, "checkpw", return_value=True):
            with self.assertRaises(auth_service.AuthenticationConfigurationError):
                auth_service.login_user("registered_username", "SecurePass123")

    def test_api_returns_actionable_503_without_secret(self):
        with patch("src.api.auth.login_user", side_effect=auth_service.AuthenticationConfigurationError("missing")):
            with self.assertRaises(HTTPException) as ctx:
                login(LoginRequest(username="registered_username", password="SecurePass123"))
            self.assertEqual(ctx.exception.status_code, 503)
            self.assertIn("JWT_SECRET_KEY", ctx.exception.detail)


if __name__ == "__main__":
    unittest.main()

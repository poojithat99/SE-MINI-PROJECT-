"""Sprint 3 security and validation integration regressions (disposable CI accounts)."""
import os
import uuid
import unittest
from datetime import datetime, timedelta, timezone

os.environ.setdefault("JWT_SECRET_KEY", "test-only-sprint3-qa-key")

from fastapi.testclient import TestClient
from jose import jwt
from src.main import app


class Sprint3SecurityAPI(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.context = TestClient(app)
        cls.client = cls.context.__enter__()

    @classmethod
    def tearDownClass(cls):
        cls.context.__exit__(None, None, None)

    def register_and_login(self):
        username = "qa3_" + uuid.uuid4().hex[:10]
        password = "ExamplePass123"
        registration = self.client.post("/api/auth/register", json={
            "username": username, "email": username + "@example.com", "password": password,
        })
        self.assertEqual(registration.status_code, 201, registration.text)
        response = self.client.post("/api/auth/login", json={
            "username": username, "password": password,
        })
        self.assertEqual(response.status_code, 200, response.text)
        token = response.json()["access_token"]
        return {"Authorization": "Bearer " + token}, token

    def test_expired_and_tampered_tokens_rejected(self):
        headers, token = self.register_and_login()
        claims = jwt.get_unverified_claims(token)
        claims["exp"] = int((datetime.now(timezone.utc) - timedelta(minutes=35)).timestamp())
        expired = jwt.encode(claims, os.environ["JWT_SECRET_KEY"], algorithm="HS256")
        for bad_token in (expired, token + "invalid"):
            response = self.client.get("/api/documents", headers={
                "Authorization": "Bearer " + bad_token,
            })
            self.assertEqual(response.status_code, 401, response.text)
        self.assertEqual(self.client.get("/api/documents", headers=headers).status_code, 200)

    def test_standard_user_denied_all_admin_routes(self):
        headers, _ = self.register_and_login()
        routes = [
            ("GET", "/api/admin/categories", None),
            ("POST", "/api/admin/categories", {"name": "Denied", "description": "Must not save"}),
            ("DELETE", "/api/admin/categories/1", None),
            ("GET", "/api/admin/audit-logs", None),
        ]
        for method, path, body in routes:
            with self.subTest(method=method, path=path):
                response = self.client.request(method, path, headers=headers, json=body)
                self.assertEqual(response.status_code, 403, response.text)

    def test_authenticated_pagination_and_semantic_input_bounds(self):
        headers, _ = self.register_and_login()
        cases = [
            ("/api/documents?page=0", 400),
            ("/api/documents?limit=0", 400),
            ("/api/documents?limit=101", 400),
            ("/api/search/semantic?q=ab", 422),
            ("/api/search/semantic?q=" + "x" * 301, 422),
            ("/api/search/semantic?q=testquery&date_from=2026-12-01&date_to=2026-01-01", 400),
        ]
        for path, expected in cases:
            with self.subTest(path=path[:80]):
                response = self.client.get(path, headers=headers)
                self.assertEqual(response.status_code, expected, response.text)

    def test_unsupported_oversized_empty_and_spoofed_uploads_rejected(self):
        headers, _ = self.register_and_login()
        cases = [
            ("empty.pdf", b"", 400),
            ("malware.exe", b"hello", 400),
            ("image.png", b"\\x89PNG\\r\\n\\x1a\\n", 400),
            ("test.zip", b"PK\\x03\\x04junk", 400),
            ("spoofed.pdf", b"MZnotapdf", 400),
            ("notdoc.docx", b"not a word zip", 400),
            ("oversize.txt", b"Q" * (10 * 1024 * 1024 + 1), 413),
        ]
        for name, payload, expected in cases:
            with self.subTest(filename=name):
                response = self.client.post("/api/documents", headers=headers, files={
                    "file": (name, payload, "application/octet-stream"),
                })
                self.assertEqual(response.status_code, expected, response.text)

    def test_cross_user_document_actions_are_denied(self):
        owner_headers, _ = self.register_and_login()
        other_headers, _ = self.register_and_login()
        content = b"Sprint 3 document access-control test and artificial intelligence retrieval."
        uploaded = self.client.post("/api/documents", headers=owner_headers,
            files={"file": ("qa3crossuser.txt", content, "text/plain")},
            data={"title": "Sprint3 cross-user evidence"})
        self.assertEqual(uploaded.status_code, 201, uploaded.text)
        document_id = uploaded.json()["id"]
        try:
            routes = [
                ("GET", f"/api/documents/{document_id}", None),
                ("GET", f"/api/documents/{document_id}/download", None),
                ("PATCH", f"/api/documents/{document_id}", {"title": "Unauthorized edit"}),
                ("POST", f"/api/documents/{document_id}/reprocess", None),
                ("DELETE", f"/api/documents/{document_id}", None),
            ]
            for method, path, body in routes:
                with self.subTest(method=method, path=path):
                    response = self.client.request(method, path, headers=other_headers, json=body)
                    self.assertEqual(response.status_code, 404, response.text)
            self.assertEqual(self.client.get(
                f"/api/documents/{document_id}", headers=owner_headers).status_code, 200)
        finally:
            self.client.delete(f"/api/documents/{document_id}", headers=owner_headers)


if __name__ == "__main__":
    unittest.main(verbosity=2)

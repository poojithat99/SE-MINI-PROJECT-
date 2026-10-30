"""Validate allowed CORS origins for local and deployed AI-CMS frontend."""
import os
from urllib.parse import urlsplit

LOCAL_ORIGINS = (
    "http://localhost:5173",
    "http://127.0.0.1:5173",
)


def get_allowed_origins(configured=None):
    """Include the two local dev origins plus explicit production origins.

    Configure AI_CMS_CORS_ORIGINS as a comma-separated list of full
    http(s) origins, e.g. https://app.example.com. Never use wildcard.
    """
    if configured is None:
        configured = os.getenv("AI_CMS_CORS_ORIGINS", "")

    origins = list(LOCAL_ORIGINS)
    for raw in configured.split(","):
        origin = raw.strip().rstrip("/")
        if not origin:
            continue
        parsed = urlsplit(origin)
        if (
            parsed.scheme not in ("http", "https")
            or not parsed.hostname
            or parsed.username is not None
            or parsed.password is not None
            or parsed.path
            or parsed.query
            or parsed.fragment
            or "*" in origin
        ):
            raise ValueError(
                "AI_CMS_CORS_ORIGINS must contain full http(s) origins "
                "without paths, wildcards, or credentials"
            )
        try:
            parsed.port
        except ValueError as exc:
            raise ValueError("Invalid port in AI_CMS_CORS_ORIGINS") from exc
        if origin not in origins:
            origins.append(origin)
    return origins

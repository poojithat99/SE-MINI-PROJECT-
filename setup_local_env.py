"""Create a strong JWT_SECRET_KEY in the project's local .env (never commit it).

Run from the project root: python scripts/setup_local_env.py
The script preserves existing .env settings and existing JWT secrets.
Production deployments must set JWT_SECRET_KEY in the hosting platform.
"""
from __future__ import annotations

import os
import secrets
from pathlib import Path


def ensure_local_secret(env_file: Path) -> str:
    if env_file.exists():
        lines = env_file.read_text(encoding="utf-8-sig").splitlines()
    else:
        lines = []

    for line in lines:
        stripped = line.strip()
        if stripped.startswith("JWT_SECRET_KEY="):
            value = stripped.split("=", 1)[1].strip().strip('"').strip("'")
            if value:
                return "JWT_SECRET_KEY already exists in local .env; left unchanged."

    generated = "JWT_SECRET_KEY=" + secrets.token_urlsafe(48)
    new_lines = [line for line in lines if not line.strip().startswith("JWT_SECRET_KEY=")]
    new_lines.append(generated)
    env_file.parent.mkdir(parents=True, exist_ok=True)

    if not env_file.exists() and os.name == "posix":
        fd = os.open(str(env_file), os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
        with os.fdopen(fd, "w", encoding="utf-8") as handle:
            handle.write("\n".join(new_lines) + "\n")
    else:
        env_file.write_text("\n".join(new_lines) + "\n", encoding="utf-8")

    return "Generated a JWT_SECRET_KEY in the local .env file. Keep it private."


if __name__ == "__main__":
    project_root = Path(__file__).resolve().parents[1]
    print(ensure_local_secret(project_root / ".env"))

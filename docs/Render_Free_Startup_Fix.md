# Render free-instance backend startup recovery

**Observed on 30 October 2026:** Render reported **Build successful**, then retried
`uvicorn src.main:app --host 0.0.0.0 --port $PORT` repeatedly and finally logged
`Port scan timeout reached, no open ports detected`.

The command is correct. The build logs also show Python **3.14** wheels and several gigabytes
of Nvidia/CUDA downloads for a CPU-only FastAPI service on a **512 MB RAM** free instance.

## Fix included in the repository

- `.python-version` pins **Python 3.12.10** (also ensure a manually created Render
  Web Service has `PYTHON_VERSION=3.12.10`).
- `src/services/embedding_service.py` delays importing `sentence_transformers`
  / PyTorch until an embedding is actually needed.
- `src/services/vector_store_service.py` delays Chroma's import and PersistentClient
  creation until a vector operation is needed; existing `_collection` callers stay compatible.
- `render.yaml` installs **CPU-only** Torch before other requirements.
- `tests/test_render_startup.py` checks that importing FastAPI does not import Torch or
  Chroma and that the vector store is initialized on first use.

## Required: update your manually created Render web service

Because this Web Service was created manually rather than through the Render Blueprint,
merging a change to `render.yaml` will **not** automatically update its settings.

1. Merge the startup fix after the GitHub PR tests pass.
2. Open the backend service on Render → **Environment**.
3. Set `PYTHON_VERSION` to exactly `3.12.10`; save. This must be a real runtime
   environment variable, not the output of `python --version`.
4. Open Render backend service → **Settings → Build & Deploy**.
5. Replace **Build Command** with the following one line:

   ```sh
   python -m pip install torch==2.6.0 --index-url https://download.pytorch.org/whl/cpu && python -m pip install -r requirements.txt
   ```

6. **Keep the existing Start Command unchanged**:

   ```sh
   uvicorn src.main:app --host 0.0.0.0 --port $PORT
   ```

7. Trigger a new deployment of the **merged main branch**. If automatic deploy
   is disabled, use the backend service's Manual Deploy menu, or connect the
   `RENDER_BACKEND_DEPLOY_HOOK_URL` secret and trigger the CI-gated CD workflow.
8. Confirm the deployment reached **Live** and
   `https://ACTUAL-BACKEND-ADDRESS.onrender.com/health` returns HTTP 200.
9. If startup still fails, inspect the last log entries for OOM, import errors,
   Python version, or missing storage permissions. The health check does not exercise
   model loading or vector search.

## Limits and safety

Free Render Web Services provide 512 MB RAM and ephemeral local storage. These changes
prioritize reaching a live health endpoint on low-memory hosting, but **do not
guarantee** that memory-heavy embeddings/search will fit in 512 MB.
The app's local SQLite databases, document files and vector index can be lost on
restart or redeployment without persistent storage.

Do not upgrade to paid compute or create new production secrets merely to solve
this issue. Do not share the JWT secret or private Render deploy hook URL.

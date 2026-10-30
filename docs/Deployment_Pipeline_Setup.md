# Sprint 4 — Frontend and Backend Deployment Pipeline

**Tracking:** [Sprint 4 #69](https://github.com/poojithat99/SE-MINI-PROJECT-/issues/69)  
**Environment:** Render (Python FastAPI web service + React/Vite static site)  
**Status:** Pipeline files prepared; **live hosting remains unconfigured until the Render services and GitHub secrets are set**.

## What was fixed

The original `.github/workflows/cd.yml` ran after successful CI on `main`, but failed because `RENDER_DEPLOY_HOOK_URL` was not configured. It also deployed only the backend. The updated workflow:

1. Runs **only after CI passes on a push to `main`**.
2. Handles both **backend** and **frontend** Render deploy hooks, passing Render the exact successful CI commit SHA.
3. Does **not** print deployment hook URLs.
4. If a hook is absent, records **NOT DEPLOYED** in the job summary instead of failing with a misleading error. A green workflow with missing hooks is *not evidence of a deployment*.
5. If a hook is present but Render rejects its request, the action **fails** and shows the HTTP status code.
6. A successful hook request means **deployment requested**, not necessarily that the service finished deploying. Live verification remains required.

`.github/workflows/ci.yml` now requires both backend Python tests and frontend Node tests plus a Vite production build. `render.yaml` describes both Render services with auto-deployment disabled, so Render isn't independently deploying commits that bypass these GitHub checks.

## 1. Create the two Render services

In [Render Dashboard](https://dashboard.render.com/) connect the GitHub repository `poojithat99/SE-MINI-PROJECT-`. Create a Blueprint from the repository's `render.yaml`. Review the service details and any charges before accepting.

| Backend web service | Frontend static site |
|---|---|
| Service name: `ai-cms-backend` | Service name: `ai-cms-frontend` |
| Root: repository root | Root: `frontend` |
| Python 3.12.10 | Node 22.16.0 |
| Build: `pip install -r requirements.txt` | Build: `npm ci && test -n "$VITE_API_URL" && npm run build` |
| Start: `uvicorn src.main:app --host 0.0.0.0 --port $PORT` | Publish: `dist` |
| Health: `/health` | Single-page app rewrite to `index.html` |
| Auto-deploy disabled | Auto-deploy disabled |

**Production environment variables:** Render generates `JWT_SECRET_KEY` for the backend using its Blueprint. Supply **`AI_CMS_CORS_ORIGINS`** on the backend with the exact public HTTPS frontend origin (no trailing slash), for example `https://YOUR-FRONTEND.onrender.com`. Supply **`VITE_API_URL`** on the frontend with the public HTTPS backend origin, for example `https://YOUR-BACKEND.onrender.com`.

These two values are requested during Blueprint creation (`sync: false`). If service URLs are not yet known, confirm the actual URLs after provisioning, set the variables in each service's **Environment** settings and redeploy. The frontend variable is embedded **at build time**: redeploy the static site whenever its URL value changes. Do **not** put secrets in any `VITE_` variable.

The backend keeps `http://localhost:5173` and `http://127.0.0.1:5173` for local development. Production origins are read from `AI_CMS_CORS_ORIGINS` (comma-separated, full HTTP(S) origins, no wildcard). Never use `*` as a production origin.

## 2. Add two GitHub Actions secrets

In the repository navigate to **Settings → Secrets and variables → Actions → New repository secret**. In the Render Dashboard, open **each service → Settings → Deploy Hook** and copy each unique URL. Add these *two* GitHub secrets:

| Secret | Source |
|---|---|
| `RENDER_BACKEND_DEPLOY_HOOK_URL` | Backend web-service Deploy Hook URL |
| `RENDER_FRONTEND_DEPLOY_HOOK_URL` | Frontend static-site Deploy Hook URL |

The old name `RENDER_DEPLOY_HOOK_URL` is still accepted for backend compatibility, but prefer the two explicit names. Deploy Hook URLs are sensitive; never paste them in GitHub issues, source files, screenshots or this chat.

The workflow uses GitHub's `production` environment. If that environment has protection rules requiring approval, approve the deployment when prompted; repository-level Actions secrets are supported.

## 3. Trigger a deployment after setup

After both services and their hooks are configured, a **new successful CI run on a push to `main`** triggers the CD workflow. You can rerun the latest eligible `main` CI workflow run, or create/merge a small reviewed change to `main` to get a fresh run.

Go to **Actions → CI**, ensure the backend and frontend jobs pass. Then open **Actions → CD - Deploy frontend and backend** and read the job summary:

- **NOT DEPLOYED** = hook missing; no request sent.
- **Deployment requested (HTTP 200/202)** = Render accepted the request, but deployment and health still require checking.
- **Failed (HTTP error)** = examine the hook configuration and Render service logs.

Render deployment hooks use an optional `ref` query parameter to deploy the exact commit that passed CI.

## 4. Confirm successful live deployment

Record the two URLs in [Sprint 4 #69](https://github.com/poojithat99/SE-MINI-PROJECT-/issues/69) after deployment.

- Open `https://YOUR-BACKEND.onrender.com/health` and verify HTTP 200 and `status: healthy`.
- Open `https://YOUR-FRONTEND.onrender.com` and confirm the React page loads.
- Inspect browser network requests and verify login/register sends requests to the **HTTPS backend**, not `127.0.0.1:8000`.
- Verify browser CORS preflight succeeds and `access-control-allow-origin` matches the actual frontend origin.
- Complete a real register → login → upload → search → logout journey with disposable test credentials; record evidence and defects under Sprint 3.
- Check Render service status and deployment logs after each hook request; this workflow does not wait for Render deployment to finish.

## Production limitations to resolve before calling deployment fully complete

**Persistence:** The current application uses SQLite files and local document/vector storage. A new Render instance without durable storage can lose data on redeployment or restart. Configure a supported persistent storage and database approach before using this for real documents or expecting persistent accounts. Persistent Render disks may require paid plans and may not cover every hardcoded storage location without further application changes; review the provider's billing before provisioning.

**Memory/build size:** The backend installs `sentence-transformers`, `chromadb` and related ML dependencies. Startup and model downloads may exceed smaller hosting plans. Diagnose actual Render build/startup logs before upgrading or changing packages.

**Security:** The deployment hook secrets belong only in GitHub Actions secrets; the production JWT key belongs only in Render environment settings. The locally generated `.env` and all `storage/` files are deliberately excluded from Git.

**No live URLs have been confirmed at document-preparation time.** This document is a setup and verification runbook, not a successful-deployment report.

## References

- [Render Blueprint documentation](https://render.com/docs/blueprint-spec)
- [Render deployment hooks](https://render.com/docs/deploy-hooks)
- [Render monorepo configuration](https://render.com/docs/monorepo-support)
- [GitHub Actions workflows](https://github.com/poojithat99/SE-MINI-PROJECT-/actions)

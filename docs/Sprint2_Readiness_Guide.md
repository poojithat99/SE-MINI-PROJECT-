# Sprint 2 — Test Data and Environment Readiness

**Date:** 30 October 2026 · **Part-3 final execution:** 2–6 November 2026 · **Tracking:** [Sprint 2 #65](https://github.com/poojithat99/SE-MINI-PROJECT-/issues/65)

The purpose of this sprint is to **prepare** test data and validate the setup steps. Full system, performance, security and acceptance **execution** belongs in Sprint 3. No case is marked Pass just because its fixture exists.

## 1. Generate reusable test data

From the project root in the active Python virtual environment:

```powershell
python -m pip install reportlab Pillow
python scripts/generate_part3_test_data.py
```

The generator writes only to `storage/part3_test_data/`, which is ignored by Git. It does **not** create accounts or alter the application's database.

Generated fixture counts:

| Fixture type | Count / status |
|---|---|
| Proposed evaluation documents | 20; at least 3 from each of six STP categories |
| Independent development/tuning documents | 6 |
| Out-of-category documents | 4 |
| PDF, DOCX, TXT format mix | Included |
| Semantic / keyword / no-match queries | 10 / 5 / 3 |
| Performance files | 100 TXT documents |
| Approximate 20-page processing files | 5 PDFs with 20 pages each |
| Invalid uploads | Empty, corrupt, scanned, password-protected PDFs; wrong-content DOCX; oversized TXT; double-extension and renamed-header files |
| SHA-256 file integrity manifest | `manifest.csv` |
| Independent category review register | `label_review.csv` (blank reviewer results) |
| Three-person usability record | `usability_observations.csv` (blank) |

**Important:** Proposed labels are **not independently validated**. Two team members must agree on the 24 evaluation/out-of-category labels before categorization results can be assessed. Semantic query expected matches also need review. Synthetic text helps exercise workflows but does not demonstrate real-world accuracy by itself.

The example encrypted-PDF fixture uses password `test-only-password` for testing only. Do not upload real personal documents or credentials to Git.

## 2. Verify local environment without modifying it

With the backend running, from the project root:

```powershell
.\.venv\Scripts\Activate.ps1
python scripts/check_part3_readiness.py --api-url http://127.0.0.1:8001
```

Change `8001` to your actual backend port. The report is written to `storage/part3_test_data/readiness_report.json`. It inspects package availability, presence (not value) of the JWT key, the backend `/health` response, CORS preflight for the `http://localhost:5173` frontend, default database **account counts only**, fixture counts and reviewer sign-off status.

A successful health check alone **does not mean login, document upload, search or AI processing passed**. Those journeys must be retested after the last merge and recorded separately.

## 3. Local-only test accounts

The STP requires two distinct standard users and one administrator.

- Create two standard users using the app's Register screen with unique test-only usernames/emails. Keep passwords private.
- The app initializes its administrator at startup from `AI_CMS_ADMIN_USERNAME`, `AI_CMS_ADMIN_EMAIL`, and `AI_CMS_ADMIN_PASSWORD` in the backend environment. Set all three locally in `.env` with unique test credentials; restart the backend using `--env-file .env`. Do not commit secrets.
- The administrator is initialized by `src/repositories/admin_repository.py` when the FastAPI application starts, not by creating a normal user in the frontend.
- Confirm that three account roles exist before ownership/administration testing; the readiness checker can report counts when the default `users.db` is used.

## 4. Application smoke check (must be performed on the final build)

The port-8000/JWT troubleshooting in the previous local run is a reason to **retest**, not evidence that the login check passed.

```powershell
# Backend terminal at project root
python -m uvicorn src.main:app --host 127.0.0.1 --port 8001 --env-file .env
```

```powershell
# Frontend terminal
cd frontend
$env:VITE_API_URL = 'http://127.0.0.1:8001'
npm run dev -- --port 5173 --strictPort
```

Open the browser on port 5173, then verify register → login → upload → search → logout. Record actual results in the test-case register during Sprint 3.

## 5. Known dependencies transferred to Sprint 3

- Have two independent reviewers agree proposed labels and semantic expected results.
- Arrange three usability participants and measure outcomes.
- Verify the app's final register/login/upload/search smoke test with the last commit SHA.
- Record a hosted HTTPS/TLS result when hosting exists; otherwise mark that case **Blocked**.
- Confirm or document mismatches: pagination 10 vs 20 per page, synchronous processing versus nonblocking status flow, rename/reprocess record association, and secondary database/vector deletion.
- Run actual unit tests, code coverage and branch coverage and save the four reports under `docs/`.

**Completion boundary:** Sprint 2 is preparation and documentation, not a claim that these future tests passed. It may be closed after the preparation PR is merged and remaining execution dependencies have been accepted into Sprint 3.

**Source:** AI-CMS Software Test Plan (STP) v1.0, sections 5–6, 13–14.

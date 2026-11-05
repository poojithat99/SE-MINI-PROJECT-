# Sprint 3 — STP Execution Status and Remaining Evidence

**Updated:** 5 November 2026 · **Issue:** #66 · **Formal testing window:** 2–6 November 2026

## Verified baseline

- 81 Python automated tests and 6 frontend automated tests passed in the local 1 November test runs; frontend production build succeeded.
- Statement coverage: 63.58% overall and **75.41%** for `src/services/*` (STP service target **50%**).
- Branch coverage: 47.69% overall and 57.94% for `src/services/*`.
- Core local browser/API scenarios are recorded in `System_Validation_Report.md`.
- All four required Markdown reports are merged under `docs/` on `main` (PR #73).

## Test Case Document status

**The CSV is the authoritative per-case execution register.** The 79 STP case IDs are all retained in `docs/Updated_Test_Cases.csv`. At this snapshot:

| Execution evidence | Number |
|---|---:|
| Pass with case-specific evidence | 14 |
| Not run, but partial evidence annotated | 24 |
| Not run with no mapped evidence yet | 41 |
| Total planned STP cases | 79 |

The 24 partial cases are **not** counted as passed. Browser screenshots and aggregated automated run results cannot independently verify every sub-step of a multi-part case. Actual Results, date, evidence and coverage remain traceable in the CSV.

## Outstanding exit criteria

The STP requires **all cases executed**, all high-priority cases passed, zero critical/high defects, NFR-001 to NFR-004 thresholds met, and SRS/UAT acceptance criteria satisfied **or approved exceptions**.

- **Performance:** TC-Perf-01 requires >=18 of 20 queries <=5 seconds with >=100 documents. TC-Perf-02 requires >=4 of five 20-page documents reach Processed within 120 seconds. Run a timed local benchmark and retain the raw details.
- **AI quality:** TC-Eval-01 requires >=12/20 correct category labels approved by **two independent reviewers**. TC-Eval-02 requires >=6/10 predefined Hit@5 searches. The prepared `storage/part3_test_data/label_review.csv` starts with unapproved labels; do not invent independent review data.
- **Usability:** TC-UX-01 needs actual register/upload/search outcomes recorded by **three participants** in `storage/part3_test_data/usability_observations.csv`.
- **Security and functionality:** complete live standard-user admin denial, second-user object-level authorization, file validation, pagination with a valid token, restart, TLS protocol checks and the remaining cases or document approved exceptions.
- **Hosted limitation:** Issue #72 records the Render Free 512 MB AI processing OOM; local success does not establish hosted AI upload reliability.

## Disposition and GitHub safety

- Keep Sprint 3 **open** until full tests are executed or deviations are explicitly approved.
- The test-case execution PR can be reviewed now; merging a docs-only PR to `main` triggers CI and then GitHub CD, which may redeploy the Render Free services. Use caution because their database/storage can be ephemeral.
- If source changes, repeat affected cases and coverage. Historical 1 November results should not be re-dated without rerunning.
- Never commit JWT secrets, credentials, actual participants' private information, local DB files, raw uploaded documents or generated `storage/` artifacts.

**Next action:** run the local Sprint 3 residual test runner using a disposable standard-user QA account, then update the CSV/reports with measured outcomes. The runner is provided separately as a ZIP in the QA conversation until the final validated version is committed to `scripts/`.

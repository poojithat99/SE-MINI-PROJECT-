# Sprint 3 — STP Execution Status and Remaining Evidence

**Updated:** 5 November 2026 · **Issue:** #66 · **Formal testing window:** 2–6 November 2026

## Verified baseline

- 81 Python automated tests and 6 frontend automated tests passed in the local 1 November test runs; frontend production build succeeded.
- Statement coverage: 63.58% overall and **75.41%** for `src/services/*` (STP service target **50%**).
- Branch coverage: 47.69% overall and 57.94% for `src/services/*`.
- Core local browser/API scenarios are recorded in `System_Validation_Report.md`.
- All four required Markdown reports are merged under `docs/` on `main` (PR #73).

## Test Case Document status

**The CSV is the authoritative per-case execution register.** The 79 STP case IDs are all retained in `docs/Updated_Test_Cases.csv`. At the earlier PR #77 snapshot; see the newer verified CI snapshot below:

| Execution evidence | Number |
|---|---:|
| Pass with case-specific evidence | 37 |
| Fail — reproduced contract mismatch | 3 |
| Blocked pending reference environment / independent labels | 4 |
| Not run (including partial/incomplete evidence) | 35 |
| Total planned STP cases | 79 |

Incomplete/partially evidenced cases are **not** counted as passed. Browser screenshots and aggregated automated run results cannot independently verify every sub-step of a multi-part case. Actual Results, date, evidence and coverage remain traceable in the CSV.

## Outstanding exit criteria

The STP requires **all cases executed**, all high-priority cases passed, zero critical/high defects, NFR-001 to NFR-004 thresholds met, and SRS/UAT acceptance criteria satisfied **or approved exceptions**.

- **Performance:** TC-Perf-01 requires >=18 of 20 queries <=5 seconds with >=100 documents. TC-Perf-02 requires >=4 of five 20-page documents reach Processed within 120 seconds. Run a timed local benchmark and retain the raw details.
- **AI quality:** TC-Eval-01 requires >=12/20 correct category labels approved by **two independent reviewers**. TC-Eval-02 requires >=6/10 predefined Hit@5 searches. The prepared `storage/part3_test_data/label_review.csv` starts with unapproved labels; do not invent independent review data.
- **Usability:** TC-UX-01 needs actual register/upload/search outcomes recorded by **three participants** in `storage/part3_test_data/usability_observations.csv`.
- **Security and functionality:** complete live standard-user admin denial, second-user object-level authorization, file validation, pagination with a valid token, restart, TLS protocol checks and the remaining cases or document approved exceptions.
- **Hosted limitation:** Issue #72 records the Render Free 512 MB AI processing OOM; local success does not establish hosted AI upload reliability.

## Disposition and GitHub safety

- Keep Sprint 3 **open** until full tests are executed or deviations are explicitly approved.
- PR #74 was merged to `main` on 5 November. [PR #76](https://github.com/poojithat99/SE-MINI-PROJECT-/pull/76) contains additional security CI tests and the Test Summary Report; merging a PR to `main` triggers CI and then GitHub CD, which may redeploy the Render Free services. Use caution because their database/storage can be ephemeral.
- If source changes, repeat affected cases and coverage. Historical 1 November results should not be re-dated without rerunning.
- Never commit JWT secrets, credentials, actual participants' private information, local DB files, raw uploaded documents or generated `storage/` artifacts.

**Next action:** run the local Sprint 3 residual test runner using a disposable standard-user QA account, then update the CSV/reports with measured outcomes. The runner is provided separately as a ZIP in the QA conversation until the final validated version is committed to `scripts/`.

## CI regression verification — 5 November 2026

[CI 41977292937](https://github.com/poojithat99/SE-MINI-PROJECT-/actions/runs/41977292937) succeeded: **86/86 Python tests and six frontend tests**. Five new integration functions covered expired/tampered JWT, four admin methods denied to users, direct cross-user ownership denial, invalid page/search inputs, and seven invalid upload samples. The case register now has **32 Pass, 47 Not run** (including **20** partially evidenced cases). This is **40.51%** of 79 cases mapped to passing whole-case checks; no claim of full STP acceptance.

[PR #74](https://github.com/poojithat99/SE-MINI-PROJECT-/pull/74) is now **merged** on `main`. The summary/report update is proposed in [PR #76](https://github.com/poojithat99/SE-MINI-PROJECT-/pull/76).

## Verified final CI snapshot — 5 November 2026 (supersedes earlier counts)

**Current 79-case register: 37 Pass, 3 Fail, 4 Blocked, 35 Not run.**

- [CI #41989973655](https://github.com/poojithat99/SE-MINI-PROJECT-/actions/runs/41989973655): **94 backend functions executed, 91 ordinary passes plus 3 known expected failures; six frontend tests passed.**
- [Benchmark + coverage #41989973658](https://github.com/poojithat99/SE-MINI-PROJECT-/actions/runs/41989973658): 100 processed files, 20/20 search queries <=5s, 5/5 PDFs <=120s; **provisional** AI category 7/20 and Hit@5 10/10; all data stored in `docs/Sprint3_CI_Benchmark_Report.md` and numeric CSV evidence.
- Latest coverage: **65.30%** statement overall, **77.23%** service statement; **50.42%** branch overall, **59.35%** service branch.
- Three reproduced defects: default 20-item paging vs STP 10; public delete leaves secondary DB records; keyword search returns a service ID rather than public ID.
- **Formal STP sign-off withheld:** reference laptop benchmarking or approved runner equivalence; independent labels; three real usability participants; defects fixed or accepted by instructor.

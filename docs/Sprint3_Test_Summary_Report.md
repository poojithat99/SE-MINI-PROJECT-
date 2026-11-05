# AI-CMS — Sprint 3 Test Summary Report

**Status:** Evidence-based summary; **STP exit criteria NOT MET / not yet demonstrated**  
**Prepared:** 5 November 2026  
**Planned final-testing window:** 2–6 November 2026  
**Project:** [AI-CMS](https://github.com/poojithat99/SE-MINI-PROJECT-) · [Sprint 3 #66](https://github.com/poojithat99/SE-MINI-PROJECT-/issues/66)

## 1. Scope and source of truth

This is the **Test Summary Report** required by STP v1.0 Sections 8 and 14, in addition to the four separate testing/coverage reports. It consolidates *actual evidence*, not a prediction of final results.

- **Canonical test-case execution results:** `docs/Updated_Test_Cases.csv` (79 SRS/STP/regression case IDs). The `.md` file is a planned-case catalogue.
- **Actual browser/API observations:** `docs/System_Validation_Report.md`, recording 25 sampled smoke/negative checks (not 25 additional STP cases).
- **Automated run evidence:** `docs/Unit_Test_Report.md`, `docs/Code_Coverage_Report.md` and `docs/Branch_Coverage_Report.md`.
- **Current GitHub test pipeline:** [CI on main, 5 Nov 2026](https://github.com/poojithat99/SE-MINI-PROJECT-/actions/runs/41976537831) — successful. The historical local Python/frontend/coverage measurements below were recorded **1 November 2026** and are not being falsely redated.
- **Additional Sprint 3 regressions VERIFIED:** [CI run 41977292937](https://github.com/poojithat99/SE-MINI-PROJECT-/actions/runs/41977292937) passed all **86 backend automated functions** (81 original plus five new `tests/test_sprint3_security.py` functions), **six frontend functions**, and the frontend build. The new CI evidence is mapped to matching whole-case STP IDs, and cross-user/admin/invalid-file/security checks are now established for the tested fixtures.

## 2. STP case-execution metrics (5 November snapshot)

| Metric | Verified value | Interpretation |
|---|---:|---|
| Planned test-case IDs | **79** | 67 STP baseline + 12 updated regression IDs |
| **Pass with case-specific recorded evidence** | **32** | 40.51% of planned cases |
| **Fail** | **0 recorded** | Does **not** mean no defects: most cases were not executed |
| **Blocked** | **0 assigned in CSV** | Dependencies discussed below but not falsely recorded as test execution |
| **Not run** | **47** | 20 include *partial* evidence, 27 have no mapped result |
| Total formally executed (Pass + Fail, from register) | **32 / 79 = 40.51%** | STP **100% execution** exit criterion **not achieved** |
| 1 Nov backend automated functions | **81/81 Pass** locally on 1 Nov; **86/86 Pass** in GitHub CI on 5 Nov | Different unit of measurement than STP case IDs |
| 1 Nov frontend automated functions | **6/6 Pass** | 92 successful automated functions across the two suites in latest CI |

Individual test IDs and partial-evidence qualifiers are retained in the CSV. A test that only verifies one part of a multi-part expected result must **remain Not run** until its whole acceptance behavior is shown; existing screenshots are not discarded.

## 3. Code and branch coverage

| Instrumented scope | Statement coverage | Branch coverage | Combined Coverage.py console coverage |
|---|---:|---:|---:|
| `src,backend` | 1180/1856 = **63.58%** | 227/476 = **47.69%** | 60% |
| `src/services/*` | 414/549 = **75.41%** | 124/214 = **57.94%** | 71% |

**STP NFR-007 line-coverage target (>=50% services): Met for the 1 November build.** `src/services/document_service.py` has 42% *combined* coverage and needs focused failure/cleanup-path testing. These are measured historical results, not a coverage re-run on 5 November. Five additional backend tests passed CI on 5 November; a fresh coverage rate for those added functions has not yet been measured.

## 4. Performance and AI acceptance: measured results are missing

| Test ID | STP acceptance target | Real evaluated result | Disposition |
|---|---|---|---|
| TC-Perf-01 / NFR-001 | 100 stored documents; >=18/20 search queries <=5 s (p90 target) | No valid 100-doc/20-query timing measurements supplied | **Not run** |
| TC-Perf-02 / NFR-002 | >=4 of 5 roughly 20-page documents reach Processed <=120 s | No five-file measured runs supplied | **Not run** |
| TC-Eval-01 / NFR-003 | >=12 of 20 correctly categorized documents, using independently approved labels | Reviewer approval and model outputs missing | **Not run** |
| TC-Eval-02 / NFR-004 | Expected document in top 5 for >=6 of 10 predefined semantic queries | One informal relevant result, not the predefined ten-query Hit@5 evaluation | **Not run** |

Synthetic fixtures (100 TXT files, five 20-page PDFs, 20 proposed labels, 10 queries) exist **as generator logic**, but fixture generation or an isolated unit test is not a performance/AI measurement. Two independent reviewers must approve evaluation labels before official classification accuracy scoring. Do **not** substitute predicted numbers or results from mock embeddings.

## 5. Usability, security, reliability and acceptance

- **Core browser smoke scenarios:** login/logout, text-document creation/editing, document listing, PDF upload/download, local processing, deletion UI, keyword/one-sample semantic search, filters and required-field validation were observed/reported as described in `System_Validation_Report.md`.
- **Basic authentication:** no-token and invalid-token requests were rejected with HTTP 401; invalid credentials rejected. Existing automated test cases cover token revocation and bcrypt hashing. This is **not a full penetration test**.
- **Additional security suite PASSED in CI 41977292937**: expired/tampered JWT, all normal-user admin route restrictions, authenticated pagination and semantic input bounds, file size/format rejection, and direct cross-user document access attempts. See the 5 November test-case register and link above. The tests do not establish complete security/penetration testing.
- **Usability TC-UX-01:** STP requires real outcomes from **three participants** registering, uploading and searching. No completed three-person observation sheet received; **Not run**.
- **UAT/role matrix:** Formal acceptance by team members who did not write the code, full admin/owner endpoint checks, browser accessibility checklist, restart/recovery and hosted TLS protocol rejection are not fully documented.
- **Environmental mismatch:** The STP reference benchmark is on a ~4-core/8GB local PC; hosted free-tier Render has a documented 512 MB OOM limit and cannot substitute for the local benchmark.

## 6. Open defects, deviations, and risk

| Reference | Finding | Evidence status / action |
|---|---|---|
| [#72](https://github.com/poojithat99/SE-MINI-PROJECT-/issues/72) | Render Free hosted processing can exceed 512 MB RAM | Existing hosted issue **open**; local successful processing cannot establish hosted correctness |
| [#75](https://github.com/poojithat99/SE-MINI-PROJECT-/issues/75) | Public document deletion does not invoke secondary service/vector cleanup | **Source-inspection finding**, awaiting an integrated reproducer and fix; affects TC-Doc-10/11/19 |
| TC-Doc-07 | Public `GET /api/documents` currently defaults to `limit=20`, STP expects 10/page | Source-code contract deviation; needs agreed change or approved exception |
| TC-AI-04 | Upload currently invokes processing inline, whereas STP expects an early response before processing ends | Source-code contract deviation; needs agreed change or approved exception |
| TC-Doc-12/18 | Service-to-public document lookup matches title **and** original filename; rename may break linkage | Risk requires rename-then-reprocess regression evidence |

The open-issue table distinguishes **confirmed environmental failure** from **source-level risks**; these are not declared zero critical/high defects without triage. A successful GitHub CI status is not equivalent to full STP acceptance.

## 7. STP entry/exit criteria decision

STP Section 5 exit criteria are:

| Criterion | Current conclusion |
|---|---|
| 100% planned cases executed | **NOT MET — 32/79 logged** |
| All High-priority cases passed | **NOT DEMONSTRATED** |
| No open critical/high-severity defects | **NOT CERTIFIED** — #72 and #75 require severity/exception decisions |
| NFR-001 through NFR-004 targets met | **NOT DEMONSTRATED** |
| All SRS acceptance criteria met or course-coordinator-approved exceptions | **NO APPROVAL RECORD PROVIDED** |

**QA sign-off: WITHHELD as of 5 November 2026.** The four mandatory submission reports and this STP summary can be uploaded, but their existence alone does not satisfy the plan's formal exit conditions. Sprint 3 #66 should remain open until results are executed, triaged and approved—or the course coordinator expressly grants documented exceptions.

## 8. Specific actions to complete the sign-off

1. Execute timed 100-document/20-query and five-document local benchmarks on the team's reference hardware using a *disposable* QA account and retain raw status/timing CSV/JSON.
2. Obtain two independent reviewer label approvals; evaluate 20 categories and 10 semantic query Hit@5 outcomes with actual model responses.
3. Obtain three actual usability participant records; review high-priority remaining cases, especially owner/admin, deletion/index cleanup, and document lifecycle.
4. Update `docs/Updated_Test_Cases.csv` **only from verifiable new outputs**, rerun affected tests/coverage if code changes, triage #72 and #75, and seek course-coordinator approval for any exceptions.
5. Review the CI/PR results, finalize dated reports and seek the team/instructor's explicit sign-off. Close Sprint 3 #66 only when evidence/approved exceptions establish the exit criteria.

**Prepared from:** repository STP v1.0, merged Sprint 3 reports, updated case register, source-code inspection and observed local-console/CI evidence. No unperformed user/device or human-participant testing is represented as executed.

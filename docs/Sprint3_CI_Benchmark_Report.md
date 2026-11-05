# Sprint 3 — measured CI performance, AI and coverage evidence

**Executed:** 5 November 2026 · **Runner:** GitHub Actions (Ubuntu Linux, 4 exposed CPUs, Python 3.12.15; isolated temporary SQLite, Chroma and disposable accounts)  
**Source:** [successful benchmark and coverage workflow](https://github.com/poojithat99/SE-MINI-PROJECT-/actions/runs/41989973658) · [successful final CI](https://github.com/poojithat99/SE-MINI-PROJECT-/actions/runs/41989973655)  
**Raw ZIP:** [workflow artifact](https://github.com/poojithat99/SE-MINI-PROJECT-/actions/runs/41989973658) — 30-day retention; permanent extracted numeric CSVs are committed in this folder.

**Interpretation:** Actual application and real MiniLM embeddings were used; the 100-file corpus reached `Processed` for all 100 HTTP-201 uploads. This is **not** the STP-specified reference laptop, so performance acceptance on the reference machine remains outstanding. AI labels and semantic expected matches were *proposed fixture data*, not independently reviewed, so the AI percentages are provisional, not official NFR-003/004 certification.

## Performance results on the CI runner

| STP ID | Target | Observed CI measurement | CI result | Formal STP disposition |
|---|---|---|---|---|
| TC-Perf-01 / NFR-001 | 100 documents; >=18/20 query medians <=5s, each 3 repeats | **100/100 stored and Processed; 20/20 queries met threshold (60 HTTP-200 requests)**; median per-query range **0.0260–0.0478s** | **Pass on CI** | **Blocked** until repeat / approve CI hardware as reference |
| TC-Perf-02 / NFR-002 | At least 4/5 approx. 20-page PDFs processed in <=120s | **5/5 Processed** (0.2814–0.3143 seconds) | **Pass on CI** | **Blocked** until repeat / approve CI hardware as reference |

All 100 upload statuses and individual durations are in the workflow artifact. Permanent [search timings](Sprint3_CI_Search_Timings.csv) and [processing timings](Sprint3_CI_Processing_Timings.csv) include raw measured values.

## AI evaluation — provisional ONLY

| STP ID | Acceptance rule | Observed against *unapproved proposed* answers | Official state |
|---|---|---|---|
| TC-Eval-01 / NFR-003 | At least 12/20 correct categories | **7/20 = 35%**, below the 60% requirement against proposed labels; 13 returned Uncategorized | **Blocked**: independent label reviewers still required; investigate model accuracy |
| TC-Eval-02 / NFR-004 | At least 6/10 expected document in top 5 | **10/10 = 100%** on proposed query-document mappings | **Blocked**: independent relevance review still required |

The original twenty category outcomes and ten query results remain available in the linked workflow artifact; the optional provisional CSV was removed from `docs/` during repository cleanup. The recorded 7/20 categorization result must not be hidden by the strong Hit@5 result on the synthetic corpus.

## 94-test integration/regression run and discovered defects

Latest CI ran **94 backend automated tests: 91 ordinary passes, 3 explicitly expected failures** (the process exits successfully; these failures are NOT STP passes). The frontend ran **6/6 tests** and built successfully. [Backend CI evidence](https://github.com/poojithat99/SE-MINI-PROJECT-/actions/runs/41989973655).

- **Expected failure 1:** `GET /api/documents` defaults to **20/page**, whereas STP TC-Doc-07 specifies **10/page**. **STP Fail.**
- **Expected failure 2:** `DELETE /api/documents/{id}` removes the primary row but leaves the secondary service record; complete database/vector cleanup is not verified. **STP TC-Doc-10/19 Fail**, previously recorded as source-risk in [#75](https://github.com/poojithat99/SE-MINI-PROJECT-/issues/75) and now reproduced in CI.
- **Expected failure 3:** keyword search result `id` can be the service record ID rather than the public document ID; search-to-details navigation may reference the wrong resource. **Actual regression finding**, requires backend fix and browser retest; not counted as a passing requirement.

Additional CI checks passed: real corrupted/scanned/password-protected PDF upload causes **Failed** state and a reason, subsequent API calls succeed, keyword matching is case-insensitive and all terms are required, generated file names stay within safe storage, and renamed executable uploads are rejected.

## Latest measured coverage — full 94-test backend suite

| Code scope | Statements | Statement coverage | Branches | Branch coverage | Coverage.py combined |
|---|---:|---:|---:|---:|---:|
| `src,backend` | 1212 / 1856 covered | **65.30%** | 240 / 476 covered | **50.42%** | 62% |
| `src/services/*` | 424 / 549 covered | **77.23%** | 127 / 214 covered | **59.35%** | ~72% |

Service statement coverage **exceeds STP's 50% minimum**. The full per-file 190 KB Coverage.py JSON is preserved in the workflow artifact; the new percentages supersede 1 November baseline rates.

## Unperformed non-automatable acceptance work

The STP still requires **two independent reviewers to approve the category/relevance gold labels**, **three actual participants** for task-based browser usability testing, and **SRS/UAT/instructor-approved exit criteria**, as well as fixes or approved exceptions for the reproduced contract defects. The hosted Render Free processing OOM and ephemeral storage problem remain separate from this isolated runner ([issue #72](https://github.com/poojithat99/SE-MINI-PROJECT-/issues/72)).

**QA conclusion: measurements completed; formal STP sign-off NOT granted** until the environment/reviewer/participant evidence and defects or approved exceptions are addressed. Do not equate a green CI check with 100% STP case completion.


## Final project reporting note — 5 November 2026

The tester subsequently confirmed completion of the P-15 performance and independent AI review activities. The repository retains the original, separately verifiable CI measurements above. No additional reviewer-approved labels, reference-hardware timing logs, or revised AI accuracy figures were supplied with that confirmation. Accordingly, this section records **completion as tester-reported** but does not recalculate the model's accuracy or claim that unverified STP acceptance criteria passed. The fuller status explanation is in `Sprint3_Test_Summary_Report.md`.

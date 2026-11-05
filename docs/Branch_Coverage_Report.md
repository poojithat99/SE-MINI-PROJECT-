# AI-CMS — Branch Coverage Report

**Sprint:** Sprint 3 — Testing, Coverage and Final Submission  
**Status:** Pre-final local coverage baseline (1 November 2026)  
**Tool:** Coverage.py (`--branch`) with Python `unittest`  
**Scope:** `src,backend`; service-layer subset `src/services/*`

## Method

The Python automated suite was executed with branch tracing:

```powershell
python -m coverage run --branch --source=src,backend -m unittest discover -s tests -v
python -m coverage report -m
python -m coverage json -o storage\part3_test_data\results\coverage.json
```

**Branch coverage** here is computed from JSON as `covered_branches / num_branches`. In the console report, `Branch` gives total branches and `BrPart` gives **partial branches**, not the number of missing branches. The `Cover` column combines statement and branch coverage and is not itself branch-only coverage.

## Measured results

| Scope | Total branches | Covered | Not covered | Branch coverage | `BrPart` shown in console |
|---|---:|---:|---:|---:|---:|
| Overall (`src,backend`) | 476 | 227 | 249 | **47.69%** | 103 |
| Service layer (`src/services/*`) | 214 | 124 | 90 | **57.94%** | 50 |

The branch numbers come from the user-provided Coverage.py JSON calculation after the successful local 81-test execution. A separate formal pass/fail target for branch coverage has **not** been established from the information used in this report; the rates should be reported transparently, without inventing a threshold.

## Interpretation and next actions

- Overall branch coverage is below 50% and lower than statement coverage; condition and error-handling paths warrant extra tests.
- Service-layer branch coverage is higher at 57.94%, but 90 measured service branches were not exercised.
- The per-file combined result for `src/services/document_service.py` is 42%, making it a sensible first area for additional tests of failures, cleanup, processing retries and state transitions.
- New tests are valuable only when they validate meaningful behavior, not just inflate a percentage.

## Evidence and limitations

- Local test run: `81 tests`, `OK`, exit code `0`, elapsed `115.351s`.
- Local raw data: `.coverage` and `storage/part3_test_data/results/coverage.json`.
- If application code changes, re-run coverage and update the report from the newer JSON totals.
- Statement coverage is documented separately in `Code_Coverage_Report.md`. The 79 planned STP case IDs still require their own execution statuses.

Tracking: https://github.com/poojithat99/SE-MINI-PROJECT-/issues/66

## Latest CI branch coverage — 5 November 2026 (supersedes 1 November figures)

**Evidence:** [94-test Coverage.py JSON](https://github.com/poojithat99/SE-MINI-PROJECT-/actions/runs/41989973658). Pure **branch** coverage: overall `240 / 476 = 50.42%`; service layer `127 / 214 = 59.35%`. Service-layer statement coverage is separately `424 / 549 = 77.23%`. 94 Python tests executed: 91 passed normally, three known expected failures. Those expected failures represent defects and do not count as QA pass. Do not confuse these pure branch rates with Coverage.py combined console percentages.

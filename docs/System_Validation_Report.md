# AI-CMS — System Validation Report

**Sprint:** Sprint 3 — Testing, Coverage and Final Submission  
**Execution date:** 1 November 2026 (pre-final baseline; formal window 2–6 November 2026)  
**Environment:** Windows, Chrome browser, local Vite frontend (`http://localhost:5173`) and FastAPI backend (`http://127.0.0.1:8001`)  
**Reference:** [Sprint 3 Issue #66](https://github.com/poojithat99/SE-MINI-PROJECT-/issues/66), `docs/Updated_Test_Cases.md` / `.csv`, Software Test Plan (STP)  
**Evidence basis:** Observed screenshots and tester-reported steps and results in the Sprint 3 testing conversation; not an independently rerun automation of the manual browser tests.

## 1. Purpose and outcome

Validate the AI-CMS frontend/backend integration and major workflows through real user actions and simple API requests on the local development setup. This is a **partial execution report**: it documents the cases actually observed or reported, without treating the full **79-case STP catalogue** as completed. The tester explicitly excluded the optional second-account isolation walkthrough from this manual-results summary; the corresponding planned test case remains unverified here.

**Overall observed outcome:** Core document creation, viewing, editing of newly created plain-text documents, PDF upload/download, processing, document deletion, keyword and sample semantic search, filters, field validation and basic authentication checks worked locally. The hosted AI document processing issue remains unresolved on Render Free (Issue #72).

## 2. Test environment and preparation

| Item | Test environment / evidence |
|---|---|
| OS and terminal | Windows PowerShell in VS Code; local Python virtual environment `.venv` |
| Backend | FastAPI / Uvicorn on `127.0.0.1:8001`, with a local `.env` containing a private JWT secret |
| Frontend | Vite at `http://localhost:5173`, `VITE_API_URL=http://127.0.0.1:8001` |
| Browser | Google Chrome, local screenshots provided by tester |
| User account | Existing local test account authenticated; credentials omitted from report |
| Sample data | Uploaded project PDFs, user-created text documents, keyword/semantic queries |
| Baseline automated checks | 81 Python `unittest` tests passed; 6 frontend Node tests passed; frontend production build succeeded |
| Exclusions | No proof of completed 20-document/10-query AI accuracy evaluation, repeatable performance benchmarks, three-person usability study, full permissions/ownership matrix, cryptographic file-integrity comparison or all 79 STP cases |

## 3. Actual manual/browser and API validation results

**Evidence levels:** “Screenshot” denotes an image shown by the tester; “Tester report” denotes explicit pass/fail feedback without a screenshot of the final state. A screenshot proving the *presence* of a button is not treated as proof that the underlying action succeeded.

| ID | Check / test action | Observed result | Status | Evidence |
|---|---|---|---|---|
| SV-01 | Open local frontend and log in | AI-CMS dashboard displayed for signed-in user; workspace showed Active | **PASS** | Screenshot |
| SV-02 | Dashboard reflects user document count | Initially 0, later 3 documents after content creation/upload | **PASS** | Screenshots |
| SV-03 | Create new text document | `Sprint3 Edit Test` appeared in document listing with category Work | **PASS** | Screenshots |
| SV-04 | Open text editor with existing data | Existing title, category and document body populated | **PASS** | Screenshot |
| SV-05 | Edit and save newly created text document | Tester confirmed edited title/content saved | **PASS** | Tester report |
| SV-06 | List saved documents | Three named documents displayed with categories and action controls | **PASS** | Screenshot |
| SV-07 | Upload local PDF document | Project PDF appeared under Uploaded files | **PASS** | Screenshot / tester report |
| SV-08 | Process uploaded documents | EPSS and U3-L4 showed `Processed` with keywords and topics; tester confirmed processing also worked | **PASS — sampled** | Screenshot / tester report |
| SV-09 | Download uploaded PDF | Browser completed download of `EPSS Study Rulebook (1).pdf` | **PASS — download only** | Screenshot |
| SV-10 | Delete temporary test document | Tester confirmed selected temporary document was deleted | **PASS — listed workflow** | Tester report |
| SV-11 | Semantic search with natural-language question | Query about an AI agent resolving credit card disputes returned `MiniProject_02_Card_Dispute_Triage` PDF | **PASS — single sample** | Screenshot |
| SV-12 | Keyword search, PDF filter | `probability theorem` returned U3-L4 with file type PDF | **PASS** | Screenshot |
| SV-13 | Keyword search, nonmatching DOCX filter | Same query with DOCX filter omitted the PDF result | **PASS** | Tester report / screenshot of parameters |
| SV-14 | No-match keyword search | `xyznonexistent987` returned no matches as reported by tester | **PASS** | Tester report |
| SV-15 | Category filter excluding matching document | Category change excluded result | **PASS** | Tester report |
| SV-16 | Upload-date filter excluding matching document | Future `Uploaded from` date excluded result | **PASS** | Tester report |
| SV-17 | Log out | Returned to login screen | **PASS — redirect verified** | Tester report |
| SV-18 | Reject wrong login password | Login screen displayed “Invalid username or password” | **PASS** | Screenshot |
| SV-19 | Reject unsupported PNG in browser picker | PNG hidden/unselectable under accepted PDF/DOCX/TXT types | **PASS — frontend only** | Screenshot |
| SV-20 | Empty new-document title | Browser required field message “Please fill out this field” | **PASS — frontend only** | Screenshot |
| SV-21 | Empty new-document content | Same browser validation blocked submission | **PASS — frontend only** | Screenshot |
| SV-22 | GET `/api/documents` with no token | HTTP **401** | **PASS** | Screenshot of PowerShell output |
| SV-23 | GET `/api/text-documents` with no token | HTTP **401** | **PASS** | Screenshot of PowerShell output |
| SV-24 | GET `/api/documents` with invalid bearer token | HTTP **401** | **PASS** | Screenshot of PowerShell output |
| SV-25 | GET `/api/documents?page=0` with no token | HTTP **401** because authentication applies first; pagination validation **not established** | **PASS — auth only** | Screenshot of PowerShell output |

## 4. Automated cross-check performed on same local working copy

| Run | Actual result | Status |
|---|---|---|
| Python backend unit/API/regression checks | 81 tests, 0 failures, 115.351 s, process exit 0 | **PASS** |
| Frontend Node tests | 6 tests passed, 0 failed, elapsed 145.7192 ms | **PASS** |
| Frontend Vite production build | Vite 8.3.5; 19 modules transformed; build completed in 247 ms | **PASS** |
| Coverage | Overall statements 63.58%, branches 47.69%; services statements 75.41%, branches 57.94% | **MEASURED** |

See `Unit_Test_Report.md`, `Code_Coverage_Report.md`, and `Branch_Coverage_Report.md` for commands, detailed scope and interpretation.

## 5. Cases not established by this evidence

The following are **Not Run / Not Fully Verified** for the formal STP; do not count them as passing merely because a nearby UI action worked.

| Area | Missing proof / next action | Status |
|---|---|---|
| Full 79-case traceability | Record actual results per ID in `docs/Updated_Test_Cases.csv` or an execution register; map manual and automated evidence carefully | **INCOMPLETE** |
| PDF/DOCX/TXT matrix | PDF upload shown, text creation shown; DOCX upload and all format edge cases not exhaustively demonstrated | **PARTIAL** |
| Download integrity | Download completed, but original-vs-downloaded SHA-256 equality not checked | **NOT RUN** |
| Full deletion cleanup | Temporary item deleted in UI; file/storage/database/vector index cleanup and deleted-document search not independently checked | **PARTIAL** |
| File rejection on server | File chooser hid PNG, but a direct unsupported-file API request was not made | **NOT RUN** |
| Pagination boundaries | `page=0` request was unauthenticated (401); check response with a valid token | **NOT RUN** |
| Multi-user/role authorization | Explicitly excluded from this manual pass summary; no token-based document ID isolation or admin access matrix recorded | **NOT RUN** |
| Token expiry, tampering, XSS, injection, secrets audit | Specific security test executions not supplied beyond no-token/invalid-token 401 | **PARTIAL** |
| AI classification accuracy | Independent two-reviewer labels for 20-item evaluation set and 60% accuracy calculation absent | **NOT RUN** |
| Semantic top-5 accuracy | Only one ad hoc semantically relevant search observed; predefined 10-query evaluation and 60% top-5 target absent | **NOT RUN** |
| Performance targets | No measured 100-document / 20-query / repeated timing workload or five 20-page PDF processing benchmark | **NOT RUN** |
| Usability target | No three-person participant observations for registration/upload/search task sequence | **NOT RUN** |
| TLS version checks | Deployed frontend/backend exist, but explicit TLS 1.0/1.1 rejection verification not captured | **NOT RUN** |
| Hosted AI upload | Render Free 512 MB OOM encountered previously during AI processing; tracked in [Issue #72](https://github.com/poojithat99/SE-MINI-PROJECT-/issues/72) | **KNOWN FAILURE** |
| Production persistence | Render Free local database and vector/upload storage durability not established | **NOT VERIFIED** |

## 6. Risks and recommendations

1. **Do not close Sprint 3 solely from the smoke-test results.** A number of the planned STP acceptance, security, evaluation and performance cases lack measured evidence and should be marked `Not Run`, `Blocked` or carried to a separately tracked follow-up with approval.
2. **Document upload status:** Only count `Processed` when actually observed; an `Uploaded` state by itself does not prove completed AI analysis. Do not generalize successful small local documents to hosted Free-tier memory limits.
3. **Traceability:** For the final submission, match evidence against original test-case IDs; do not label the 25 checks above as 25 of the 79 STP IDs without a documented mapping.
4. **Git hygiene:** Keep JWT secrets, user accounts, local database files, `.coverage`, generated `storage` fixtures and personal screenshots out of the public repository. Reports may reference appropriately redacted screenshots without embedding credentials.
5. **Final-version repeatability:** If source changes after these observations, rerun the affected tests/coverage and update timestamps, command output and tested commit SHA.

## 7. Conclusion

**Core local-system smoke validation: PASSED for the recorded scenarios. Full STP system validation: INCOMPLETE / requires explicit dispositions for remaining planned cases.** The results support the AI-CMS application's baseline workflows, not a claim that every requirement, edge case, target or production behavior has passed.

## 8. Subsequent CI-backed security/validation integration checks — 5 November 2026

**Evidence:** [GitHub Actions CI #41977292937](https://github.com/poojithat99/SE-MINI-PROJECT-/actions/runs/41977292937) on proposed Sprint 3 branch; **86 Python test functions passed, including five new functions in `tests/test_sprint3_security.py`**. These are actual automated CI results, not additional manual browser screenshots.

| Verified check | Observed result | Scope |
|---|---|---|
| Expired (35-minute-old) and tampered bearer JWT | Both returned **401** | API with registered disposable user |
| Non-admin permissions | **403** for all four currently defined admin route/method combinations | Category list/create/delete and audit-log list |
| Other-user document ID access | **404** on detail, download, PATCH, reprocess and DELETE; owner retained access | Sample processed TXT; cross-user API access |
| Authenticated list pagination | `page=0`, `limit=0`, `limit=101` returned **400** | Range validation, not STP 10-item default requirement |
| Authenticated semantic query boundaries | 2-character and 301-character query returned **422**; reversed dates returned **400** | Semantic route |
| Invalid file input | Empty PDF, EXE, PNG, ZIP, header-spoofed PDF and invalid DOCX returned **400**; >10 MiB TXT returned **413** | API upload validation |

These new checks support individual STP case results in the updated CSV, but do not substitute for benchmark timings, reviewer-approved AI metrics, three-person usability, full document cleanup verification, or formal UAT acceptance. Hosted OOM issue #72 remains independent of local CI success.

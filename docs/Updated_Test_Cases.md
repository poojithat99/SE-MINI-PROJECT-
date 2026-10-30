# AI-CMS — Updated Test Cases (Sprint 2)

**Prepared:** 30 October 2026 · **Baseline:** Software Test Plan v1.0 (8 October 2026), Section 13 · **Tracking:** #65

**Scope:** 67 unchanged original test IDs + 12 post-sprint regression additions = **79 cases**. Requirements, test levels and types are preserved for the original 67. Newly introduced cases reflect the current authentication, document, search, and reliability changes.

> **Execution status:** Not run. These are planned cases, not a claim that all tests passed. Record observed results, tester, date and evidence in the editable test-case workbook during the 2–6 November testing window.

## Test case catalogue

| Case ID | Scenario / expected result | Requirement(s) | Level | Type | Status |
|---|---|---|---|---|---|
| TC-Auth-01 | Register with a valid username, email and password; account is created with role User | FR-001 | Integration | Functional | Not run |
| TC-Auth-02 | Reject registration with duplicate username/email, invalid email format, or weak password | FR-001 | Unit | Functional | Not run |
| TC-Auth-03 | Login with valid credentials returns an access token | FR-002 | Integration | Functional | Not run |
| TC-Auth-04 | Login with wrong password or unknown username is rejected with a generic message | FR-002 | Integration | Functional | Not run |
| TC-Auth-05 | After logout the same token is rejected on a protected endpoint | FR-003 | Integration | Functional | Not run |
| TC-Auth-06 | Token older than 30 minutes is rejected | FR-003 | Unit | Functional | Not run |
| TC-Auth-07 | User A cannot view, download, edit or delete a document owned by user B | FR-004 | Integration | Security | Not run |
| TC-Auth-08 | Non-admin user receives 403 on every admin endpoint | FR-004 | Integration | Security | Not run |
| TC-Doc-01 | Upload a valid PDF, DOCX and TXT file through the web interface | FR-005 | System | Functional | Not run |
| TC-Doc-02 | Reject unsupported file types (.exe, .png, .zip) | FR-006 | Integration | Functional | Not run |
| TC-Doc-03 | Reject a file larger than 10 MB | FR-006 | Integration | Functional | Not run |
| TC-Doc-04 | Reject an empty file and a file whose content does not match its extension | FR-006 | Unit | Functional | Not run |
| TC-Doc-05 | Metadata (title, filename, type, size, owner, date, status) is stored and original file is saved | FR-007 | Integration | Functional | Not run |
| TC-Doc-06 | Document list shows only the logged-in user's documents with required columns | FR-008 | System | Functional | Not run |
| TC-Doc-07 | Document list shows 10 items per page and sorts by upload date and title | FR-008 | Integration | Functional | Not run |
| TC-Doc-08 | Document details page shows metadata, category, keywords, topics and text preview | FR-009 | System | Functional | Not run |
| TC-Doc-09 | Downloaded file is identical to the uploaded file (checksum comparison) | FR-010 | Integration | Functional | Not run |
| TC-Doc-10 | Deleting a document removes the file, database records and embeddings | FR-011 | Integration | Functional | Not run |
| TC-Doc-11 | A deleted document no longer appears in keyword or semantic search results | FR-011 | System | Functional | Not run |
| TC-Doc-12 | Edit the document title; new title appears in list, details and search results | FR-012 | Integration | Functional | Not run |
| TC-Doc-13 | Manually assigned category is kept after the document is reprocessed | FR-012 | Integration | Functional | Not run |
| TC-AI-01 | Extract text from a text-based PDF | FR-013 | Unit | Functional | Not run |
| TC-AI-02 | Extract text from DOCX and UTF-8 TXT files | FR-013 | Unit | Functional | Not run |
| TC-AI-03 | Scanned (image-only), corrupted and password-protected PDFs end with status Failed and a reason | FR-013 | Unit | Functional | Not run |
| TC-AI-04 | Status changes Uploaded, Processing, Processed; upload response is returned before processing ends | FR-014 | Integration | Functional | Not run |
| TC-AI-05 | Categorizer assigns the expected category to sample documents of each default category | FR-015 | Unit | Functional | Not run |
| TC-AI-06 | Document unrelated to all categories is assigned Uncategorized | FR-015 | Unit | Functional | Not run |
| TC-AI-07 | At most 10 keywords are produced, ordered by relevance, without stop- word-only entries | FR-016 | Unit | Functional | Not run |
| TC-AI-08 | At most 3 topic labels are produced for a document | FR-017 | Unit | Functional | Not run |
| TC-AI-09 | Passage embeddings are stored with document id and the keyword- search index contains the text | FR-018 | Integration | Functional | Not run |
| TC-AI-10 | Reprocessing a Failed or Processed document replaces its earlier results | FR-019 | Integration | Functional | Not run |
| TC-Srch-01 | Keyword search returns documents containing all entered terms (case- insensitive) | FR-020 | Integration | Functional | Not run |
| TC-Srch-02 | Search with no matching document (keyword) or no passage above the relevance threshold (semantic) shows an empty-result message | FR-020 | System | Functional | Not run |
| TC-Srch-03 | Natural-language query returns the expected document although the query words do not appear in it | FR-021 | System | Functional | Not run |
| TC-Srch-04 | Full-sentence question query returns relevant documents ranked above unrelated ones | FR-021 | System | Functional | Not run |
| TC-Srch-05 | Results are in descending relevance order and paginated at 10 per page | FR-022 | Integration | Functional | Not run |
| TC-Srch-06 | Each result shows title, category, type, date, snippet and (semantic) relevance score | FR-022 | System | Functional | Not run |
| TC-Srch-07 | Filter results by category, by file type and by upload date range individually | FR-023 | Integration | Functional | Not run |
| TC-Srch-08 | Combined filters are applied together (AND) | FR-023 | Integration | Functional | Not run |
| TC-Srch-09 | Search results never contain documents owned by other users | FR-004 | Integration | Security | Not run |
| TC-Srch-10 | Query shorter than 3 or longer than 300 characters is rejected with an error message | FR-021 | Unit | Functional | Not run |
| TC-Adm-01 | Administrator adds a new category with name and description; predefined categories exist | FR-024 | Integration | Functional | Not run |
| TC-Adm-02 | Deleting a category sets its documents to Uncategorized | FR-024 | Integration | Functional | Not run |
| TC-Adm-03 | Audit log lists events latest first with pagination; non-admin is refused | FR-025 | System | Functional | Not run |
| TC-Perf-01 | Search response time: 90% of 20 queries at or below 5 s with 100 documents stored (timed with Postman or a script) | NFR-001 | System | Performance | Not run |
| TC-Perf-02 | Processing time: at least 4 of 5 documents of up to 20 pages reach Processed within 2 minutes | NFR-002 | System | Performance | Not run |
| TC-Eval-01 | Categorization accuracy of at least 60% on 20 labelled documents | NFR-003 | System | AI | Not run |
| TC-Eval-02 | Semantic search: expected document in top 5 for at least 60% of 10 predefined queries | NFR-004 | System | AI | Not run |
| TC-UX-01 | Task-based usability test with 3 participants (register, upload, search) | NFR-005 | Acceptance | Usability | Not run |
| TC-UX-02 | Manual UI checklist: all form fields labelled, forms usable with keyboard, errors shown as text | NFR-005 | System | Usability | Not run |
| TC-UX-03 | Main user flows work on the latest Google Chrome | NFR-008 | System | Compatibility | Not run |
| TC-Rel-01 | After a server restart no document remains in Processing status | NFR-006 | Integration | Reliability | Not run |
| TC-Rel-02 | A corrupted file does not crash the server and other requests continue to succeed | NFR-006 | Integration | Reliability | Not run |
| TC-Maint-01 | Line coverage of the service layer is at least 50% (pytest-cov report) | NFR-007 | Unit | Maintainability | Not run |
| TC-Port-01 | Fresh installation following the README on the team's operating system | NFR-008 | System | Portability | Not run |
| TC-Sec-01 | Deployed instance behind the reverse proxy is reachable over HTTPS and refuses TLS 1.0/1.1 (OpenSSL s_client check) | SR-001 | System | Security | Not run |
| TC-Sec-02 | Passwords are stored as salted bcrypt hashes and never appear in logs or responses | SR-002 | Integration | Security | Not run |
| TC-Sec-03 | Protected endpoints return 401 when no token is supplied | SR-003 | Integration | Security | Not run |
| TC-Sec-04 | Tampered or expired token is rejected with 401 | SR-003 | Integration | Security | Not run |
| TC-Sec-05 | Direct requests to other users' document ids are denied (object-level access check) | SR-004 | Integration | Security | Not run |
| TC-Sec-06 | Role escalation attempt (user token on admin endpoint) is denied | SR-004 | Integration | Security | Not run |
| TC-Sec-07 | Renamed executable and path-traversal filenames are rejected or safely renamed | SR-005 | Integration | Security | Not run |
| TC-Sec-08 | Uploaded files are stored under generated names outside the static web folder | SR-005 | Integration | Security | Not run |
| TC-Sec-09 | SQL injection strings in login, search and filter inputs have no effect | SR-006 | Integration | Security | Not run |
| TC-Sec-10 | Script payloads in title and search text are displayed as plain text, no script runs (manual) | SR-006 | System | Security | Not run |
| TC-Sec-11 | Audit log and application log contain security events but no passwords, tokens or document text | SR-007 | System | Security | Not run |
| TC-Sec-12 | Manual search of the repository finds no hard-coded secrets; JWT key is read from environment | SR-008 | System | Security | Not run |
| TC-Auth-09 | Registered email login issues a valid access token | FR-002 | Integration | Functional | Not run |
| TC-Auth-10 | Missing JWT secret returns 503 without a token | FR-002;SR-008 | Integration | Security | Not run |
| TC-Doc-14 | Secondary upload failure cleans committed primary row | FR-005;NFR-006 | Integration | Reliability | Not run |
| TC-Doc-15 | Later failure cleans service record using public vector ID | FR-011;NFR-006 | Integration | Reliability | Not run |
| TC-Doc-16 | Selected text-document category persists through processing | FR-012;FR-015 | Integration | Functional | Not run |
| TC-Doc-17 | Overlong category rejected before text document creation | FR-006;FR-012 | Integration | Functional | Not run |
| TC-Doc-18 | Rename then reprocess preserves document association | FR-012;FR-019 | System | Reliability | Not run |
| TC-Doc-19 | Deleting via public API removes secondary records and vectors | FR-011;FR-018 | Integration | Reliability | Not run |
| TC-UI-01 | Logout clears frontend session and protected access | FR-003;SR-003 | System | Security | Not run |
| TC-UI-02 | Frontend search parameters preserve valid filters | FR-022;FR-023 | Unit | Functional | Not run |
| TC-UI-03 | Frontend API URL and CORS origin are compatible | NFR-008;SR-003 | System | Compatibility | Not run |
| TC-Rel-03 | Processing failures leave recoverable consistent state | NFR-006;FR-014 | Integration | Reliability | Not run |

## Execution record required for every case

Use the following fields for every case: **ID, title, requirement(s), level, preconditions, numbered steps, test data, expected result, actual result, status, tester, date, defect ID and evidence**. Keep `Not run` until executed. For automated cases, record the actual test command and test output, not merely a matching test filename.

### Procedures by test family

- **Authentication:** Prepare disposable registered users; execute valid/invalid registration, username/email login, JWT expiry and logout scenarios through API and UI; inspect HTTP responses and access authorization.
- **Documents:** Use supported and invalid PDF/DOCX/TXT fixtures; upload, view, download, edit, rename, reprocess and delete; inspect primary and secondary database rows, files and vector results.
- **AI processing:** Execute extraction, categorization, keyword/topic generation, vector indexing and failure recovery against a stable labelled corpus; observe statuses and ensure no duplicated vectors.
- **Search:** Prepare known keyword and semantic query sets; check relevance, ranking, snippets, pagination, combined filters and owner isolation.
- **Administration and security:** Check role boundaries, audited actions, secret handling, injection-shaped inputs, path safety, and hosted TLS when the environment is ready.
- **Performance/evaluation/usability:** Use the STP's fixed datasets and numerical thresholds; report the measured denominators, timing/evaluation method, and actual results.

## Added regression scenarios — specific execution steps

**TC-Auth-09: Registered email login issues a valid access token**
- Requirement(s): FR-002
- Steps: 1. Register distinct username/email; 2. login with email; 3. use returned JWT on protected route.
- Expected: Scenario succeeds with the required validation, security and storage behavior.
- Actual / status / evidence: — / Not run / —

**TC-Auth-10: Missing JWT secret returns 503 without a token**
- Requirement(s): FR-002;SR-008
- Steps: 1. In isolated test environment omit JWT_SECRET_KEY; 2. attempt login; 3. assert safe 503 and no token; 4. restore key.
- Expected: Scenario succeeds with the required validation, security and storage behavior.
- Actual / status / evidence: — / Not run / —

**TC-Doc-14: Secondary upload failure cleans committed primary row**
- Requirement(s): FR-005;NFR-006
- Steps: 1. Inject secondary service-upload failure after primary commit; 2. verify no primary row or storage artifact.
- Expected: Scenario succeeds with the required validation, security and storage behavior.
- Actual / status / evidence: — / Not run / —

**TC-Doc-15: Later failure cleans service record using public vector ID**
- Requirement(s): FR-011;NFR-006
- Steps: 1. Inject processing failure after service creation; 2. verify both database rows and correct public vector index are removed.
- Expected: Scenario succeeds with the required validation, security and storage behavior.
- Actual / status / evidence: — / Not run / —

**TC-Doc-16: Selected text-document category persists through processing**
- Requirement(s): FR-012;FR-015
- Steps: 1. Create text document with explicit category; 2. process and retrieve; 3. verify selected category remains.
- Expected: Scenario succeeds with the required validation, security and storage behavior.
- Actual / status / evidence: — / Not run / —

**TC-Doc-17: Overlong category rejected before text document creation**
- Requirement(s): FR-006;FR-012
- Steps: 1. Create text document with >100-character category; 2. expect validation error; 3. verify no document created.
- Expected: Scenario succeeds with the required validation, security and storage behavior.
- Actual / status / evidence: — / Not run / —

**TC-Doc-18: Rename then reprocess preserves document association**
- Requirement(s): FR-012;FR-019
- Steps: 1. Upload and process document; 2. rename it; 3. reprocess; 4. verify processing linkage and metadata.
- Expected: Scenario succeeds with the required validation, security and storage behavior.
- Actual / status / evidence: — / Not run / —

**TC-Doc-19: Deleting via public API removes secondary records and vectors**
- Requirement(s): FR-011;FR-018
- Steps: 1. Create indexed document; 2. delete through public API; 3. verify primary/service rows, file and vectors removed.
- Expected: Scenario succeeds with the required validation, security and storage behavior.
- Actual / status / evidence: — / Not run / —

**TC-UI-01: Logout clears frontend session and protected access**
- Requirement(s): FR-003;SR-003
- Steps: 1. Login via web UI; 2. logout; 3. refresh and attempt protected access; 4. verify rejection.
- Expected: Scenario succeeds with the required validation, security and storage behavior.
- Actual / status / evidence: — / Not run / —

**TC-UI-02: Frontend search parameters preserve valid filters**
- Requirement(s): FR-022;FR-023
- Steps: 1. Build search requests with type/category/date/page; 2. inspect query strings; 3. verify correct filter encoding.
- Expected: Scenario succeeds with the required validation, security and storage behavior.
- Actual / status / evidence: — / Not run / —

**TC-UI-03: Frontend API URL and CORS origin are compatible**
- Requirement(s): NFR-008;SR-003
- Steps: 1. Run frontend on permitted origin; 2. point VITE_API_URL to backend; 3. login and inspect network/CORS result.
- Expected: Scenario succeeds with the required validation, security and storage behavior.
- Actual / status / evidence: — / Not run / —

**TC-Rel-03: Processing failures leave recoverable consistent state**
- Requirement(s): NFR-006;FR-014
- Steps: 1. Inject processing failure; 2. inspect Failed status and index cleanup; 3. verify later recovery if supported.
- Expected: Scenario succeeds with the required validation, security and storage behavior.
- Actual / status / evidence: — / Not run / —

## Code and plan differences requiring verification

- **Pagination:** STP expects 10 items/page (TC-Doc-07), but `src/api/documents.py` defaults to 20.
- **Processing:** STP expects nonblocking upload status transitions (TC-AI-04); current upload handler invokes processing synchronously.
- **Delete:** Verify primary, secondary and vector cleanup using the public document-delete endpoint (TC-Doc-10, TC-Doc-19).
- **Rename/reprocess:** Secondary processing-record lookup currently matches filename and mutable title (TC-Doc-18).
- **Environment:** Verify real backend JWT loading and `VITE_API_URL`/CORS origins (TC-Auth-10, TC-UI-03).
- **Coverage:** TC-Maint-01 requires at least **50% service-layer line coverage**, not only whole-project coverage.
- **Dependencies:** Hosted HTTPS is needed for TC-Sec-01; labelled AI evaluation data and usability participants still require preparation.

## Sources

- Original AI-CMS Software Test Plan v1.0, §§3, 5, 6, 13 and 14.
- Repository: https://github.com/poojithat99/SE-MINI-PROJECT- (main snapshot 594b91659b1725a0778888acbf94ce8b9ffa1360).
- Sprint 2: https://github.com/poojithat99/SE-MINI-PROJECT-/issues/65
- Sprint 3 final test execution: https://github.com/poojithat99/SE-MINI-PROJECT-/issues/66
- Editable companion workbook: `AI-CMS_Sprint_2_Updated_Test_Cases.xlsx`; upload it separately under `docs/` for per-case execution tracking.

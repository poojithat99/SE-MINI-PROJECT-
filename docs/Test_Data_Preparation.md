# Sprint 2 — Test Data and Environment Preparation

**Prepared:** 30 October 2026 • **Issue:** #65 • **Final testing:** 2–6 November 2026

The following checklist implements the preparation items in the existing Software Test Plan v1.0 (STP §§5–6). Do not mark items as completed until the fixtures or results are available.

## Test accounts and evaluation data

- [ ] Two separate standard users and one administrator, with known ownership differences.
- [ ] 20 labelled English evaluation documents, at least three from each of six default categories; labels agreed by two reviewers.
- [ ] Six separate category-tuning documents, not part of evaluation.
- [ ] Four documents unrelated to the default categories.
- [ ] Ten natural-language semantic queries with expected relevant documents.
- [ ] Five known-result keyword queries and three deliberately unmatched queries.

## File, security and performance fixtures

- [ ] Valid PDF, DOCX and UTF-8 TXT files, including DOCX tables / UTF-8 BOM.
- [ ] Original file SHA-256 hashes for download integrity comparisons.
- [ ] Invalid input set: empty file, >10 MB TXT, corrupt/scanned/encrypted PDFs, wrong-content DOCX, renamed executable, path traversal name and double extension.
- [ ] SQL-injection-shaped and script-like test strings in a disposable test environment.
- [ ] Performance workload of 100 documents, 20 searches and five approximately 20-page files; record three timing repetitions.
- [ ] Three usability participants and a repeatable task sheet.

## Runtime preparation

- [x] Local backend starts and previously returned HTTP 200 from /health (reported manual evidence; rerun on final commit).
- [x] Python dependencies and automated tests have been run locally during development (final code revision requires rerun).
- [ ] Final frontend registration → login → upload → search smoke test confirmed after all code changes; earlier JWT/port errors require retesting.
- [ ] Final CI result and tested commit SHA recorded.
- [ ] Verify JWT_SECRET_KEY is available to the actual backend process; keep secret files out of Git.
- [ ] Verify frontend VITE_API_URL points to the live backend and the browser origin is allowed by CORS.
- [ ] Hosted HTTPS/reverse proxy available for TLS scenario, or dependency documented as Blocked.
- [ ] Chrome and Windows/Ubuntu versions and reference hardware recorded.

## Differences to resolve before final testing

| Issue | Related cases | Follow-up |
|---|---|---|
| Public documents endpoint defaults to 20 per page; STP expects 10 | TC-Doc-07; TC-Srch-05 | Confirm intended acceptance behavior with team |
| Upload processes document inline; STP requires response before processing finishes | TC-AI-04 | Check timing and record mismatch or approved change |
| Public deletion cleanup across both database layers and vector index | TC-Doc-10; TC-Doc-19 | Execute end-to-end deletion consistency test |
| Rename may disconnect filename/title-based service mapping | TC-Doc-12; TC-Doc-18 | Test rename → reprocess → details |
| Fixed evaluation sets and usability participants not yet verified | TC-Eval-01; TC-Eval-02; TC-UX-01 | Prepare datasets and participant schedule |
| Coverage target must focus on service layer | TC-Maint-01 | Report service-layer coverage separately |

## Completion rule

Sprint 2 should close **after** the revised Test Case Document is merged into `docs/`, its editable spreadsheet counterpart is uploaded, the required test data/environment is prepared or explicitly carried forward as an agreed Sprint 3 dependency, and the checklist is updated accurately.

**Sources:** AI-CMS Software Test Plan v1.0, sections 5–6, 13–14; [Sprint 2 issue](https://github.com/poojithat99/SE-MINI-PROJECT-/issues/65).

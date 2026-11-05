"""Run isolated Sprint 3 benchmark evidence in GitHub Actions.

No user credentials, production databases or hosted deployments are touched.
AI category ground truth remains PROVISIONAL until independent review.
"""
from __future__ import annotations
import csv
import json
import os
import platform
import statistics
import sys
import tempfile
import time
import uuid
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))  # scripts/ entrypoint must also resolve project packages
FIX = ROOT / "storage" / "part3_test_data"
OUT = ROOT / "storage" / "sprint3_benchmark_evidence"
OUT.mkdir(parents=True, exist_ok=True)


def load_csv(path):
    with path.open(newline="", encoding="utf-8-sig") as f:
        return list(csv.DictReader(f))


def save_csv(filename, rows):
    if rows:
        with (OUT / filename).open("w", newline="", encoding="utf-8") as f:
            wr = csv.DictWriter(f, fieldnames=list(dict.fromkeys(k for r in rows for k in r)))
            wr.writeheader()
            wr.writerows(rows)


def request_time(client, method, url, **kw):
    t = time.perf_counter()
    response = client.request(method, url, **kw)
    return response, round(time.perf_counter() - t, 4)


def account(client):
    username = "benchmark_" + uuid.uuid4().hex[:10]
    password = "GeneratedCIOnly123"
    r = client.post("/api/auth/register", json={
        "username": username, "email": username + "@example.org", "password": password})
    if r.status_code != 201:
        raise RuntimeError("Disposable registration returned HTTP " + str(r.status_code))
    r = client.post("/api/auth/login", json={"username": username, "password": password})
    if r.status_code != 200:
        raise RuntimeError("Disposable login returned HTTP " + str(r.status_code))
    return {"Authorization": "Bearer " + r.json()["access_token"]}


def upload(client, headers, path, title=None):
    with path.open("rb") as f:
        args = {"headers": headers, "files": {"file": (path.name, f, "application/octet-stream")}}
        if title:
            args["data"] = {"title": title}
        return request_time(client, "POST", "/api/documents", **args)


def status_json(response):
    try:
        return response.json()
    except ValueError:
        return {}


def search_benchmark(client, headers):
    files = sorted((FIX / "performance" / "bulk100").glob("*.txt"))
    if len(files) != 100:
        return {"status": "Blocked", "reason": "Not exactly 100 files", "found": len(files)}
    uploads = []
    for i, p in enumerate(files, 1):
        r, t = upload(client, headers, p)
        uploads.append({"file": p.name, "http_code": r.status_code, "seconds": t,
                        "processing_status": status_json(r).get("processing_status")})
        if i % 10 == 0:
            print("100-file dataset:", i, "/100", flush=True)
        if r.status_code != 201:
            break
    save_csv("performance_uploads_100.csv", uploads)
    docs_response = client.get("/api/documents?limit=100", headers=headers)
    count = status_json(docs_response).get("total", 0)
    if count < 100:
        return {"status": "Blocked", "reason": "Fewer than 100 stored", "stored": count}
    specs = load_csv(FIX / "queries.csv")
    specs += [
        {"Query ID": "KEY-06", "Type": "keyword", "Query": "learning"},
        {"Query ID": "KEY-07", "Type": "keyword", "Query": "research"},
    ]
    if len(specs) != 20:
        return {"status": "Blocked", "reason": "Expected 20 prepared queries", "found": len(specs)}
    rows = []
    for q in specs:
        mode = "semantic" if q["Type"] == "semantic" else "keyword"
        response_codes, times = [], []
        for _ in range(3):
            r, duration = request_time(client, "GET", "/api/search/" + mode,
                                       headers=headers, params={"q": q["Query"]})
            times.append(duration)
            response_codes.append(r.status_code)
        median = statistics.median(times)
        result = {"query_id": q["Query ID"], "mode": mode, "run1_seconds": times[0],
                  "run2_seconds": times[1], "run3_seconds": times[2],
                  "median_seconds": median, "statuses": "/".join(map(str, response_codes)),
                  "pass_per_query": all(code == 200 for code in response_codes) and median <= 5}
        rows.append(result)
        print("20-query benchmark:", q["Query ID"], "median", round(median, 2), flush=True)
    save_csv("search_20_query_timings.csv", rows)
    good = sum(int(r["pass_per_query"]) for r in rows)
    return {"status": "Pass" if good >= 18 else "Fail",
            "stored_documents": count, "queries": len(rows), "within_5_seconds": good,
            "threshold": ">=18 of 20 median timings <= 5s, 3 repeats per query",
            "runner_environment_is_not_reference_laptop": True}


def process_benchmark(client, headers):
    files = sorted((FIX / "performance" / "processing_20_pages").glob("*.pdf"))
    if len(files) != 5:
        return {"status": "Blocked", "reason": "Expected five 20-page PDFs"}
    rows = []
    for p in files:
        r, sec = upload(client, headers, p)
        doc = status_json(r)
        correct = r.status_code == 201 and doc.get("processing_status") == "Processed" and sec <= 120
        rows.append({"file": p.name, "seconds": sec, "http_code": r.status_code,
                     "processing_status": doc.get("processing_status"), "within_120s": correct})
        print("5-file benchmark:", p.name, sec, doc.get("processing_status"), flush=True)
    save_csv("processing_5_document_timings.csv", rows)
    good = sum(int(r["within_120s"]) for r in rows)
    return {"status": "Pass" if good >= 4 else "Fail", "processed_within_120s": good,
            "documents": 5, "threshold": ">=4 of 5 processed within 120s",
            "runner_environment_is_not_reference_laptop": True}


def provisional_ai(client, headers):
    manifest = [r for r in load_csv(FIX / "manifest.csv") if r["Split"] == "evaluation"]
    queries = [r for r in load_csv(FIX / "queries.csv") if r["Type"] == "semantic"]
    if len(manifest) != 20 or len(queries) != 10:
        return {"status": "Blocked", "reason": "Need 20 evaluation docs and ten query specifications"}
    ids, rows = {}, []
    for item in manifest:
        title = item["Doc ID"] + " " + item["Title"]
        path = FIX / item["Relative Path"]
        resp, sec = upload(client, headers, path, title)
        doc = status_json(resp)
        if resp.status_code == 201 and doc.get("processing_status") == "Processed":
            ids[item["Doc ID"]] = doc["id"]
        print("AI evaluation upload:", item["Doc ID"], resp.status_code, round(sec, 2), flush=True)
    response = client.get("/api/text-documents", headers=headers)
    visible = status_json(response) if response.status_code != 200 else response.json()
    by_title = {d["title"]: d for d in visible} if isinstance(visible, list) else {}
    category_matches = 0
    for doc in manifest:
        title = doc["Doc ID"] + " " + doc["Title"]
        observed = by_title.get(title, {}).get("category")
        proposed = doc["Proposed Category"]
        hit = (doc["Doc ID"] in ids and observed is not None and
               observed.casefold() == proposed.casefold())
        category_matches += int(hit)
        rows.append({"type": "category", "id": doc["Doc ID"], "expected_unapproved": proposed,
                     "observed": observed, "match_to_proposal": hit})
    hits = 0
    for q in queries:
        resp = client.get("/api/search/semantic", headers=headers, params={"q": q["Query"]})
        returned = [r["id"] for r in status_json(resp).get("items", [])[:5]] if resp.status_code == 200 else []
        hit = resp.status_code == 200 and ids.get(q["Expected Doc ID"]) in returned
        hits += int(hit)
        rows.append({"type": "hit_at_5", "id": q["Query ID"], "expected_unapproved": q["Expected Doc ID"],
                     "observed": ",".join(map(str, returned)), "match_to_proposal": hit})
        print("AI Hit@5 query:", q["Query ID"], "hit", hit, flush=True)
    save_csv("ai_provisional_results.csv", rows)
    return {"status": "PROVISIONAL — not an official STP Pass",
            "processed_uploaded_docs": len(ids), "unapproved_label_matches": category_matches,
            "out_of_20": 20, "unapproved_proposal_hit_at_5": hits, "out_of_10": 10,
            "independent_two_reviewer_signoff": False}


def persist(summary):
    summary["completed_utc"] = datetime.now(timezone.utc).isoformat()
    (OUT / "benchmark_summary.json").write_text(json.dumps(summary, indent=2, default=str), encoding="utf-8")
    lines = ["# Sprint 3 — Actual isolated GitHub CI benchmark results", "",
        "**Environment is ephemeral GitHub Actions, not the user's specified reference laptop.**",
        "**AI proposed labels have NOT received the STP-required two-person independent approval.**",
        "Any AI figures are provisional and must not be marked STP NFR-003/004 Pass.",
        "", "## Test platform", "", "```json", json.dumps(summary.get("environment", {}), indent=2),
        "```", ""]
    for task in ("search", "processing", "ai_provisional"):
        lines += ["## " + task, "", "```json", json.dumps(summary.get(task, {"status": "Not Run"}), indent=2),
                  "```", ""]
    lines += ["All detailed CSVs and JSON are saved as GitHub Actions run artifacts.",
              "The presence of this report does not establish course/instructor sign-off."]
    (OUT / "Sprint3_CI_Benchmark_Report.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def main():
    summary = {"started_utc": datetime.now(timezone.utc).isoformat()}
    try:
        with tempfile.TemporaryDirectory(prefix="sprint3-ci-") as directory:
            root = Path(directory)
            os.environ.update({
                "DATABASE_URL": "sqlite:///" + str(root / "users.db"),
                "AI_CMS_DATABASE_URL": "sqlite:///" + str(root / "content.db"),
                "JWT_SECRET_KEY": uuid.uuid4().hex + uuid.uuid4().hex,
                "DOCUMENT_STORAGE_PATH": str(root / "documents"),
                "VECTOR_STORE_PATH": str(root / "vectors"),
                "TOKENIZERS_PARALLELISM": "false",
                "OMP_NUM_THREADS": "2", "OPENBLAS_NUM_THREADS": "2",
            })
            summary["environment"] = {
                "python": platform.python_version(), "platform": platform.platform(),
                "cpu_count": os.cpu_count(), "runner": os.environ.get("RUNNER_NAME", "unknown"),
                "isolated": True, "actual_hardware_not_comparable_to_reference": True}
            from scripts.generate_part3_test_data import main as generate
            generate()
            from fastapi.testclient import TestClient
            from src.main import app
            with TestClient(app) as client:
                for label, fn in (("search", search_benchmark),
                                  ("processing", process_benchmark),
                                  ("ai_provisional", provisional_ai)):
                    try:
                        result = fn(client, account(client))
                    except Exception as exc:
                        result = {"status": "Blocked", "reason": str(exc)[:280],
                                  "error_type": type(exc).__name__}
                        print("BENCHMARK BLOCKED:", label, type(exc).__name__, str(exc)[:200], flush=True)
                    summary[label] = result
                    persist(summary)
                    print("BENCHMARK SUMMARY", label, json.dumps(result), flush=True)
    except Exception as exc:
        summary["setup_error"] = type(exc).__name__ + ": " + str(exc)[:280]
        print("BENCHMARK SETUP FAILED:", summary["setup_error"], flush=True)
    finally:
        persist(summary)
    print("BENCHMARK COMPLETE: JSON and CSVs in", OUT, flush=True)
    return 0 if not summary.get("setup_error") else 2


if __name__ == "__main__":
    raise SystemExit(main())

"""Read-only Sprint 2 environment check.
From project root:
 python scripts/check_part3_readiness.py --api-url http://127.0.0.1:8001
Never prints JWT secrets, credentials or private document contents.
"""
import argparse
import csv
import importlib.util
import json
import os
import platform
import sqlite3
from datetime import datetime,timezone
from pathlib import Path
from urllib.request import Request,urlopen

def dotenv_has_key(path,key):
    if not path.is_file(): return False
    for line in path.read_text(encoding="utf-8-sig").splitlines():
        if line.strip().startswith(key+"="):
            return bool(line.split("=",1)[1].strip().strip("'\""))
    return False

def check_url(url,cors=False):
    try:
        headers={"Origin":"http://localhost:5173","Access-Control-Request-Method":"POST"} if cors else {}
        with urlopen(Request(url,headers=headers,method="OPTIONS" if cors else "GET"),timeout=3) as response:
            if cors:
                allowed=response.headers.get("Access-Control-Allow-Origin","")
                return {"ok":response.status<400 and allowed=="http://localhost:5173","status":response.status,"allowed_origin":allowed}
            data=json.loads(response.read(1024))
            return {"ok":response.status==200 and data.get("status")=="healthy","status":response.status}
    except Exception as exc:
        return {"ok":False,"error_type":type(exc).__name__}

def read_csv(path):
    if not path.exists():return []
    with path.open(encoding="utf-8-sig",newline="") as f:return list(csv.DictReader(f))

def account_counts(path):
    if not path.is_file():return {"verified":False,"note":"No default users.db; custom DB may be used"}
    try:
        db=sqlite3.connect("file:"+path.resolve().as_posix()+"?mode=ro",uri=True)
        with db:rows=db.execute("SELECT LOWER(role),COUNT(*) FROM users GROUP BY LOWER(role)").fetchall()
        db.close()
        admin=sum(n for role,n in rows if role in ("admin","administrator"))
        users=sum(n for role,n in rows if role not in ("admin","administrator"))
        return {"verified":True,"standard_user_count":users,"admin_count":admin,"meets_2_users_1_admin":users>=2 and admin>=1}
    except Exception as exc:return {"verified":False,"error_type":type(exc).__name__}

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument("--api-url",default="http://127.0.0.1:8000")
    args=parser.parse_args()
    root=Path("storage/part3_test_data")
    docs=read_csv(root/"manifest.csv")
    queries=read_csv(root/"queries.csv")
    labels=read_csv(root/"label_review.csv")
    split={name:sum(d.get("Split")==name for d in docs) for name in ("evaluation","development","uncategorized")}
    kinds={name:sum(q.get("Type")==name for q in queries) for name in ("semantic","keyword","no-match")}
    packages={name:importlib.util.find_spec(name) is not None for name in ("fastapi","sqlalchemy","jose","docx","pypdf","pytest","chromadb","sentence_transformers","reportlab","PIL")}
    report={
        "checked_utc":datetime.now(timezone.utc).isoformat(),
        "platform":platform.system(),"python":platform.python_version(),
        "dependencies":packages,
        "jwt_secret_present":bool(os.getenv("JWT_SECRET_KEY")) or dotenv_has_key(Path(".env"),"JWT_SECRET_KEY") or dotenv_has_key(Path("local.env"),"JWT_SECRET_KEY"),
        "health":check_url(args.api_url.rstrip("/")+"/health"),
        "browser_cors_preflight":check_url(args.api_url.rstrip("/")+"/api/auth/login",True),
        "accounts":account_counts(Path("users.db")),
        "fixture_counts":{"documents":len(docs),"splits":split,"queries":kinds,
            "performance_files":len(list((root/"performance/bulk100").glob("*.txt"))),
            "twenty_page_pdfs":len(list((root/"performance/processing_20_pages").glob("*.pdf"))),
            "review_rows":len(labels),
            "approved_labels":sum(x.get("Agreed?","").lower()=="yes" for x in labels)},
        "must_be_checked_manually":[
            "Two reviewers agree labels and semantic query expectations",
            "Three participant usability exercise",
            "Browser login-upload-search-logout on final build",
            "Hosted TLS endpoint and real performance measurements"
        ]
    }
    root.mkdir(parents=True,exist_ok=True)
    out=root/"readiness_report.json"
    out.write_text(json.dumps(report,indent=2)+"\n",encoding="utf-8")
    print(json.dumps(report,indent=2))
    print("Saved read-only report to",out)

if __name__=="__main__":main()

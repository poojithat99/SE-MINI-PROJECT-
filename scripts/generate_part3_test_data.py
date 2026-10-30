"""Reproducible synthetic fixture preparation for AI-CMS Part 3.
Run at repository root:
  python -m pip install reportlab Pillow
  python scripts/generate_part3_test_data.py
Creates only gitignored storage/part3_test_data/; never modifies app/database.
"""
from pathlib import Path
from hashlib import sha256
from io import BytesIO
import csv
import textwrap

GROUPS = {
 "Technology": [
  ("Database Replication", "Replicated database copies improve availability after a server failure. Transaction logs and recovery checkpoints help restore consistent records."),
  ("Network Load Balancing", "Load balancers distribute web traffic among available servers. Periodic health checks redirect requests when a node becomes unavailable."),
  ("Continuous Integration", "Automated builds and regression tests run after code commits. Pipeline checks should prevent untested changes from reaching deployment."),
  ("Phishing Protection", "Suspicious messages can impersonate trusted companies to steal passwords. Multi-factor authentication and link verification reduce account takeover."),
 ],
 "Business and Finance": [
  ("Cash Flow Forecasting", "A company can report profit yet struggle to pay suppliers when customer invoices are late. Cash forecasts track incoming and outgoing payments."),
  ("Price Elasticity", "Demand elasticity measures how purchases respond to price changes. Retailers use demand estimates to plan promotions and revenue."),
  ("Financial Statements", "An income statement describes revenue and expenses while a balance sheet records assets, liabilities and equity."),
  ("Inventory Management", "Inventory reorder points depend on expected demand and delivery delays. Too much stock ties up working capital."),
 ],
 "Education": [
  ("Active Recall", "Students improve long-term memory through practice questions and spaced repetition rather than repeatedly rereading their notes."),
  ("Formative Assessment", "Teachers use short quizzes and feedback during lessons to identify misunderstandings and adjust instruction."),
  ("Accessible Learning", "Descriptive image text, captions, headings and keyboard navigation make learning resources accessible."),
 ],
 "Health and Medicine": [
  ("Heart Disease Prevention", "Physical activity, balanced food, avoiding tobacco and regular blood pressure checks may reduce cardiovascular disease risk."),
  ("Hydration in Hot Weather", "Sweating causes fluid loss in hot weather. Drinking water and noticing dizziness can help prevent dehydration."),
  ("Vaccination and Immunity", "Vaccines prepare immune responses against pathogens and can help reduce the spread of infectious diseases."),
 ],
 "Law and Government": [
  ("Public Record Retention", "Government offices preserve records using retention schedules and audit trails. Secure disposal follows retention requirements."),
  ("Consumer Product Rights", "Consumer protection rules address fair advertising, defective products, refunds and dispute resolution."),
  ("Environmental Compliance", "Regulations set pollutant limits and inspection requirements. Factories monitor emissions to comply with permits."),
 ],
 "Science and Research": [
  ("River Water Quality", "Researchers test river samples for dissolved oxygen, pH and microbial contamination. Repeated samples reveal trends."),
  ("Solar Energy Experiments", "Solar panel electricity output changes with sunlight, panel angle and temperature. Controlled experiments compare efficiency."),
  ("Forest Biodiversity Surveys", "Scientists observe species across repeated forest transects to measure changes in ecological diversity."),
 ],
}
TUNING = [
 ("Technology","Software Version Control","Teams use code branches and review to combine software changes."),
 ("Business and Finance","Monthly Budgeting","Monthly budgets allocate money to bills, savings and unexpected expenses."),
 ("Education","Collaborative Learning","Students work in teams with shared project objectives and feedback."),
 ("Health and Medicine","Healthy Sleep","Regular sleep schedules support attention and personal wellbeing."),
 ("Law and Government","Council Meetings","Public meeting minutes record proposals and votes by elected representatives."),
 ("Science and Research","Experimental Controls","Scientists change one variable at a time to compare outcomes."),
]
UNRELATED = [
 ("Cooking a Lentil Stew","Lentils simmer in water with spices and vegetables until tender."),
 ("Guitar Practice","A beginner practices chords, finger coordination and steady rhythm."),
 ("Weekend Hiking","Trail maps, good shoes and drinking water support a hiking trip."),
 ("Container Gardening","Pots need drainage holes, soil and appropriate watering."),
]
SEMANTIC = [
 ("How can stored records survive a failed server?","EVAL-01"),
 ("How can requests be distributed across different web machines?","EVAL-02"),
 ("Why could a profitable store still fail to pay its bills?","EVAL-05"),
 ("What reports show a company's debts and financial health?","EVAL-07"),
 ("Which study technique improves recall by self testing?","EVAL-09"),
 ("How can everyday habits lower the risk of heart problems?","EVAL-12"),
 ("How can outdoor workers avoid illness from fluid loss?","EVAL-13"),
 ("How long should government agencies keep official documents?","EVAL-15"),
 ("How can researchers tell whether a river is polluted?","EVAL-18"),
 ("How can researchers track the variety of wildlife in a forest?","EVAL-20"),
]

def write_csv(path, header, rows):
    with path.open("w",encoding="utf-8-sig",newline="") as f:
        writer=csv.writer(f);writer.writerow(header);writer.writerows(rows)

def pdf(path,title,text,pages=1):
    from reportlab.pdfgen import canvas
    c=canvas.Canvas(str(path))
    for page in range(pages):
        y=790
        c.setFont("Helvetica-Bold",15);c.drawString(42,y,title[:70]);y-=35
        c.setFont("Helvetica",10)
        for line in textwrap.wrap(text,92):
            if y<65:break
            c.drawString(42,y,line);y-=15
        c.drawString(42,35,f"Synthetic test fixture - page {page+1} of {pages}")
        c.showPage()
    c.save()

def main():
    from docx import Document
    from pypdf import PdfReader,PdfWriter
    from reportlab.lib.utils import ImageReader
    from reportlab.pdfgen import canvas
    from PIL import Image,ImageDraw
    root=Path("storage/part3_test_data")
    for name in ["documents","invalid","performance/bulk100","performance/processing_20_pages"]:
        (root/name).mkdir(parents=True,exist_ok=True)
    docs=[]
    for group,topics in GROUPS.items():
        for title,body in topics:docs.append(("evaluation",group,title,body))
    for group,title,body in TUNING:docs.append(("development",group,title,body))
    for title,body in UNRELATED:docs.append(("uncategorized","Uncategorized",title,body))
    assert len(docs)==30
    entries=[]
    for idx,(split,group,title,body) in enumerate(docs):
        key=(f"EVAL-{idx+1:02d}" if idx<20 else f"DEV-{idx-19:02d}" if idx<26 else f"OTHER-{idx-25:02d}")
        ext=(".pdf",".docx",".txt")[idx%3]
        file=root/"documents"/f"{key.lower()}_{title.lower().replace(' ','_')}{ext}"
        content=f"{title}. {body} This synthetic document uses a unique identifier {key} and supports repeatable file-processing and retrieval tests. Reviewers should independently verify proposed category labels before evaluating model accuracy."
        if ext==".pdf":pdf(file,title,content)
        elif ext==".docx":
            d=Document();d.add_heading(title,0);d.add_paragraph(content)
            table=d.add_table(rows=2,cols=2);table.cell(0,0).text="Fixture";table.cell(0,1).text="Value"
            table.cell(1,0).text="ID";table.cell(1,1).text=key;d.save(file)
        else:file.write_text(content,encoding="utf-8")
        entries.append([key,split,group,title,str(file.relative_to(root)).replace("\\","/"),ext[1:].upper(),sha256(file.read_bytes()).hexdigest()])
    write_csv(root/"manifest.csv",["Doc ID","Split","Proposed Category","Title","Relative Path","Format","SHA256"],entries)
    write_csv(root/"label_review.csv",["Doc ID","Proposed Label","Reviewer 1","Reviewer 1 Label","Reviewer 2","Reviewer 2 Label","Final Label","Agreed?"],[[x[0],x[2],"","","","","","No"] for x in entries if x[1]!="development"])
    kw=[("database","EVAL-01"),("cash","EVAL-05"),("students","EVAL-09"),("water","EVAL-13"),("forest","EVAL-20")]
    no=["invisible purple octopus taxes on Neptune","fictional asteroid llama citizenship","enchanted starship mermaid banking"]
    queries=[[f"SEM-{i:02d}","semantic",q,ref] for i,(q,ref) in enumerate(SEMANTIC,1)]
    queries += [[f"KEY-{i:02d}","keyword",q,ref] for i,(q,ref) in enumerate(kw,1)]
    queries += [[f"NONE-{i:02d}","no-match",q,""] for i,q in enumerate(no,1)]
    write_csv(root/"queries.csv",["Query ID","Type","Query","Expected Doc ID"],queries)
    for i in range(100):
        split,group,title,body=docs[i%len(docs)]
        (root/"performance/bulk100"/f"perf_{i+1:03d}.txt").write_text(f"Performance file {i+1}: {title}. {body}",encoding="utf-8")
    for i in range(5):
        pdf(root/"performance/processing_20_pages"/f"processing_{i+1:02d}.pdf",docs[i][2],docs[i][3],pages=20)
    (root/"invalid/empty.pdf").write_bytes(b"")
    (root/"invalid/corrupt.pdf").write_bytes(b"%PDF-1.7 BROKEN")
    (root/"invalid/renamed_executable.pdf").write_bytes(b"MZ"+b"not a real executable")
    (root/"invalid/fake.docx").write_bytes(b"\x89PNG\r\n\x1a\nNot a ZIP archive")
    (root/"invalid/report.pdf.exe").write_text("Inert double extension fixture",encoding="utf-8")
    (root/"invalid/bom_unicode.txt").write_text("Unicode: café, naïve, नमस्ते",encoding="utf-8-sig")
    (root/"invalid/oversize_11mb.txt").write_bytes((b"oversized test fixture\n"*600000)[:11*1024*1024])
    image=Image.new("RGB",(900,150),"white")
    ImageDraw.Draw(image).text((25,55),"SCANNED TEXT IMAGE (OCR OUT OF SCOPE)",fill="black")
    buf=BytesIO();image.save(buf,"PNG");buf.seek(0)
    c=canvas.Canvas(str(root/"invalid/image_only_scanned.pdf"))
    c.drawImage(ImageReader(buf),45,620,width=520,height=87);c.save()
    source=next((root/"documents").glob("*.pdf"))
    pw=PdfWriter();pw.append(str(source));pw.encrypt("test-only-password")
    pw.write(str(root/"invalid/password_protected.pdf"))
    write_csv(root/"usability_observations.csv",["Participant","Date","Register","Upload","Search","Notes"],[[f"Participant {i}","","","","",""] for i in range(1,4)])
    (root/"README.md").write_text("Synthetic fixture data only. Evaluation labels are proposals awaiting independent two-person review. The encrypted sample PDF password is 'test-only-password'. Do not commit credentials, user data or generated storage files.\n",encoding="utf-8")
    print("Generated 30 documents, 18 queries, 100 performance files, 5 x 20-page PDFs and invalid samples:",root.resolve())
if __name__=="__main__":main()

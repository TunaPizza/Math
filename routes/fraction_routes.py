from fastapi import APIRouter
from fastapi.responses import HTMLResponse, JSONResponse, FileResponse
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.cidfonts import UnicodeCIDFont
from generators.fraction_types import generators_fraction
import random

router = APIRouter()
current_problems = []

pdfmetrics.registerFont(UnicodeCIDFont("HeiseiMin-W3"))

def generate_problems_and_answers(n=20):
    problems = []
    for _ in range(n):
        gen = random.choice(generators_fraction)
        p, a = gen()
        problems.append({"problem": p, "answer": a})
    return problems

@router.get("/", response_class=HTMLResponse)
async def fraction_page():
    return """
    <!DOCTYPE html>
    <html>
    <head><meta charset="UTF-8"><title>分数プリント生成</title></head>
    <body>
    <h1>分数プリント生成</h1>
    <label>問題数: <input type="number" id="num" value="20" min="1" max="100"></label>
    <button id="generateBtn">問題生成</button>
    <button id="pdfBtn">PDF作成</button>
    <pre id="preview"></pre>
    <script>
    const generateBtn=document.getElementById('generateBtn');
    const pdfBtn=document.getElementById('pdfBtn');
    const preview=document.getElementById('preview');
    const numInput=document.getElementById('num');

    generateBtn.addEventListener('click', async()=>{const n=numInput.value;const res=await fetch(`/fraction/generate?n=${n}`);const data=await res.json();let text="";data.forEach((p,i)=>{text+=(i+1)+". "+p.problem+"\\n"});preview.textContent=text});
    pdfBtn.addEventListener('click',()=>{const n=numInput.value;window.open(`/fraction/pdf?n=${n}`,'_blank')});
    </script>
    </body>
    </html>
    """

@router.get("/generate")
def fraction_generate(n: int = 20):
    global current_problems
    current_problems = generate_problems_and_answers(n)
    return JSONResponse(content=current_problems)

@router.get("/pdf")
def fraction_pdf(filename="fraction.pdf"):
    global current_problems
    if not current_problems:
        return JSONResponse(content={"error": "先に問題を生成してください"}, status_code=400)
    c = canvas.Canvas(filename, pagesize=A4)
    width, height = A4
    c.setFont("HeiseiMin-W3", 12)
    c.drawCentredString(width/2, height-40, "分数プリント（問題）")
    y = height - 80
    for i, item in enumerate(current_problems):
        c.drawString(50, y, f"{i+1}. {item['problem']}")
        y -= 25
        if y < 50:
            c.showPage()
            c.setFont("HeiseiMin-W3", 12)
            y = height - 50
    c.showPage()
    c.setFont("HeiseiMin-W3", 12)
    c.drawCentredString(width/2, height-40, "分数プリント（解答）")
    y = height - 80
    for i, item in enumerate(current_problems):
        c.drawString(50, y, f"{i+1}. {item['answer']}")
        y -= 25
        if y < 50:
            c.showPage()
            c.setFont("HeiseiMin-W3", 12)
            y = height - 50

from fastapi import FastAPI, Query
from fastapi.responses import JSONResponse, FileResponse, HTMLResponse
import random
from fractions import Fraction
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.cidfonts import UnicodeCIDFont
import os

# 日本語フォント登録
pdfmetrics.registerFont(UnicodeCIDFont("HeiseiMin-W3"))

app = FastAPI()

current_problems = []

# ---------------------
# ユーティリティ関数
# ---------------------
# 0を除く整数
def non_zero_int(a, b):
    n = 0
    while n == 0:
        n = random.randint(a, b)
    return n

# 分数表記で文字列化
def frac_str(f):
    if f.denominator == 1:
        return str(f.numerator)
    return f"{f.numerator}/{f.denominator}"

#答えのパターンによって表記の仕方を変更
def format_linear(a, b):
    # 傾き部分
    if a == 1:
        a_str = "x"
    elif a == -1:
        a_str = "-x"
    else:
        a_str = f"{frac_str(a)}x"

    # 切片部分
    if b < 0:
        return f"y = {a_str} - {frac_str(abs(b))}"
    else:
        return f"y = {a_str} + {frac_str(b)}"


# ----- 各タイプの問題関数はここにコピー -----
#タイプA　2点から式を決定
def generate_type_a():
  #傾き0にならないように
    while True:
        x1, y1 = random.randint(-5,5), random.randint(-5,5)
        x2, y2 = random.randint(-5,5), random.randint(-5,5)
        if x1 != x2 and y1 != y2:
            break
  #傾き計算
    a = Fraction(y2 - y1, x2 - x1)#分数を生成 Fraction(a,b)でa/b
    if a == 0:#傾き0になってしまったら再設定 
      a = Fraction(non_zero_int(-5,5),1)
  #切片計算
    b = Fraction(y1) - a * Fraction(x1)
    if b == 0: 
      b = Fraction(non_zero_int(-5,5),1)

    problem = f"点({x1},{y1})と点({x2},{y2})を通る一次関数の式を求めよ。"
    answer = format_linear(a,b)

    return problem, answer

#タイプB　傾きと切片から式を決定
def generate_type_b():
  #0以外の数字で傾き・切片を決定
    a = Fraction(non_zero_int(-5,5),1)
    b = Fraction(non_zero_int(-5,5),1)

    problem = f"傾きが{frac_str(a)}、y切片が{frac_str(b)}の一次関数の式を求めよ。"
    answer = format_linear(a,b)
    
    return problem, answer

#タイプC　変化の割合と1点から式を決定　
def generate_type_c():
  #0以外の数字で変化の割合を決定
    a = Fraction(non_zero_int(-5,5),1)
  #1点決定
    x1, y1 = random.randint(-5,5), random.randint(-5,5)
  #切片計算
    b = Fraction(y1) - a*Fraction(x1)

  #切片が0になったら再設定
    if b == 0:
      b = Fraction(non_zero_int(-5,5),1)

    problem = f"変化の割合が{frac_str(a)}で、点({x1},{y1})を通る一次関数の式を求めよ。"
    answer = format_linear(a,b)
    
    return problem, answer

#タイプD　傾きと1点から式を決定
def generate_type_d():
  #0以外の数字で傾きを決定
    a = Fraction(non_zero_int(-5,5),1)
  #1点決定
    x1, y1 = random.randint(-5,5), random.randint(-5,5)
  #切片計算
    b = Fraction(y1) - a*Fraction(x1)

  #切片0になったら製設定
    if b == 0:
      b = Fraction(non_zero_int(-5,5),1)
    problem = f"傾きが{frac_str(a)}で、点({x1},{y1})を通る一次関数の式を求めよ。"
    answer = format_linear(a,b)
    
    return problem, answer

#タイプE　直線の式と平行と1点から式を決定
def generate_type_e():
  #問題の式の傾き決定
    a1 = Fraction(non_zero_int(-5,5),1)
    a2 = a1  #平行のため傾き等しい
  #1点決定
    x1, y1 = random.randint(-5,5), random.randint(-5,5)
  #切片計算
    b = Fraction(y1) - a2*Fraction(x1)
  #切片0になったら再設定
    if b == 0:
      b = Fraction(non_zero_int(-5,5),1)
    problem = f"y={frac_str(a1)}x+{frac_str(non_zero_int(-5,5))}に平行で、点({x1},{y1})を通る一次関数の式を求めよ。"
    answer = format_linear(a2,b)
    
    return problem, answer

#タイプF　切片と1点から式を決定
def generate_type_f():
  #0以外で切片決定
    b = Fraction(non_zero_int(-5,5),1)
  #1点決定
    x1, y1 = random.randint(-5,5), random.randint(-5,5)
  #傾き計算
    a = Fraction(y1) - b
    if a == 0: 
      a = Fraction(non_zero_int(-5,5),1)
    problem = f"y切片が{frac_str(b)}で、点({x1},{y1})を通る一次関数の式を求めよ。"
    answer = format_linear(a,b)
    
    return problem, answer

#タイプG　増加量と1点から式を決定
def generate_type_g():
  #xの増加量とyの増加量を0以外から決定
    delta_y = non_zero_int(-5,5)
    delta_x = non_zero_int(1,5)
  #傾き計算
    a = Fraction(delta_y, delta_x)
  #1点決定
    x1, y1 = random.randint(-5,5), random.randint(-5,5)
  #切片計算
    b = Fraction(y1) - a*Fraction(x1)
  #yの増加量によって表記を調整
    if delta_y > 0:
     problem = f"xが{delta_x}増加するとyが{delta_y}増加し、点({x1},{y1})を通る一次関数の式を求めよ。"
    else:
     problem = f"xが{delta_x}増加するとyが{abs(delta_y)}減少し、点({x1},{y1})を通る一次関数の式を求めよ。"

    answer = format_linear(a,b)
    return problem, answer

#タイプH タイプAの文章形式タイプ
def generate_type_h():
  #傾き0にならないように
    while True:
        x1, y1 = random.randint(-5,5), random.randint(-5,5)
        x2, y2 = random.randint(-5,5), random.randint(-5,5)
        if x1 != x2 and y1 != y2:
            break
  #傾き計算
    a = Fraction(y2 - y1, x2 - x1)#分数を生成 Fraction(a,b)でa/b
    if a == 0:#傾き0になってしまったら再設定 
      a = Fraction(non_zero_int(-5,5),1)
  #切片計算
    b = Fraction(y1) - a * Fraction(x1)
    if b == 0: 
      b = Fraction(non_zero_int(-5,5),1)

    problem = f"x={x1}のときy={y1}、x={x2}のときy={y2}となる一次関数の式を求めよ。"
    answer = format_linear(a,b)
    
    return problem, answer

#タイプI　タイプBの文章形式
def generate_type_i():
  #0以外の数字で傾き・切片を決定
    a = Fraction(non_zero_int(-5,5),1)
    b = Fraction(non_zero_int(-5,5),1)

    problem = f"傾きが{frac_str(a)}、y切片が{frac_str(b)}の一次関数の式を求めよ。"
    answer = format_linear(a,b)
    
    return problem, answer

#タイプJ　タイプCの文章形式
def generate_type_j():
  #0以外の数字で変化の割合を決定
    a = Fraction(non_zero_int(-5,5),1)
  #1点決定
    x1, y1 = random.randint(-5,5), random.randint(-5,5)
  #切片計算
    b = Fraction(y1) - a*Fraction(x1)

  #切片が0になったら再設定
    if b == 0:
      b = Fraction(non_zero_int(-5,5),1)

    problem = f"変化の割合が{frac_str(a)}で、x={x1}のときy={y1}となる一次関数の式を求めよ。"
    answer = format_linear(a,b)
    
    return problem, answer
  
#タイプK　タイプDの文章形式
def generate_type_k():
  #0以外の数字で傾きを決定
    a = Fraction(non_zero_int(-5,5),1)
  #1点決定
    x1, y1 = random.randint(-5,5), random.randint(-5,5)
  #切片計算
    b = Fraction(y1) - a*Fraction(x1)

  #切片0になったら製設定
    if b == 0:
      b = Fraction(non_zero_int(-5,5),1)
    problem = f"傾きが{frac_str(a)}で、x={x1}のときy={y1}となる一次関数の式を求めよ。"
    answer = format_linear(a,b)
    
    return problem, answer

#タイプL　タイプEの文章形式
def generate_type_l():
  #問題の式の傾き決定
    a1 = Fraction(non_zero_int(-5,5),1)
    a2 = a1  #平行のため傾き等しい
  #1点決定
    x1, y1 = random.randint(-5,5), random.randint(-5,5)
  #切片計算
    b = Fraction(y1) - a2*Fraction(x1)
  #切片0になったら再設定
    if b == 0:
      b = Fraction(non_zero_int(-5,5),1)
    problem = f"y={frac_str(a1)}x+{frac_str(non_zero_int(-5,5))}に平行で、x={x1}のときy={y1}となる一次関数の式を求めよ。"
    answer = format_linear(a2,b)
    
    return problem, answer

#タイプM　タイプFの文章形式
def generate_type_m():
  #0以外で切片決定
    b = Fraction(non_zero_int(-5,5),1)
  #1点決定
    x1, y1 = random.randint(-5,5), random.randint(-5,5)
  #傾き計算
    a = Fraction(y1) - b
    if a == 0: 
      a = Fraction(non_zero_int(-5,5),1)
    problem = f"y切片が{frac_str(b)}で、x={x1}のときy={y1}となる一次関数の式を求めよ。"
    answer = format_linear(a,b)
    
    return problem, answer

#タイプN　タイプGの文章形式
def generate_type_n():
  #xの増加量とyの増加量を0以外から決定
    delta_y = non_zero_int(-5,5)
    delta_x = non_zero_int(1,5)
  #傾き計算
    a = Fraction(delta_y, delta_x)
  #1点決定
    x1, y1 = random.randint(-5,5), random.randint(-5,5)
  #切片計算
    b = Fraction(y1) - a*Fraction(x1)
  # yの増加量によって表記を調整
    if delta_y > 0:
        problem = f"xが{delta_x}増加するとyが{delta_y}増加し、x={x1}のときy={y1}となる一次関数の式を求めよ。"
    else:
        problem = f"xが{delta_x}増加するとyが{abs(delta_y)}減少し、x={x1}のときy={y1}となる一次関数の式を求めよ。"

    answer = format_linear(a, b)
    return problem, answer
  
#タイプO　直線の式と垂直と1点から式を決定
def generate_type_o():
  #問題の式の傾き決定
    a1 = Fraction(non_zero_int(-5,5),1)
    a2 = -Fraction(1,a1)  #垂直のため傾き傾きの－
  #1点決定
    x1, y1 = random.randint(-5,5), random.randint(-5,5)
  #切片計算
    b = Fraction(y1) - a2*Fraction(x1)
  #切片0になったら再設定
    if b == 0:
      b = Fraction(non_zero_int(-5,5),1)
    problem = f"y={frac_str(a1)}x+{frac_str(non_zero_int(-5,5))}に垂直で、点({x1},{y1})を通る一次関数の式を求めよ。"
    answer = format_linear(a2,b)
    
    return problem, answer

#タイプP　タイプOの文章形式
def generate_type_p():
  #問題の式の傾き決定
    a1 = Fraction(non_zero_int(-5,5),1)
    a2 = -Fraction(1,a1)  #垂直のため傾き傾きの－
  #1点決定
    x1, y1 = random.randint(-5,5), random.randint(-5,5)
  #切片計算
    b = Fraction(y1) - a2*Fraction(x1)
  #切片0になったら再設定
    if b == 0:
      b = Fraction(non_zero_int(-5,5),1)
    problem = f"y={frac_str(a1)}x+{frac_str(non_zero_int(-5,5))}に垂直で、x={x1}のときy={y1}となる一次関数の式を求めよ。"
    answer = format_linear(a2,b)
    
    return problem, answer

# ========== 問題生成関数群 ==========
generators = [
    generate_type_a, generate_type_b, generate_type_c, generate_type_d,
    generate_type_e, generate_type_f, generate_type_g,
    generate_type_h, generate_type_i, generate_type_j, generate_type_k,
    generate_type_l, generate_type_m, generate_type_n,generate_type_o,
    generate_type_p
]

def generate_problems_and_answers(n=20):
    problems = []
    for _ in range(n):
        gen = random.choice(generators)
        p, a = gen()
        problems.append({"problem": p, "answer": a})
    return problems

# --- API ---
@app.get("/generate")
def generate_api(n: int = 20):
    global current_problems
    current_problems = generate_problems_and_answers(n)  # 保存
    return JSONResponse(content=current_problems)

@app.get("/pdf")
def save_pdf_combined(filename="linear_combined.pdf"):
    global current_problems
    if not current_problems:
        return JSONResponse(content={"error": "先に問題を生成してください"}, status_code=400)

    c = canvas.Canvas(filename, pagesize=A4)
    width, height = A4
    c.setFont("HeiseiMin-W3", 12)

    # --- 問題ページ ---
    c.drawCentredString(width/2, height-40, "一次関数プリント（問題）")
    y = height - 80
    for i, item in enumerate(current_problems):
        c.drawString(50, y, f"{i+1}. {item['problem']}")
        y -= 25
        if y < 50:
            c.showPage()
            c.setFont("HeiseiMin-W3", 12)
            y = height - 50

    # --- 解答ページ ---
    c.showPage()
    c.setFont("HeiseiMin-W3", 12)
    c.drawCentredString(width/2, height-40, "一次関数プリント（解答）")
    y = height - 80
    for i, item in enumerate(current_problems):
        c.drawString(50, y, f"{i+1}. {item['answer']}")
        y -= 25
        if y < 50:
            c.showPage()
            c.setFont("HeiseiMin-W3", 12)
            y = height - 50

    c.save()
    return FileResponse(filename, media_type='application/pdf', filename=filename)

# ---------------------
# HTMLルート
# ---------------------
@app.get("/", response_class=HTMLResponse)
async def index():
    return """
    <!DOCTYPE html>
    <html>
    <head>
      <meta charset="UTF-8">
      <title>一次関数プリント生成</title>
      <style>
        body { font-family: sans-serif; margin: 20px; }
        button { margin: 5px; }
        pre { background: #f0f0f0; padding: 10px; }
      </style>
    </head>
    <body>
      <h1>一次関数プリント生成</h1>
      <label>問題数: <input type="number" id="num" value="20" min="1" max="100"></label><br>
      <button id="generateBtn">問題生成</button>
      <button id="pdfBtn">PDF作成</button>
      <h2>生成された問題（プレビュー）</h2>
      <pre id="preview"></pre>

      <script>
        const generateBtn = document.getElementById('generateBtn');
        const pdfBtn = document.getElementById('pdfBtn');
        const preview = document.getElementById('preview');
        const numInput = document.getElementById('num');

        generateBtn.addEventListener('click', async () => {
          const n = numInput.value;
          const res = await fetch(`/generate?n=${n}`);
          const data = await res.json();
          let text = "";
          data.forEach((p, i) => {
            text += (i+1) + ". " + p.problem + "\\n";
          });
          preview.textContent = text;
        });

        pdfBtn.addEventListener('click', () => {
          const n = numInput.value;
          window.open(`/pdf?n=${n}`, '_blank');
        });
      </script>
    </body>
    </html>
    """
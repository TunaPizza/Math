from fastapi import FastAPI, Query
from fastapi.responses import FileResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles

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

# ===== 静的ファイル用ディレクトリ（必要に応じて） =====
app.mount("/static", StaticFiles(directory="static"), name="static")

# ===== ここに一次関数問題生成関数群 =====
def non_zero_int(a, b):
    n = 0
    while n == 0:
        n = random.randint(a, b)
    return n

def frac_str(f):
    if f.denominator == 1:
        return str(f.numerator)
    return f"{f.numerator}/{f.denominator}"

def format_linear(a, b):
    if a == 1:
        a_str = "x"
    elif a == -1:
        a_str = "-x"
    else:
        a_str = f"{frac_str(a)}x"
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

def generate_problems_and_answers(n=10):
    problems = []
    for _ in range(n):
        gen = random.choice(generators)
        p, a = gen()
        problems.append((p, a))
    return problems

def save_pdf_combined(problems, filename="linear_combined.pdf"):
    c = canvas.Canvas(filename, pagesize=A4)
    width, height = A4
    c.setFont("HeiseiMin-W3", 12)

    # 問題ページ
    c.drawCentredString(width/2, height-40, "一次関数プリント（問題）")
    y = height - 80
    for i, (p, _) in enumerate(problems):
        c.drawString(50, y, f"{i+1}. {p}")
        y -= 25
        if y < 50:
            c.showPage()
            c.setFont("HeiseiMin-W3", 12)
            y = height - 50

    # 解答ページ
    c.showPage()
    c.setFont("HeiseiMin-W3", 12)
    c.drawCentredString(width/2, height-40, "一次関数プリント（解答）")
    y = height - 80
    for i, (_, a) in enumerate(problems):
        c.drawString(50, y, f"{i+1}. {a}")
        y -= 25
        if y < 50:
            c.showPage()
            c.setFont("HeiseiMin-W3", 12)
            y = height - 50

    c.save()


# ===== FastAPI ルート =====
@app.get("/", response_class=HTMLResponse)
async def index():
    return """
    <html>
    <head><title>一次関数プリント生成</title></head>
    <body>
      <h1>一次関数プリント生成</h1>
      <form action="/generate_pdf">
        <label>問題数: <input type="number" name="num" value="10" min="1" max="50"></label>
        <button type="submit">PDF生成</button>
      </form>
    </body>
    </html>
    """

@app.get("/generate_pdf")
async def generate_pdf(num: int = Query(10, ge=1, le=50)):
    problems = generate_problems_and_answers(num)
    filename = "linear_combined.pdf"
    save_pdf_combined(problems, filename)
    return FileResponse(filename, media_type="application/pdf", filename=filename)

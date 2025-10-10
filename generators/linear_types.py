from fractions import Fraction
import random
from utils import non_zero_int, frac_str, format_linear

# ----- 各タイプの問題関数 -----
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
    b0 = Fraction(non_zero_int(-5,5))
  #切片0になったら再設定
    if b == 0:
      b = Fraction(non_zero_int(-5,5),1)

    line0 = format_linear(a1,b0)
    problem = f"{line0}に平行で、点({x1},{y1})を通る一次関数の式を求めよ。"
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
    b0 = Fraction(non_zero_int(-5,5))
  #切片0になったら再設定
    if b == 0:
      b = Fraction(non_zero_int(-5,5),1)
    
    line0 = format_linear(a1,b0)

    problem = f"{line0}に平行で、x={x1}のときy={y1}となる一次関数の式を求めよ。"
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
    b0  = Fraction(non_zero_int(-5,5))
  #切片0になったら再設定
    if b == 0:
      b = Fraction(non_zero_int(-5,5),1)
    
    line0 = format_linear(a1,b0)
    problem = f"{line0}に垂直で、点({x1},{y1})を通る一次関数の式を求めよ。"
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
    b0 = Fraction(non_zero_int(-5,5))
  #切片0になったら再設定
    if b == 0:
      b = Fraction(non_zero_int(-5,5),1)

    line0 = format_linear(a1,b0)
    problem = f"{line0}に垂直で、x={x1}のときy={y1}となる一次関数の式を求めよ。"
    answer = format_linear(a2,b)
    
    return problem, answer

def generate_type_q():
  #問題の式の切片決定
    b1 = Fraction(non_zero_int(-5,5),1)
    b2 = b1
  #1点決定
    x1, y1 = random.randint(-5,5), random.randint(-5,5)
  #傾き計算
    a2 = Fraction(y1) - b1 
    a1 = Fraction(non_zero_int(-5,5),1)

    line1 = format_linear(a1,b1)

    problem = f"{line1}とy軸上で交わり、点({x1},{y1})を通る一次関数の式を求めよ。"
    answer = format_linear(a2,b2)
    
    return problem, answer

def generate_type_r():
  #問題の式の切片決定
    b1 = Fraction(non_zero_int(-5,5),1)
    b2 = b1
  #1点決定
    x1, y1 = random.randint(-5,5), random.randint(-5,5)
  #傾き計算
    a2 = Fraction(y1) - b1 
    a1 = Fraction(non_zero_int(-5,5),1)
    
    line1 = format_linear(a1,b1)

    problem = f"{line1}とy軸上で交わり、x={x1}のときy={y1}となる一次関数の式を求めよ。"
    answer = format_linear(a2,b2)
    
    return problem, answer

#タイプS　x軸上で交わる直線の式の求め方
def generate_type_s():
    # 元の直線の傾きを決定
    a0 = Fraction(non_zero_int(-5,5), 1)
    a1 = Fraction(non_zero_int(-5,5), 1)

    b0 = Fraction(non_zero_int(-5,5), 1)
    b1 = Fraction(non_zero_int(-5,5), 1)

    Aa = a0
    temx = -b1 / a1
    Ab = -a1 * temx

    line0 = format_linear(a0, b0)
    line1 = format_linear(a1, b1)

    problem = f"{line0}平行で、直線{line1}とx軸と交わる一次関数の式を求めよ。"
    answer = format_linear(Aa, Ab)
    
    return problem, answer

generators_linear = [
    generate_type_a, generate_type_b, generate_type_c, generate_type_d,
    generate_type_e, generate_type_f, generate_type_g,
    generate_type_h, generate_type_i, generate_type_j, generate_type_k,
    generate_type_l, generate_type_m, generate_type_n,generate_type_o,
    generate_type_p, generate_type_q, generate_type_r,generate_type_s
]
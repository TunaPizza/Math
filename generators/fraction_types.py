from fractions import Fraction
import random
from utils import frac_str

def generate_type_frac():
    # 分子・分母をランダムに生成（分母は2以上）
    a1 = random.randint(1, 9)
    b1 = random.randint(2, 9)
    a2 = random.randint(1, 9)
    b2 = random.randint(2, 9)

    # Fractionオブジェクトに変換
    f1 = Fraction(a1, b1)
    f2 = Fraction(a2, b2)

    # 計算方法をランダムに選ぶ
    op = random.choice(["+", "-", "×", "÷"])

    if op == "+":
        result = f1 + f2
    elif op == "-":
        result = f1 - f2
    elif op == "×":
        result = f1 * f2
    elif op == "÷":
        result = f1 / f2

    # 問題文
    problem = f"{a1}/{b1} {op} {a2}/{b2} ="

    # 答えを文字列化（整数なら分母を表示せず、分数なら約分済み）
    if result.denominator == 1:
        answer = str(result.numerator)
    else:
        answer = f"{result.numerator}/{result.denominator}"

    return problem, answer

generators_fraction = [
    generate_type_frac
]
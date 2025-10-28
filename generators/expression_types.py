from fractions import Fraction
import random
from utils import non_zero_int

def generate_expression():
    num = random.randint(2, 4)
    numbers = [non_zero_int(-9,9) for _ in range(num)]
    op = random.choices(["+", "-", "*", "/"], k = num-1)
    expr_parts = []
    for i in range(num - 1):
        expr_parts.append(f"({numbers[i]})")
        expr_parts.append(op[i])
    expr_parts.append(str(numbers[-1])")
    expr = " ".join(expr_parts)
    
    # 括弧をランダムに1組追加（50%の確率）
    if num >= 3 and random.random() < 0.5:
        i = random.randint(0, num - 2)
        expr_parts[i * 2] = "(" + expr_parts[i * 2]
        expr_parts[i * 2 + 2] = expr_parts[i * 2 + 2] + ")"
        expr = " ".join(expr_parts)
    
    # 結果の計算
    try:
        answer = eval(expr)
        answer = round(answer, 2)  # 小数第2位まで
    except ZeroDivisionError:
        return generate_expression()  # 0除算の場合は再生成
    
    # 表示用に × ÷ に置換
    problem = expr.replace("*", "×").replace("/", "÷")
    
    return problem, answer

generators_expression = [
    generate_expression
]
 
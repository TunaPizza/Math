from fractions import Fraction
import random
from utils import non_zero_int, format_expression_parts

def generate_expression():
    num = random.randint(2, 4)
    numbers = [non_zero_int(-9, 9) for _ in range(num)]
    ops = random.choices(["+", "-", "*", "/"], k=num - 1)

    # --- フォーマットを統一 ---
    expr_parts = format_expression_parts(numbers, ops)

    # --- ランダムで括弧を1組だけ追加 ---
    if num >= 3 and random.random() < 0.5:
        i = random.randint(0, num - 2)
        expr_parts[i * 2] = "(" + expr_parts[i * 2]
        expr_parts[i * 2 + 2] = expr_parts[i * 2 + 2] + ")"

    expr = " ".join(expr_parts)

    try:
        answer = eval(expr)
        answer = Fraction(answer_value).limit_denominator()
    except ZeroDivisionError:
        return generate_expression()

    problem = expr.replace("*", "×").replace("/", "÷")

    return problem, answer


generators_expression = [
    generate_expression
    ]

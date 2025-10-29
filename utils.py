import random
from fractions import Fraction

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

#問題の表記を整え
def format_expression_parts(numbers, ops):
    expr_parts = []

    for i in range(len(ops)):
        left = str(numbers[i])
        right = str(numbers[i + 1])
        op = ops[i]

        # 右側が負の数の場合だけカッコで囲む
        if numbers[i + 1] < 0:
            right = f"({right})"

        expr_parts.append(left)
        expr_parts.append(op)
        expr_parts.append(right)

    # 重複追加防止のために最初の数字と演算子部分を整理
    result = [str(numbers[0])]
    for i in range(len(ops)):
        op = ops[i]
        right = str(numbers[i + 1])
        if numbers[i + 1] < 0:
            right = f"({right})"
        result.extend([op, right])

    return result

def format_algebra_expression(coef, var, const=0):
    if coef == 0:
        expr = ""
    elif coef == 1:
        expr = var
    elif coef == -1:
        expr = f"-{var}"
    else:
        expr = f"{coef}{var}"

    # --- 定数部分 ---
    if const > 0:
        if expr:
            expr += f" + {const}"
        else:
            expr = f"{const}"
    elif const < 0:
        if expr:
            expr += f" - {abs(const)}"
        else:
            expr = f"-{abs(const)}"
    elif coef == 0:
        expr = "0"

    return expr

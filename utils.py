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
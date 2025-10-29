from fractions import Fraction
import random
from utils import non_zero_int,format_algebra_expression

def type1():
    var = random.choice(["x", "a"])
    coef1 = non_zero_int(-5, 5)
    coef2 = non_zero_int(-5, 5)
    const1 = non_zero_int(-5, 5)
    const2 = non_zero_int(-5, 5)

    problem = f"{coef1}{var} + {coef2}{var} + {const1} + {const2}"
    answer_coef = coef1 + coef2
    answer_const = const1 + const2
    answer = format_algebra_expression(answer_coef, var, answer_const)

    return problem, answer

def type2():
    var = random.choice(["x", "a"])
    k = non_zero_int(-5, 5)
    c1, n1 = non_zero_int(-5, 5), non_zero_int(-5, 5)

    problem = f"{k}({c1}{var} + {n1})"
    answer = format_algebra_expression(k * c1, var, k * n1)
    return problem, answer

def type3():
    var = random.choice(["x", "a"])
    c1, c2 = non_zero_int(-5, 5), non_zero_int(-5, 5)
    n1, n2 = non_zero_int(-5, 5), non_zero_int(-5, 5)

    problem = f"({c1}{var} + {n1}) - ({c2}{var} + {n2})"
    answer = format_algebra_expression(c1 - c2, var, n1 - n2)
    return problem, answer

def type4():
    var = random.choice(["x", "a"])
    c1, c2 = non_zero_int(-5, 5), non_zero_int(-5, 5)
    n1, n2 = non_zero_int(-5, 5), non_zero_int(-5, 5)

    problem = f"({c1}{var} + {n1}) + ({c2}{var} + {n2})"
    answer = format_algebra_expression(c1 + c2, var, n1 + n2)
    return problem, answer

generators_algebra = [
    type1,type2,type3,type4
]
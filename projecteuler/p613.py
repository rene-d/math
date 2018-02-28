"""
Pythagorean Ant

https://projecteuler.net/problem=613
"""

from scipy.integrate import dblquad
from math import pi, atan2


def p(y, x):
    return (pi / 2 + atan2(y, 4 - x) + atan2(x, 3 - y)) / (2 * pi)


res = dblquad(p, 0, 4, lambda x: 0, lambda x: 3 - 3 * x / 4)
print(round(res[0] / (3 * 4 / 2), 10))

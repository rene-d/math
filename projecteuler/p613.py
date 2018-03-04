"""
Pythagorean Ant

https://projecteuler.net/problem=613
"""

from scipy.integrate import dblquad
from math import pi, atan2


"""
 A
 |\
 | \            ①   calcule de l'angle α de (AXB) en fonction des coordonnées de X
 |  \                la probabilité de sortie par AB est p(x,y)/2π si la fourmi est en X
 |   \
 |    \         ②   1/S ∬ p(x,y) dxdy sur l'aire S du triangle x=0..4 et y=3*(1-x/4)
 |     \             donnera la probabilité de sortie par AB quelque soit la position
 |  X   \
 |       \      ③   Wolfram Alpha est impressionnant, mais SciPy aussi 😃
 ----------
C          B
"""


def p(y, x):
    return (pi / 2 + atan2(y, 4 - x) + atan2(x, 3 - y)) / (2 * pi)


res = dblquad(p, 0, 4, lambda x: 0, lambda x: 3 - 3 * x / 4)
print(round(res[0] / (3 * 4 / 2), 10))

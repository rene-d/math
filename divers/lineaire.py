#!/usr/bin/env python3

from fractions import Fraction

a = input("point A ? ")
x1, y1 = map(int, a.split())

a = input("point B ? ")
x2, y2 = map(int, a.split())


a = Fraction(y1 - y2, x1 - x2)
b = y1 - x1 * a

print(f"Equation de la droite y=a𝑥+b :  y = {a} 𝑥 + {b}")
print(f"a = {a}")
print(f"b = {b}")

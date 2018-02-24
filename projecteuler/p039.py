"""
Integer right triangles

If p is the perimeter of a right angle triangle with integral length sides, {a,b,c}, there are
exactly three solutions for p = 120.

{20,48,52}, {24,45,51}, {30,40,50}

For which value of p ≤ 1000, is the number of solutions maximised?

https://projecteuler.net/problem=39
"""

import math

pmax = 0
nbmax = 0
for p in range(1, 1001):
    nb = 0
    # TODO: à optimiser
    for a in range(1, p // 3):
        for b in range(a + 1, 2 * p // 3):
            c = int(math.sqrt(a * a + b * b))
            if p == a + b + c and a * a + b * b == c * c:
                # print("solution pour p={:4d}  a={:4d} b={:4d} c={:4d} {:4d} {:4d}"
                # .format(p,a,b,c,a*a+b*b-c*c,a+b+c))
                nb += 1
    if nb > nbmax:
        pmax = p
        nbmax = nb
print(pmax)
print(nbmax)

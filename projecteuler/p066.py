"""
Diophantine equation

https://projecteuler.net/problem=66
"""


from math import sqrt
from fractions import Fraction


# Quelques liens...

# https://oeis.org/A033313
# Smallest positive integer x satisfying the Pell equation x^2 - D*y^2 = 1
# for nonsquare D and positive y.

# Calcul de la fraction continue de √S
# https://en.wikipedia.org/wiki/Methods_of_computing_square_roots#Continued_fraction_expansion

# Algo de résolution de l'équation de Pell
# http://mathworld.wolfram.com/PellEquation.html


def CFE(S):
    """
    """
    vS = int(sqrt(S))
    a = [vS]
    if vS ** 2 == S:
        return a

    m0 = 0
    d0 = 1
    a0 = vS

    while True:
        m1 = d0 * a0 - m0
        d1 = (S - m1 ** 2) // d0
        a1 = (vS + m1) // d1
        a.append(a1)
        if a1 == 2 * vS:
            break
        m0, d0, a0 = m1, d1, a1

    return a


def fraction_continue(f, a, i):
    ai = a[0] if i == 0 else a[1 + (i - 1) % (len(a) - 1)]
    if f == 0:
        return Fraction(ai)
    return ai + 1 / f


def pell(d):
    if int(sqrt(d)) ** 2 == d:
        return 0, 0

    a = CFE(d)
    n = len(a) - 1    # longueur du motif
    k = n if n % 2 == 0 else 2 * n
    f = Fraction(0)

    while k > 0:
        k -= 1
        f = fraction_continue(f, a, k)

    x = f.numerator
    y = f.denominator
    # print(d, "OK" if x * x - d * y * y == 1 else "ERREUR", f, round((x / y) ** 2, 6), a)
    return x, y


xmax, dmax = 0, 0
for d in range(2, 1001):
    x = pell(d)[0]
    if x > xmax:
        xmax, dmax = x, d
print(dmax)

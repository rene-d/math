"""
Odd period square roots

https://projecteuler.net/problem=64
"""

from math import sqrt


def CFE(S):
    """
    https://en.wikipedia.org/wiki/Methods_of_computing_square_roots#Continued_fraction_expansion
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


print(sum([1 - len(CFE(i)) % 2 for i in range(1, 10001)]))

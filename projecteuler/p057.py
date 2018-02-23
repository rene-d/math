"""
Square root convergents

https://projecteuler.net/problem=57
"""

from fractions import Fraction


def fraction_continue(f):
    """ fraction continue de √2 """
    return 1 + 1 / (1 + f)


resultat = 0
f = Fraction(1)
for i in range(1000):
    f = fraction_continue(f)
    if len(str(f.numerator)) > len(str(f.denominator)):
        resultat += 1
print(resultat)

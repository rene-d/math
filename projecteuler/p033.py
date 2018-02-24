"""
Digit cancelling fractions

https://projecteuler.net/problem=33
"""

from fractions import Fraction
from math import gcd

resultat = Fraction(1)

for d in range(11, 100):
    for n in range(10, d):

        # fraction irréductible
        if gcd(n, d) == 1:
            continue

        # cas triviaux
        if n % 10 == 0 and d % 10 == 0:
            continue

        # si les chiffres des unités du numérateur et dénominateur sont identiques
        if n % 10 == d % 10:
            # on utile le chiffre des dizaines
            f = Fraction(n // 10, d // 10)

        # etc.
        elif n % 10 == d // 10 and d % 10 != 0:
            f = Fraction(n // 10, d % 10)

        elif n // 10 == d % 10:
            f = Fraction(n % 10, d // 10)

        elif n // 10 == d // 10 and d % 10 != 0:
            f = Fraction(n % 10, d % 10)

        else:
            continue

        # est-on est dans le cas de réduction de l'énoncé ?
        if f == Fraction(n, d):
            resultat *= f

print(resultat.denominator)

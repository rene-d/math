"""
Diophantine equation

https://projecteuler.net/problem=66
"""

from eulerlib import Fraction

"""
https://fr.wikipedia.org/wiki/Fraction_continue_d%27un_irrationnel_quadratique
https://fr.wikipedia.org/wiki/Équation_de_Pell-Fermat
"""


def fraction_continue(f):
    """ fraction continue de √2 """
    return 1 + 1 / (1 + f)


resultat = 0
f = Fraction(1)
for i in range(1000):
    f = fraction_continue(f)
    if len(str(f.num)) > len(str(f.den)):
        resultat += 1
print(resultat)

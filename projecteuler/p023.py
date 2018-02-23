"""
Non-abundant sums

https://projecteuler.net/problem=23
"""

from eulerlib import diviseurs
import itertools


L = 28123

abondants = []
for i in range(12, L):
    d = diviseurs(i)        # tous les diviseurs de i, y compris 1 et i
    s = sum(d[0:-1])        # tous les diviseurs sauf i
    if s > i:
        abondants.append(i)

pas_une_somme = [True] * L
for i, j in itertools.combinations_with_replacement(abondants, 2):
    if i + j < L:
        pas_une_somme[i + j] = False

print(sum([i for i, ok in enumerate(pas_une_somme) if ok]))

"""
Distinct primes factors

https://projecteuler.net/problem=47
"""

from eulerlib import decompose

consecutif = 4
liste_facteurs = []

for i in range(2, 1000000):

    facteurs = [f[0] for f in decompose(i)]

    if len(facteurs) != consecutif:
        liste_facteurs.clear()
        continue

    liste_facteurs.append(facteurs)

    if len(liste_facteurs) >= consecutif:
        print(i - len(liste_facteurs))
        break

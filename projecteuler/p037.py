"""
Truncatable primes

The number 3797 has an interesting property. Being prime itself, it is possible to continuously
remove digits from left to right, and remain prime at each stage: 3797, 797, 97, and 7. Similarly
we can work from right to left: 3797, 379, 37, and 3.

Find the sum of the only eleven primes that are both truncatable from left to right and right to
left.

NOTE: 2, 3, 5, and 7 are not considered to be truncatable primes.

https://projecteuler.net/problem=37
"""

from eulerlib import Crible

crible = Crible(1000000)

nb = 0
somme = 0
for p in crible.liste():

    if p < 10:
        continue

    ko = False

    gauche = p
    droite = 0
    i = 0
    while gauche >= 10 and not ko:

        gauche, r = divmod(gauche, 10)
        #print("x",gauche)
        if not crible.est_premier(gauche):
            ko = True

        droite = droite + r * 10 ** i
        #print("y",droite)
        if not crible.est_premier(droite):
            ko = True

        i += 1

    if not ko:
        nb += 1
        somme += p
        # print(nb, p)
        if nb == 11:
            # print("fin")
            break

print(somme)
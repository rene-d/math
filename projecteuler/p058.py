"""
Spiral primes

https://projecteuler.net/problem=58
"""

from eulerlib import est_premier


nb_premiers = 0
n = 1
i = 0
while True:
    i += 1

    for _ in range(4):
        n += i * 2
        if est_premier(n):
            nb_premiers += 1

    # largeur du carré: 2i+1
    # nombre de nombres sur les diagonales: 4i+1
    if 4 * i + 1 > 10 * nb_premiers:
        print(2 * i + 1)
        break

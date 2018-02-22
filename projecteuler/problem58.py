"""
Spiral primes

https://projecteuler.net/problem=58
"""

from premiers.liste_premiers import est_premier

"""
Spirale d'Ulam
réponse: 26241
"""

x = y = n = 0
nb_diagonales = 0


def ligne(i, dx, dy):
    global n, x, y, nb_diagonales
    for _ in range(i):
        n = n + 1
        if abs(x) == abs(y):        # on est sur une diagonale
            if est_premier(n):
                nb_diagonales += 1
        x += dx
        y += dy


i = 1
while i < 100000:
    ligne(i, 1, 0)
    ligne(i, 0, -1)
    i += 1
    ligne(i, -1, 0)
    ligne(i, 0, 1)
    i += 1

    # nombre de points de diagonales: 2i+1
    if 2 * i - 1 > 10 * nb_diagonales:
        print(i)
        break

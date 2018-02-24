"""
Reciprocal cycles

https://projecteuler.net/problem=26
"""

from eulerlib import pgcd

# https://fr.wikipedia.org/wiki/Développement_décimal_périodique#Longueur_de_la_période
# Si n est premier avec 10, la longueur de la période est égale à l'ordre multiplicatif de
#  10 modulo n.

# https://fr.wikipedia.org/wiki/Ordre_multiplicatif
# l'ordre multiplicatif, modulo un entier naturel n, d'un entier relatif a premier à n,
# est le plus petit entier k > 0 tel que a^k ≡ 1 (modulo n).


def ord10(n):

    # n doit être premier avec 10
    if pgcd(n, 10) != 1:
        return 0

    k = 1
    a = 10
    while True:
        if (a ** k) % n == 1:
            break
        k += 1
    return k


print(max((ord10(i), i) for i in range(3, 1000))[1])

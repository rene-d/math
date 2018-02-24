"""
Champernowne's constant

https://projecteuler.net/problem=40
"""


def d(n):
    """ retourne le n-ième chiffre de la constante de Champernowne """

    if n < 1:
        raise ValueError

    nc = 1  # nombre de chiffres de la zone actuelle
    while n > 9 * (10 ** (nc - 1)) * nc:
        n -= 9 * (10 ** (nc - 1)) * nc
        nc += 1

    q, r = divmod(n - 1, nc)
    # q = nombre de la zone actuelle (à 1... près)
    # r = n° du chiffre dans le nombre (0 = celui de gauche)
    for _ in range(nc - 1 - r):
        q //= 10
    if r == 0:
        return q + 1
    else:
        return q % 10


def test_champernowne():
    """ vérification rapide avec une construction triviale de la constante """
    dd = ['.']
    i = 1
    while len(dd) < 10000:
        dd.extend([int(c) for c in str(i)])
        i += 1
    for i in range(1, 10000):
        assert dd[i] == d(i)


test_champernowne()
resultat = 1
for i in range(7):
    resultat *= d(10 ** i)
print(resultat)

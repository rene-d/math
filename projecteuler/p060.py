"""
Prime pair sets

The primes 3, 7, 109, and 673, are quite remarkable. By taking any two primes and concatenating
them in any order the result will always be prime. For example, taking 7 and 109, both 7109 and
1097 are prime. The sum of these four primes, 792, represents the lowest sum for a set of four
primes with this property.

Find the lowest sum for a set of five primes for which any two primes concatenate to produce
another prime.

https://projecteuler.net/problem=60
"""

from eulerlib import Crible

crible = Crible(10000)
premiers = crible.liste()


def cherche(start, level=4, nb=[]):

    if level == 0:
        # on a trouvé suffisamment de nombres
        print(sum(nb))
        print(nb)
        return True

    # cherche un nouveau premier...
    for i, p in enumerate(premiers[start:], start=start):

        # ... qui peut compléter la liste passée en paramètre
        # en respectant les critères de l'énoncé
        yes = True
        for q in nb:
            sp = str(p)
            sq = str(q)
            if not crible.est_premier(int(sp + sq)) or not crible.est_premier(int(sq + sp)):
                yes = False
                break

        # p convient, on continue de remplir la liste
        if yes:
            if cherche(start + 1, level - 1, nb + [p]):
                return True

    return False


cherche(1, level=5)

"""
Counting fractions

https://projecteuler.net/problem=72
"""

# https://en.wikipedia.org/wiki/Farey_sequence


def totients(n):
    """ retourne la liste des indicatrices d'Euler (ou totient) pour 2 ≤ i ≤ n """
    phi = list(range(n + 1))
    for i in range(2, n + 1):
        if phi[i] == i:     # i est premier
            for j in range(i, n + 1, i):
                phi[j] -= phi[j] // i
    return phi[2:]          # supprime 0 et 1


t = totients(1000000)
print(sum(t))

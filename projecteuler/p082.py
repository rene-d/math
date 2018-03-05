"""
Path sum: three ways

https://projecteuler.net/problem=82
"""

matrix = []
N = 0
cache = {}


def cherche(x, y, dernier=None):
    global cache

    if y >= N or x >= N or x < 0 or y < 0:
        raise

    if (x, y, dernier) in cache:
        return cache[(x, y, dernier)]

    # la méthode lecture de la matrice inverse x et y
    v = matrix[y][x]

    # est-on arrivé ?
    if x == N - 1:
        return v

    # essaie un coup à droite
    m = [cherche(x + 1, y)]

    # pas de retour en arrière: si on monte on ne doit pas descendre
    if dernier != 'B' and y > 0:
        m.append(cherche(x, y - 1, 'H'))

    # et vice-versa
    if dernier != 'H' and y < N - 1:
        m.append(cherche(x, y + 1, 'B'))

    v += min(m)

    cache[(x, y, dernier)] = v

    return v


for i in open("p082_matrix.txt"):
    ligne = [int(n) for n in i.split(",")]
    if len(ligne) > 0:
        matrix.append(ligne)
N = len(matrix)
assert N == 80

print(min([cherche(0, i) for i in range(N)]))

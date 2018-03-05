"""
Path sum: two ways

https://projecteuler.net/problem=81
"""

import functools

matrix = []
N = 0


@functools.lru_cache(maxsize=None)
def cherche(x, y):
    global N, matrix

    if y >= N or x >= N:
        return 0

    # la méthode lecture de la matrice inverse x et y
    v = matrix[y][x]

    if x == N - 1:
        # on ne peut que descendre
        v += cherche(x, y + 1)
    elif y == N - 1:
        # on ne peut qu'aller sur la droite
        v += cherche(x + 1, y)
    else:
        # il faut tester à droite ou en bas
        v += min(cherche(x + 1, y), cherche(x, y + 1))

    return v


for i in open("p081_matrix.txt"):
    ligne = [int(n) for n in i.split(",")]
    if len(ligne) > 0:
        matrix.append(ligne)

N = len(matrix)
assert N == 80
for row in matrix:
    assert len(row) == N

print(cherche(0, 0))

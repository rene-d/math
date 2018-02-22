"""
Maximum path sum II

https://projecteuler.net/problem=67
"""

triangle = []
cache = dict()


def cherche(ligne, position):
    """ fonction récursive qui retourne la somme max de l'arbre sous (ligne, position) """
    global cache

    if ligne >= len(triangle):
        return 0

    v = triangle[ligne][position]

    max = 0
    for i in range(0, 2):
        # la mise en cache des sommes sous le noeud courant évite
        # des tonnes récursions inutiles
        if (ligne + 1, position + i) in cache:
            s = cache[(ligne + 1, position + i)]
        else:
            s = cherche(ligne + 1, position + i)
            cache[(ligne + 1, position + i)] = s
        if v + s > max:
            max = v + s

    return max


for i in open("p067_triangle.txt"):
    ligne = [int(n) for n in i.split()]
    if len(ligne) > 0:
        triangle.append(ligne)

print(cherche(0, 0))

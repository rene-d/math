"""
Cyclical figurate numbers

https://projecteuler.net/problem=61
"""

from copy import deepcopy
from math import sqrt


def P(p, n):
    return (p - 2) * n * (n - 1) // 2 + n
    """
    if p == 3:
        return n * (n + 1) // 2
    elif p == 4:
        return n * n
    elif p == 5:
        return n * (3 * n - 1) // 2
    elif p == 6:
        return n * (2 * n - 1)
    elif p == 7:
        return n * (5 * n - 3) // 2
    elif p == 8:
        return n * (3 * n - 2)
    raise
    """


def P_inverse(p, n):
    i = int(sqrt(n / (p - 2) * 2))
    j = 0
    while j < 10:
        if P(p, i + j) == n:
            return i + j
        j += 1


# liste des nombres polygonaux < 10000, le degré est stocké dans un bit
polygonal = [0] * 10000
for n in range(2, 5000):
    for p in range(3, 9):
        i = P(p, n)
        if 1000 <= i < 10000:
            polygonal[i] = polygonal[i] | (1 << p)


def cherche(n, masque, liste):

    p = polygonal[n]
    if p == 0:
        return False

    # si le masque est le même, la condition d'unicité de représentation
    # ne peut plus être respectée
    if masque == masque | p:
        return False

    masque |= p
    liste.append(n)

    if len(liste) >= 6:
        if masque == 0b00111111000:
            if liste[0] // 100 == n % 100:
                print(sum(liste))
                print(liste)
                for k in liste:
                    print("  {} : {}".format(k, ''.join(
                        ["P{}({})".format(i, P_inverse(i, k)) if b == '1' else ""
                         for i, b in enumerate(reversed(bin(polygonal[k])))])))
                return True
        return False

    # on cycle
    n = (n % 100) * 100

    # et on cherche un nombre adhoc
    for j in range(n + 10, n + 100):
        if cherche(j, masque, deepcopy(liste)):
            return True

    return False

# 2512, 1281, 8128, 2882, 8256, 5625


for i in range(1010, 10000):
    if cherche(i, 0, []):
        break

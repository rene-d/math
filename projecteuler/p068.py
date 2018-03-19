"""
Magic 5-gon ring

https://projecteuler.net/problem=68
"""

import itertools


def verifie(r):
    n = r[0] + r[5] + r[9]
    if r[1] + r[6] + r[5] == n:
        if r[2] + r[7] + r[6] == n:
            if r[3] + r[8] + r[7] == n:
                if r[4] + r[9] + r[8] == n:
                    return True
    return False


def combi():
    rings = [i for i in range(1, 11)]
    for r in itertools.permutations(rings):
        if verifie(r):
            m = r.index(min(r[0:5]))

            p = []
            for i in range(m, m - 5, -1):
                i = i % 5
                p.extend([r[i], r[5 + (i + 5) % 5], r[5 + (i + 4) % 5]])

            p = ''.join(map(str, p))
            if len(p) == 16:
                yield int(p)


print(max(combi()))

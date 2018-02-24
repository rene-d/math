"""
Coin sums

https://projecteuler.net/problem=31
"""

import functools

coins = [1, 2, 5, 10, 20, 50, 100, 200]


@functools.lru_cache(maxsize=None)
def r(objectif, piece):

    nb = 0
    for i in range(piece, len(coins)):
        if objectif == coins[i]:
            nb += 1
        elif objectif > coins[i]:
            nb += r(objectif - coins[i], i)

    return nb


print(r(200, 0))

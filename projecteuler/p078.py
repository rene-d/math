"""
Coin partitions

https://projecteuler.net/problem=78
"""

import functools

# C'est exactement la partition d'un entier n
# https://fr.wikipedia.org/wiki/Partition_d%27un_entier


@functools.lru_cache(maxsize=None)
def p(n):
    if n < 0:
        return 0
    if n <= 1:
        return 1
    r = 0
    k = 1
    g = 0
    signe = 1
    while g <= n:
        g = k * (3 * k + 1) // 2
        r += signe * (p(n - g) + p(n - k * (3 * k - 1) // 2))
        signe = -signe
        k += 1
    return r


n = 5
while n < 100000:
    n += 1
    q = p(n)
    if q % 1000000 == 0:
        print(n)
        break

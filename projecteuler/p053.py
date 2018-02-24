"""
Combinatoric selections

https://projecteuler.net/problem=53
"""

import math
import functools


@functools.lru_cache(maxsize=None)
def fact(n):
    return math.factorial(n)


def C(n, k):
    """ Coefficient binomial """
    return math.factorial(n) // math.factorial(k) // math.factorial(n - k)


# itertools.combinations_with_replacement
resultat = 0
for n in range(1, 101):
    for k in range(1, n):
        if C(n, k) >= 1000000:
            resultat += 1
print(resultat)

"""
Counting summations

https://projecteuler.net/problem=76
"""

import functools

# https://en.wikipedia.org/wiki/Partition_(number_theory)
# https://en.wikipedia.org/wiki/Divisor_function


@functools.lru_cache(maxsize=None)
def sigma1(n):
    # https://oeis.org/A000203
    s = 0
    for d in range(1, n // 2 + 1):
        if n % d == 0:
            s += d
    return s + n


@functools.lru_cache(maxsize=None)
def p(n):
    # https://oeis.org/A000041
    if n <= 1:
        return 1
    return sum(sigma1(n - k) * p(k) for k in range(0, n)) // n


print(p(100) - 1)       # -1 pour enlever 0+100


# nota: la réponse est dans https://oeis.org/A000041/b000041.txt

"""
Square prime factors II

https://projecteuler.net/problem=633
"""

from functools import lru_cache
from math import pi


MAX = 1000000
primes = []
sieve = [True] * (1 + MAX)
for n in range(2, MAX + 1):
    if sieve[n]:
        primes.append(n)
        for i in range(n, MAX + 1, n):
            sieve[i] = False


@lru_cache()
def s(k):
    assert k >= 1
    return sum(1 / (p ** 2 - 1) ** k for p in primes)


zeta_2 = pi ** 2 / 6

C = [0] * 8
C[0] = 1 / zeta_2

for k in range(1, 8):
    C[k] = sum((-1) ** (i + 1) * C[k - i] * s(i) for i in range(1, k + 1)) / k
    # print("{} {:.9e} {}".format(k, C[k], s(k)))

print("{:.4e}".format(C[7]))

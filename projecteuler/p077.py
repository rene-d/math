"""
Prime summations

https://projecteuler.net/problem=77
"""

# http://oeis.org/A000607
# http://mathworld.wolfram.com/PrimePartition.html
# https://math.stackexchange.com/questions/89240/prime-partition


from eulerlib import Crible, decompose
import functools


crible = Crible(10000)


@functools.lru_cache(maxsize=None)
def sopf(n):
    return sum(p[0] for p in decompose(n))


@functools.lru_cache(maxsize=None)
def b(n):
    return (sopf(n) + sum(sopf(j) * b(n - j) for j in range(1, n))) // n


n = 1
while b(n) < 5000:
    n += 1
print(n)

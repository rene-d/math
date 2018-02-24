"""
Pandigital prime

We shall say that an n-digit number is pandigital if it makes use of all the digits 1 to n exactly
once. For example, 2143 is a 4-digit pandigital and is also prime.

What is the largest n-digit pandigital prime that exists?

https://projecteuler.net/problem=41
"""

from eulerlib import est_premier
import itertools

chiffres = "987654321"
nmax = 0


def test(chiffres):
    for perm in itertools.permutations(chiffres):
        n = int(''.join(perm))
        if est_premier(n):
            return n


m = 0
for i in range(4):
    for perm in itertools.permutations(chiffres[i:]):
        n = int(''.join(perm))
        if est_premier(n):
            m = n
            break
    if m != 0:
        break
print(m)

"""
Prime permutations

The arithmetic sequence, 1487, 4817, 8147, in which each of the terms increases by 3330,
is unusual in two ways: (i) each of the three terms are prime, and, (ii) each of the
4-digit numbers are permutations of one another.

There are no arithmetic sequences made up of three 1-, 2-, or 3-digit primes, exhibiting
this property, but there is one other 4-digit increasing sequence.

What 12-digit number do you form by concatenating the three terms in this sequence?

https://projecteuler.net/problem=49
"""

from premiers.eratosthene import Crible


crible = Crible(10000)
premiers = crible.liste()

premiers = [i for i in premiers if i >= 1000]
nb = len(premiers)

for i in range(nb - 2):
    p1 = premiers[i]

    # exclut la solution de l'énoncé
    if p1 == 1487:
        continue

    for j in range(i + 1, nb - 1):
        p2 = premiers[j]
        p3 = p2 + (p2 - p1)
        if p3 not in premiers:
            continue

        s1 = sorted(str(p1))
        s2 = sorted(str(p2))
        if s1 != s2:
            continue

        s3 = sorted(str(p3))
        if s1 != s3:
            continue

        print("%d%d%d" % (p1, p2, p3))

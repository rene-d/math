"""
Circular primes

The number, 197, is called a circular prime because all rotations of the digits:
197, 971, and 719, are themselves prime.

There are thirteen such primes below 100: 2, 3, 5, 7, 11, 13, 17, 31, 37, 71, 73, 79, and 97.

How many circular primes are there below one million?

https://projecteuler.net/problem=35
"""

from eulerlib import Crible


def rotation(n):
    nombres = []

    chiffres = 0
    q = n
    while q != 0:
        q //= 10
        chiffres += 1

    decalage = 10 ** (chiffres - 1)
    for _ in range(chiffres):
        n, r = divmod(n, 10)
        n += r * decalage
        nombres.append(n)

    return nombres


crible = Crible(1000000)

resultat = 0
for i in crible.liste():
    if all([crible.est_premier(j) for j in rotation(i)]):
        resultat += 1
print(resultat)

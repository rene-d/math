"""
10001st prime

By listing the first six prime numbers: 2, 3, 5, 7, 11, and 13, we can see that the 6th prime is 13.

What is the 10 001st prime number?

https://projecteuler.net/problem=7
"""

from eulerlib import est_premier


compte = 0
n = 1

while compte < 10001:
    n += 1
    if est_premier(n):
        compte += 1

print(n)

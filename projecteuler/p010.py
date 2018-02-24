"""
Summation of primes

The sum of the primes below 10 is 2 + 3 + 5 + 7 = 17.

Find the sum of all the primes below two million.

https://projecteuler.net/problem=10
"""

from eulerlib import Crible


MAX = 2000000

# solution avec crible
crible = Crible(MAX)
print(sum(crible.liste()))

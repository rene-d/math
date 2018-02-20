"""
Largest prime factor

The prime factors of 13195 are 5, 7, 13 and 29.

What is the largest prime factor of the number 600851475143 ?

https://projecteuler.net/problem=3
"""

from premiers.decompose import decompose


print(decompose(600851475143)[-1])

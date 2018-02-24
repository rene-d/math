"""
Digit factorials

145 is a curious number, as 1! + 4! + 5! = 1 + 24 + 120 = 145.

Find the sum of all numbers which are equal to the sum of the factorial of their digits.

Note: as 1! = 1 and 2! = 2 are not sums they are not included.

https://projecteuler.net/problem=34
"""

from math import factorial


fact = [factorial(i) for i in range(0, 10)]

resultat = 0
n = 10
while n < 100000:

    s = 0
    q = n
    while q != 0:
        q, r = divmod(q, 10)
        s += fact[r]

    if s == n:
        resultat += n

    n += 1

print(resultat)

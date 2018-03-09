"""
Prime generating integers

https://projecteuler.net/problem=357
"""

from eulerlib import Crible


crible = Crible(100000000)


def diviseurs(n):
    d = 1
    while d * d <= n:
        q, r = divmod(n, d)
        if r == 0:
            if not crible.est_premier(d + q):
                return False
        d += 1
    return True


assert diviseurs(30)

sum = 1     # pour n=1
for n in range(2, 100000000, 2):
    if diviseurs(n):
        sum += n
        print(n)
print(sum)

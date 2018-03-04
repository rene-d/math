"""
Totient maximum

https://projecteuler.net/problem=69
"""

from eulerlib import EulerPhi


rmax, nmax = 0, 0
for n in range(1, 1000001):
    r = n / EulerPhi(n)
    if r > rmax:
        rmax, nmax = r, n
print(nmax)

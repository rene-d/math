"""
Totient permutation

https://projecteuler.net/problem=70
"""

from eulerlib import EulerPhi, Crible


crible = Crible(10000000)
phi = crible.EulerPhi()

def est_permutation(a, b):
    chiffres = [0] * 10
    while a != 0:
        a, r = divmod(a, 10)
        chiffres[r] += 1
    while b != 0:
        b, r = divmod(b, 10)
        chiffres[r] -= 1
    return all(c == 0 for c in chiffres)

rmin, nmin = 10, 0
for n in range(2, 10000000):
    p = phi[n]
    r = n / p
    if r < rmin:
        if est_permutation(n, p):
            rmin, nmin = r, n
print(nmin)

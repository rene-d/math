"""
Quadratic primes

https://projecteuler.net/problem=27
"""

from eulerlib import Crible

crible = Crible(1000)
premiers = crible.liste()

premiers.extend([-i for i in premiers])

solution = 0
n_max, a_max, b_max = 0, 0, 0
for b in premiers:
    for a in range(-999, 1000):

        for n in range(0, 1000):
            p = n * n + a * n + b

            if not crible.est_premier(p):
                if n > n_max:
                    # print("nouveau max", n, a, b)
                    n_max, a_max, b_max = n, a, b
                break

print(a_max * b_max)

print("n²{:+d}n{:+d} ⇒ {} premiers".format(a_max, b_max, n_max))

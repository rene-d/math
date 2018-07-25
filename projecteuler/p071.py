"""
Ordered fractions

https://projecteuler.net/problem=71
"""

# brute force...
# on cherche la fraction < 3/7 avec le plus grand dénominateur (et donc numérateur)
# la fraction est irréductible, sinon on serait déjà mémorisée puisqu'on parcourt les
# dénominateurs de manière croissante

N = 1000000

max_n = 0
max_d = 1

for d in range(1, N + 1):

    n = (d * 3) // 7

    if n * 7 >= d * 3:          # i.e. n/d >= 3/7
        continue

    if n * max_d > d * max_n:   # i.e.  n/d > max_n/max_d
        max_n = n
        max_d = d

print(max_n)

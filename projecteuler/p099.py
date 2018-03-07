"""
Largest exponential

https://projecteuler.net/problem=99
"""

import math

i = 0
imax, fmax = 0, 0
for s in open("p099_base_exp.txt"):
    i += 1
    base, exp = s.split(',')
    base, exp = int(base), int(exp)

    # log() est strictement croissante: il suffit de trouver le max
    # de b*log(a) pour trouver le max de a^b
    f = exp * math.log(base)
    if f > fmax:
        fmax, imax = f, i
print(imax)

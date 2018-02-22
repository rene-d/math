"""

https://projecteuler.net/problem=5
"""

from eulerlib import decompose2


f = dict()
for i in range(1, 21):
    for k in decompose2(i):
        if f.get(k[0], 0) < k[1]:
            f[k[0]] = k[1]

ppcm = 1
for i, p in f.items():
    ppcm *= (i ** p)
print(ppcm)

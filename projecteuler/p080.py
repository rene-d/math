"""
Square root digital expansion

https://projecteuler.net/problem=80
"""

import mpmath as mp

mp.mp.dps = 105

r = 0
for i in range(1, 101):
    # on ne compte pas les carrés
    if int(i **0.5)**2 != i:
        continue

    j = 0
    for d in str(mp.sqrt(i)):
        if d != '.':
            r += int(d)
            j += 1
            # 100 chiffres exactement, y compris la partie entière
            if j == 100:
                break
print(r)

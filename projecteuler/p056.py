"""
Powerful digit sum

https://projecteuler.net/problem=56
"""

s = 0
for a in range(1, 100):
    for b in range(1, 100):
        s = max(s, sum([int(c) for c in str(a ** b)]))
print(s)

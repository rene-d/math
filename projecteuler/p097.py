"""
https://projecteuler.net/problem=97
"""

m = 28433

for i in range(7830457):
    m *= 2
    m %= 10000000000

m += 1
print(m)

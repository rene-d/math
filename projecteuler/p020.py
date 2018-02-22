"""
Factorial digit sum

https://projecteuler.net/problem=20
"""

f = 1
for i in range(1, 101):
    f *= i

print(sum([int(c) for c in str(f)]))

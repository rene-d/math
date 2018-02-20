"""
Sum square difference

https://projecteuler.net/problem=6
"""

N = 100
s1 = s2 = 0
for i in range(1, N + 1):
    s1 += i
    s2 += i ** 2

s1 = s1 ** 2

print(s1 - s2)

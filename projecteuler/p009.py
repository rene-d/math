"""
Special Pythagorean triplet

https://projecteuler.net/problem=9
"""

for a in range(1, 1000):
    for b in range(a + 1, 1000):
        c = 1000 - a - b
        if a * a + b * b == c * c:
            print(a * b * c)
            # print(a, b, c)

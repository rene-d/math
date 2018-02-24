"""
Triangular, pentagonal, and hexagonal

https://projecteuler.net/problem=45
"""


# Triangle
def Tn(n):
    return n * (n + 1) // 2


# Pentagonal
def Pn(n):
    return n * (3 * n - 1) // 2


# Hexagonal
def Hn(n):
    return n * (2 * n - 1)


i, j, k = 285, 165, 143 + 1

while True:
    t = Tn(i)
    p = Pn(j)
    h = Hn(k)

    if t == p and p == h:
        print(t)
        # print(i, j, k)
        break

    if t <= p and t <= h:
        i += 1
    if p <= h and p <= t:
        j += 1
    if h <= t and h <= p:
        k += 1

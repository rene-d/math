"""
Highly divisible triangular number

https://projecteuler.net/problem=12
"""


def diviseurs(n):
    div = [1]
    i = 2
    while i * i <= n:
        q, r = divmod(n, i)
        if r == 0:
            div.append(i)
            if i != q:
                div.append(q)
        i += 1
    div.append(n)
    return div


i = 0
n = 0
nd = 0
while nd < 500:
    i += 1
    n += i
    nd = len(diviseurs(n))
print(n)

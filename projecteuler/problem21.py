"""
Amicable numbers

https://projecteuler.net/problem=21
"""


def d(n):
    somme = 0
    for i in range(1, n // 2 + 1):
        if n % i == 0:
            somme += i
    return somme


resultat = 0
for i in range(1, 10000):
    a = d(i)
    if d(a) == i and a != i:
        # print(i, "amicable avec", a)
        resultat += i
print(resultat)

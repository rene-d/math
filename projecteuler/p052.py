"""
Permuted multiples

https://projecteuler.net/problem=52
"""


def meme_chiffres(a, b):
    return sorted(str(a)) == sorted(str(b))


for i in range(1, 1000000):

    if all([meme_chiffres(i, i * j) for j in range(2, 7)]):
        print(i)
        break

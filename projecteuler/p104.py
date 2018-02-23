"""
Pandigital Fibonacci ends

https://projecteuler.net/problem=104
"""


def pandigital(n):
    """ retourne True si n (modulo 10^9) contient tous les chiffres de 1 à 9 """
    test = 0
    for _ in range(0, 9):
        n, r = divmod(n, 10)
        test = test | (1 << r)
    return test == 0b1111111110


a, b = 1, 1
k = 1
while True:
    k += 1
    a, b = b, a + b

    if pandigital(a % 1000000000):
        if pandigital(int(str(a)[0:9])):
            print(k)
            break

"""
Pandigital products

We shall say that an n-digit number is pandigital if it makes use of all the digits 1 to n exactly
once; for example, the 5-digit number, 15234, is 1 through 5 pandigital.

The product 7254 is unusual, as the identity, 39 × 186 = 7254, containing multiplicand, multiplier,
and product is 1 through 9 pandigital.

Find the sum of all products whose multiplicand/multiplier/product identity can be written as a 1
through 9 pandigital.

HINT: Some products can be obtained in more than one way so be sure to only include it once in your
sum.

https://projecteuler.net/problem=32
"""


def pandigital(a, b, c):
    """ retourne True si n (modulo 10^9) contient tous les chiffres de 1 à 9 """

    usage = [0] * 10

    def test(n):
        while n != 0:
            n, r = divmod(n, 10)
            usage[r] += 1

    test(a)
    test(b)
    test(c)

    return all([i == 1 for i in usage[1:]]) and usage[0] == 0


resultat = set()
for a in range(1, 100000):
    for b in range(1, 98765432 // a + 1):
        c = a * b
        if len(str(c)) + len(str(a)) + len(str(b)) > 9:
            break
        if pandigital(a, b, c):
            resultat.add(c)
print(sum(resultat))

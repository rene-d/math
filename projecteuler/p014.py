"""
Longest Collatz sequence

https://projecteuler.net/problem=14
"""

sequences = dict()


def collatz(n):
    longueur = 1
    n_orig = n
    while n > 1:
        j = sequences.get(n, 0)
        if j != 0:
            longueur += j
            break
        longueur += 1
        if n % 2 == 0:
            n = n // 2
        else:
            n = 3 * n + 1
    sequences[n_orig] = longueur
    return longueur


longueur_max = resultat = 0
for i in range(1, 1000000):
    longueur = collatz(i)
    if longueur > longueur_max:
        # print(longueur, i)
        longueur_max = longueur
        resultat = i
print(resultat)

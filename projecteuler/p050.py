"""
Consecutive prime sum

The prime 41, can be written as the sum of six consecutive primes:

41 = 2 + 3 + 5 + 7 + 11 + 13
This is the longest sum of consecutive primes that adds to a prime below one-hundred.

The longest sum of consecutive primes below one-thousand that adds to a prime,
contains 21 terms, and is equal to 953.

Which prime, below one-million, can be written as the sum of the most consecutive primes?

https://projecteuler.net/problem=50
"""

from eulerlib import est_premier, Crible


MAX = 1000000

crible = Crible(4000)
premiers = crible.liste()

cumul = [0]
somme = 0
for i, p in enumerate(premiers):
    somme += p
    if somme > MAX:
        break
    cumul.append(somme)

# vérifie qu'on a bien calculé assez de premiers
assert somme > MAX

longueur = 1
resultat = 0
for i in range(len(cumul)):
    for j in range(i + longueur, len(cumul)):
        n = cumul[j] - cumul[i]
        if est_premier(n):
            longueur = j - i
            resultat = n

print(resultat, longueur)

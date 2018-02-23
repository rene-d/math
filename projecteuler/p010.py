"""
Summation of primes

The sum of the primes below 10 is 2 + 3 + 5 + 7 = 17.

Find the sum of all the primes below two million.

https://projecteuler.net/problem=10
"""

from eulerlib import est_premier, Crible


MAX = 2000000

# solution avec crible
crible = Crible(MAX)
print(sum(crible.liste()))


"""

# les solutions ci-après sont lentes mais donnent le même résultat

# solution en testant tous les entiers impairs
somme = 2
i = 3
while i < MAX:
    if est_premier(i):
        somme += i
    i += 2
print(somme)

# même solution, écriture plus concise
print(2 + sum(i for i in range(3, MAX, 2) if est_premier(i)))

"""
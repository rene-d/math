#! /usr/bin/env python3
"""
Test de la primalité d'un nombre

Détails de l'algorithme et de son implémentation en Python
"""


# saisit le nombre à vérifier
n = input('entrez le nombre à tester : ')

# convertit la chaîne de caractères en entier
n = int(n)

# 0 et 1 ne sont pas des nombres premiers
if n <= 1:
    print(n, "n'est pas premier")

# 2 est le seul premier pair
elif n == 2:
    print(n, "est premier !")

# teste si le nombre est pair (% = reste de la division entière)
elif n % 2 == 0:
    print(n, "est pair")

# n ≥ 3 : on cherche s'il a un diviseur d impair, avec d² ≤ n
else:
    d = 3
    est_premier = True
    while d * d <= n:
        if n % d == 0:
            print(n, "est multiple de", d)
            est_premier = False
        d = d + 2
    if est_premier:
        print(n, "est premier !")

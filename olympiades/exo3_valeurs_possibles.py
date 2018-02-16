#! /usr/bin/env python3

# Préparation Olympiades de Mathématiques - Exercice 3

import sys


# programme de calcul de l'énoncé
def calcule(N):
    while True:
        X = N % 10
        M = N - X
        D = int(M / 10)
        R = D + 2 * X
        if R == N:
            break
        if R < 10:
            break
        N = R
    return R


# cherche les valeurs possibles de sortie du programme de calcul pour N de 1 à M
def possibles(M):
    valeurs = set()             # set() est une instruction qui crée une liste à valeurs uniques

    # boucle sur tous les N
    for N in range(1, M + 1):   # N prendra les valeurs de 1 à M
        R = calcule(N)          # effectue le programme de calcul
        valeurs.add(R)          # ajoute R à la liste s'il n'est pas déjà dedans

    # affichage du résultat
    print("valeurs possibles pour 1 ≤ N ≤ %d : %r" % (M, valeurs))


def main():
    if len(sys.argv) >= 2:
        M = int(sys.argv[1])
        possibles(M)
    else:
        possibles(1000)


if __name__ == '__main__':
    main()

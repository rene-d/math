#! /usr/bin/env python3

# Préparation Olympiades de Mathématiques - Exercice 3

import sys


def calcule(N):
    print()
    print("=================> entrée du programme de calcul: N = ", N)

    while True:

        print("(début)   N = ", N)

        # étape 1: repérer le chiffre X des unités de N
        # en informatique, ceci s'obtient avec un modulo
        X = N % 10
        print("(étape 1) X = ", X)

        # étape 2: calculer N-X et stocker dans M
        M = N - X
        print("(étape 2) M = ", M)

        # étape 3: diviser M par D et stocker dans D
        D = int(M / 10)
        print("(étape 3) D = ", D)

        # étape 4: calculer D+2*X et stocker dans R
        R = D + 2 * X
        print("(étape 4) R = ", R)

        # étape 5: si R≠N aller à l'étape 6 sinon arrêter
        if R == N:
            print("(étape 5) stop étape 5")
            break

        # étape 6: si R a un seul chiffre alors arrêter sinon recommencer à l'étape 1
        # en informatique (et math aussi), ceci revient à dire que R≤9
        if R <= 9:
            print("(étape 6) stop étape 6")
            break

        # on va reprendre le calcul avec R comme valeur d'entrée (N)
        N = R
        print()

    # sortie de la boucle, on affiche le résultat
    print("=================> résultat: R = ", R)
    return R


if len(sys.argv) >= 2:
    for N in sys.argv[1:]:
        N = int(N)
        print("%5d ->  %3d " % (N, calcule(N)))
else:
    calcule(15)
    calcule(2015)

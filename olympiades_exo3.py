#! /usr/bin/env python3

# Préparation Olympiades de Mathématiques - Exercice 3

import sys


def calcule(N):
   print()
   while True:
      print("N = ", N)

      X = N % 10
      print("X = ", X)

      M = N - X
      print("M = ", M)

      D = int(M / 10)
      print("D = ", D)

      R = D + 2 * X
      print("R = ", R)

      if R == N:
          print("stop étape 5")
          break

      if R < 10:
          print("stop étape 6")
          break

      N = R
      print()

   print("=================> résultat: R = ", R)
   return R


if len(sys.argv) >= 1:
    for N in sys.argv[1:]:
        N = int(N)
        print("%5d ->  %3d " % (N , f(N)))
else:
    calcule(15)
    calcule(2015)


"""

N =  15
X =  5
M =  10
D =  1
R =  11

N =  11
X =  1
M =  10
D =  1
R =  3
stop étape 6
=================> résultat: R =  3

N =  2015
X =  5
M =  2010
D =  201
R =  211

N =  211
X =  1
M =  210
D =  21
R =  23

N =  23
X =  3
M =  20
D =  2
R =  8
stop étape 6
=================> résultat: R =  8
"""

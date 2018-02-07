#! /usr/bin/env python3

import math


# calcule la longueur du côté
print("Calcul de la longueur du côté du pentagone régulier inscrit")
print("dans le cercle de rayon R")

R = float(input("Entrez R : "))
D = 2 * R * math.sin(36 * math.pi / 180)
print("Côté du pentagone : ", D)

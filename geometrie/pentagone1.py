#! /usr/bin/env python3

from math import sin, pi


# calcule la longueur du côté
print("Calcul de la longueur du côté du pentagone régulier inscrit")
print("dans le cercle de rayon R")

R = float(input("Entrez R : "))
D = 2 * R * sin(36 * pi / 180)
print("Côté du pentagone : ", D)

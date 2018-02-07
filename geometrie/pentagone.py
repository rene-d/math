#! /usr/bin/env python3

import math
import turtle


# calcule la longueur du côté
print("Calcul de la longueur du côté du pentagone régulier inscrit")
print("dans le cercle de rayon R")

R = float(input("Entrez R : "))
D = 2 * R * math.sin(36 * math.pi / 180)
print("Côté du pentagone : ", D)

# utilise des coordonnées -10 à 10 pour les abscisses, -15 à 5 pour les ordonnées
turtle.setworldcoordinates(-10, -15, 10, 5)

# trace le pentagone de côté D
turtle.right(36)
for i in range(5):
    turtle.forward(D)           # avance de D
    turtle.right(72)            # tourne de 72°

# trace le cercle de rayon R
turtle.setheading(0)
turtle.color('red')
turtle.circle(-R, steps=100)    # trace le cercle

# attend que la fenêtre soit fermée
turtle.mainloop()

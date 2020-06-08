#! /usr/bin/env python3

import math
import turtle


# saisie du rayon du cercle
R = turtle.numinput("Pentagone",
                    """
Calcul de la longueur du côté du pentagone régulier inscrit dans le cercle de rayon R.

Entrez R :""", 2, 1, 10)

# calcule la longueur du côté
D = 2 * R * math.sin(36 * math.pi / 180)

# utilise des coordonnées -10 à +10 pour les abscisses, -19 à +1 pour les ordonnées
# en appliquant le ratio de correction entre hauteur et largeur
ratio = turtle.window_width() / turtle.window_height()
turtle.setworldcoordinates(-10 * ratio, -19, 10 * ratio, 1)

turtle.write('Rayon du cercle = {:.3f}\nCôté du pentagone = {:.3f}'.format(R, D),
             False, align="center")

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

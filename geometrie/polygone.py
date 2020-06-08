#! /usr/bin/env python3

# charge les fonctions mathématiques
from math import sin, cos, pi

# charge la librairie "turtle" qui permet de dessiner rapidement
from turtle import *


# saisie du nombre de côtés
n = int(numinput("Polygone", "Nombre de côtés ? ", 5, 5, 30))

# calcule un rayon acceptable en fonction de la fenêtre
R = window_height() * 0.45

# calcule les sommets du polygone
sommets = [(R * cos(2 * pi / n * i), R * sin(2 * pi / n * i))
           for i in range(n)]

title("Etoiles : {} sommets".format(n))
hideturtle()
speed(speed="fastest")

for i in range(n):
    for j in range(n):
        if (i - j + n) % n in range(2, int((n - 1) / 2 + 1)):
            penup()
            goto(sommets[i])
            pendown()
            goto(sommets[j])

# pour sauvegarder le dessin:
# getscreen().getcanvas().postscript(file='etoile{}.eps'.format(n), colormode='color')

mainloop()

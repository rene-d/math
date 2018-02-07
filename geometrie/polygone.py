#! /usr/bin/env python3

# librairie "système"
import sys

# charge la librairie des fonctions mathématiques
import math
# autre possibilité: from math import sqrt
# et on utilise sqrt() au lieu de math.sqrt()

# charge la librairie "turtle" qui permet de dessiner rapidement
from turtle import *

if len(sys.argv) == 2:
    n = int(sys.argv[1])
else:
    while True:
        n = input("nombre de côtés ? ")
        n = int(n)
        if n >= 3 and n <= 20:
            break
        print("entrez un nombre impair entre 3 et 20.")


R = screensize()[1] * 0.9

sommets = [(R * math.cos(2 * math.pi / n * i), R * math.sin(2 * math.pi / n * i))
           for i in range(n)]

title("Etoiles")
hideturtle()
speed(speed="fastest")

for i in range(n):
    for j in range(n):
        if (i - j + n) % n in range(2, int((n - 1) / 2 + 1)):
            penup()
            goto(sommets[i])
            pendown()
            goto(sommets[j])


# ts = getscreen()
# ts.getcanvas().postscript(file='etoile{}.eps'.format(n), colormode='color')

print("Appuyez sur Entrée pour terminer...")
input()

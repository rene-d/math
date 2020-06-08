#! /usr/bin/env python3

# -*- coding: utf-8 -*-

from __future__ import print_function
import os, sys
import turtle


# dessine une ligne entre deux points
def ligne(x1, y1, x2, y2):
    turtle.penup()
    turtle.goto(x1, y1)
    turtle.pendown()
    turtle.goto(x2, y2)


# dessine le pendu
def pendu(n):

    # initialisation
    if n == 0:
        turtle.hideturtle()
        turtle.penup()
        turtle.goto(0, 250)
        turtle.write("JEU DU PENDU", align="center", font=("Helvetica", 30, "normal"))

    # première erreur, on dessine la base de la potence
    if n == 1:
        turtle.pensize(8)
        ligne(-50, -150, 50, -150)

    # deuxième erreur, on dessine le poteau
    if n == 2:
        turtle.pensize(5)
        ligne(0, -150, 0, 200)

    # etc.
    if n == 3:
        ligne(0, 200, 150, 200)

    if n == 4:
        l = 45  # longueur de la corde
        ligne(0, 200 - l, l, 200)

    if n == 5:
        ligne(150, 200, 150, 200 - 35)

    if n == 6:
        r = 20  # rayon de la tête
        turtle.pensize(3)
        turtle.pencolor("blue")
        turtle.penup()
        turtle.goto(150, 200 - 35 - r * 2)
        turtle.pendown()
        turtle.circle(r)

    if n == 7:
        ligne(150, 200 - 35 - 2 * 20, 150, 0)

    if n == 8:
        ligne(100, 75, 200, 75)

    if n == 9:
        ligne(150, 0, 100, -50)

    if n == 10:
        ligne(150, 0, 200, -50)


print("Jeu du pendu")
pendu(0)  # initialisation graphique

mot = input("Entrez un mot à faire deviner : ")

# convertit mot en majuscules
mot = mot.upper()

# calcule la longueur du mot
longueur = len(mot)

print("Le mot", mot, "contient", longueur, "lettres.")
input("Appuyez sur Entrée pour démarrer le jeu... ")

os.system("clear")

# compteur d'erreurs
erreurs = 0

# les lettres trouvées
trouvees = ""
for i in range(0, longueur):
    if mot[i].isalpha():
        trouvees = trouvees + "_"
    else:
        trouvees = trouvees + mot[i]

while True:

    print()
    print("Erreur", erreurs, ": ", trouvees)

    lettre = input("Lettre ? ")
    if lettre == ".":
        sys.exit()

    lettre = lettre.upper()
    if len(lettre) != 1 or not lettre.isalpha():
        print("Erreur de saisie. Il faut entrer une lettre (A à Z).")
        continue

    lettre_trouvee = False
    for i in range(0, longueur):
        if lettre == mot[i]:
            trouvees = trouvees[0:i] + lettre + trouvees[i + 1 :]
            lettre_trouvee = True

    if trouvees == mot:
        print()
        print("C'EST GAGNÉ !!! Le mot était bien:", mot)
        print()
        break

    if lettre_trouvee == False:
        erreurs = erreurs + 1
        pendu(erreurs)

    if erreurs >= 10:
        print()
        print("PENDU :( Le mot à trouver était:", mot)
        print()
        break

print("Merci d'avoir joué au jeu du Pendu !")
input()

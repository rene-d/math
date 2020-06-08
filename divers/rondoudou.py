#!/usr/bin/env python3

# Romain et René DEVICHI
# 31 mai 2020

import re
import turtle


# définition des points (énoncé de la « Figure mystère »)
donnees = """
Oreilles
A1 (-4;6)
A2 (-3,8;7,5) A3 (-3,5;9) A4 (-3;10) A5 (-2;9,6) A6 (-1;9)
A7 (0;8)
B1 (-3,25;6,5) B2 (-3,25;7,5) B3 (-3;8,5)
B4 (-2,75;9,25) B5 (-2;8,5)
B6 (-1,5;7,5) B7 (-2,5;7)
C1 (4,5;6) C2 (5,5;6) C3 (6,5;5,8) C4 (7,5;5,5) C5 (8;5)
C6 (7;3) C7 (5,5;2)
D1 (5;4,75)
D2 (6;4,75) D3 (7,25;4,5)
D4 (6,5;3,5)
D5 (5,5;2,75)
D6 (5,5;3,75)

Mèches
F1 (2;4,5) F2 (1,5;3)
F3 (0;2,5) F4 (-1;3)
F5 (-1,75;4)
F6 (-1,75;5) F7 (-1,5;6) F8 (-1;7)
F9 (-0,5;7,5) F10 (1,5;8,5)
F11 (2;8,5) F12 (3;8)
F13 (3,5;7,5) F14 (4;6,5) F15 (4,5;5,5)
F16 (4;5,5) F17 (1;4)
F18 (3;5)
F19 (3,5;5,5)

Pattes avants
G1 (-5;3)
G2 (-5,5;3,75) G3 (-6;4)
G4 (-6,5;3,75) G5 (-6,5;3)
G6 (-6;2)
G7 (-5;1)
G8 (2;-0,5)
G9 (2,25;-1,5) G10 (3;-2)
G11 (3,5;-1) G12 (3,3;0)

Pattes arrières
I1 (-4,5;-1)
I2 (-5,5;-2,25) I3 (-6,5;-3,25) I4 (-7;-4,5)
I5 (-6,5;-5)
I6 (-4,25;-4,5) I7 (-3,5;-4)
I8 (-2,75;-3,25)
I9 (1;-3,9)
I10 (2;-4,5)
I11 (3;-4,75) I12 (4;-5)
I13 (5;-5)
I14 (5,75;-4,5) I15 (5,5; - 3,75) I16 (5;-3)
I17 (4,5 ; - 2,5) I18 (3,75 ; - 2)

Bouche
E1 (-2;1)
E2 (-1,5;0,5) E3 (0;0)

Corps
M1 (-4,5;5) M2 (-5;0)
M3 (-4;-2) M4 (-3;-3) M5 (-2;-3,5)
M6 (0;-4) M7 (2;-3,5) M8 (3;-2,75) M9 (4,5;-1) M10 (5;0)
"""


points = {}


def coordonnees(x0, y0, x1, y1):
    """ définit le repère et trace les axes X Y. """
    turtle.reset()
    turtle.setworldcoordinates(x0, y0, x1, y1)
    turtle.speed(0)
    turtle.pencolor("blue")
    turtle.penup()
    for x in range(x0, x1 + 1):
        turtle.goto(x, 0)
        turtle.pendown()
        turtle.dot()

    turtle.penup()
    for y in range(y0, y1 + 1):
        turtle.goto(0, y)
        turtle.pendown()
        turtle.dot()


def cercle(x, y, r):
    """ trace un cercle de centre x,y et de rayon r. """
    turtle.penup()
    turtle.goto(x, y - r)
    turtle.pendown()
    turtle.setheading(0)
    turtle.circle(r, steps=20)


def relie(liste, debut=None, fin=None):
    """ relie une liste de points par des traits. """
    if debut:
        turtle.penup()
        for i in range(debut, fin + 1):
            p = liste + str(i)
            turtle.goto(*points[p])
            turtle.pendown()
    else:
        turtle.penup()
        for p in liste.split():
            turtle.goto(*points[p])
            turtle.pendown()


# lecture des points (avec une expression régulière)
for p, x, y in re.findall(r"([A-Z]\d+)\((\-?\d+?,?\d*?);(\-?\d+?,?\d*)\)", donnees.replace(" ", "")):
    x = float(x.replace(",", "."))
    y = float(y.replace(",", "."))
    print(p, x, y)
    points[p] = (x, y)


coordonnees(-8, -6, 9, 11)
turtle.speed(0)
turtle.pencolor("black")

relie("A", 1, 7)
relie("B1 B2 B3 B4 B5 B6 B7 B1")

relie("C1 C2 C3 C4 C5 C6 C7")
relie("D1 D2 D3 D4 D5 D6 D1")

relie("F", 1, 15)
relie("F14 F16")
relie("F17 F19")

relie("G", 1, 7)
relie("G", 8, 12)

relie("I", 1, 8)
relie("I", 9, 18)

relie("E1 E2 E3")

relie("A1 M1 G1 G7 M2 I1 M3 M4 I8 M5 M6 I9 M7 M8 I18 M9 M10 C7")

cercle(4, 3, 0.4)
cercle(3.5, 2, 1.5)
cercle(3.75, 2.5, 1)

cercle(-2, 4, 0.4)
cercle(-2.5, 3, 1.5)
cercle(-2.25, 3.5, 1)


turtle.penup()
turtle.goto(4, 9.5)
turtle.write("Rondoudou", font=("Corbel", 30))

turtle.hideturtle()
turtle.mainloop()

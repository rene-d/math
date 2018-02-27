"""
Marsh Crossing

https://projecteuler.net/problem=607
"""

from p607 import *
import turtle


def l(*v):
    it = iter(v)
    first = True
    while True:
        try:
            x = next(it)
            y = next(it)
            if first:
                first = False
                turtle.penup()
            else:
                turtle.pendown()
            turtle.goto(x, y)
        except StopIteration:
            break
    turtle.penup()


# initialise turtle
ratio = turtle.window_width() / turtle.window_height()
turtle.setworldcoordinates(-10 * ratio, -30, 100 * ratio, 80)
turtle.speed(0)

# appelle le solver
y0, y1, y2, y3, y4, y5 = res.x

# trace les zones du marais
l(x0, -20, x0, 80)
l(x1, -20, x1, 80)
l(x2, -20, x2, 80)
l(x3, -20, x3, 80)
l(x4, -20, x4, 80)
l(x5, -20, x5, 80)

# nom des zones
turtle.goto((x0 + x1) / 2, -5)
turtle.write("zone 9", move=False, align="center")
turtle.goto((x1 + x2) / 2, -5)
turtle.write("zone 8", move=False, align="center")
turtle.goto((x2 + x3) / 2, -5)
turtle.write("zone 7", move=False, align="center")
turtle.goto((x3 + x4) / 2, -5)
turtle.write("zone 6", move=False, align="center")
turtle.goto((x4 + x5) / 2, -5)
turtle.write("zone 5", move=False, align="center")

# chemin direct
l(xa, ya, xb, yb)

# chemin optimisé
turtle.pensize(5)
l(xa, ya, x0, y0, x1, y1, x2, y2, x3, y3, x4, y4, x5, y5, xb, yb)

turtle.mainloop()

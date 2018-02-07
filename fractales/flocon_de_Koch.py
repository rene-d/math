#! /usr/bin/env python3
# rene-d 2016

""" trace un flocon de Koch """

import turtle
from raise_app import raise_app


generation = 0
taille = 400.0


def koch(l, n):
    """ Fractacle de Koch """
    if n <= 0:
        turtle.forward(l)
    else:
        koch(l / 3, n - 1)
        turtle.left(60)
        koch(l / 3, n - 1)
        turtle.right(120)
        koch(l / 3, n - 1)
        turtle.left(60)
        koch(l / 3, n - 1)


def flocon(l, n):
    """ Flocon de Koch """
    koch(l, n)
    turtle.right(120)
    koch(l, n)
    turtle.right(120)
    koch(l, n)


def dessine(l, n):          # pragma: no cover
    """ dessine l'étoile de Koch de génération n """

    turtle.onkey(None, 'Left')
    turtle.onkey(None, 'Right')

    turtle.reset()
    turtle.clear()

    turtle.hideturtle()

    if n < 2:
        turtle.speed(0.1)
    else:
        turtle.speed(0)

    turtle.penup()
    turtle.setpos(-l / 2, l / 3)
    turtle.pendown()
    turtle.setheading(0)

    turtle.color('red', 'yellow')
    turtle.begin_fill()
    flocon(l, n)
    turtle.end_fill()

    turtle.onkey(lambda: precedent(0, 0), 'Left')
    turtle.onkey(lambda: suivant(0, 0), 'Right')


def suivant(x, y):          # pragma: no cover
    """ augmente le niveau de génération """
    global generation, taille
    generation += 1
    dessine(taille, generation)


def precedent(x, y):        # pragma: no cover
    """ diminue le niveau de génération """
    global generation, taille
    if generation > 1:
        generation -= 1
        dessine(taille, generation)


def main():                 # pragma: no cover
    print("⟶ : augmenter la génération")
    print("⟵ : diminuer la génération")
    print(" x : sortir")

    # dessine une première étoile
    suivant(0, 0)

    turtle.onkey(turtle.bye, 'x')
    turtle.onkey(turtle.bye, 'q')

    turtle.listen()
    raise_app()
    turtle.mainloop()


if __name__ == '__main__':
    main()

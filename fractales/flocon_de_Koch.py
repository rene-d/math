#! /usr/bin/env python3
# rene-d 2016

""" trace un flocon de Koch """

import turtle

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


def dessine(l, n):
    """ dessine l'étoile de Koch de génération n """

    turtle.reset()
    turtle.clear()

    turtle.onscreenclick(None, 1)
    turtle.onscreenclick(None, 3)

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

    turtle.onscreenclick(suivant, 1)
    turtle.onscreenclick(precedent, 3)


def suivant(x, y):
    """ augmente le niveau de génération """
    global generation, taille
    generation += 1
    dessine(taille, generation)


def precedent(x, y):
    """ diminue le niveau de génération """
    global generation, taille
    if generation > 1:
        generation -= 1
        dessine(taille, generation)


def main():
    print("x: sortir")
    print("clic gauche: augmenter la génération")
    print("clic droit: diminuer la génération")

    # dessine une première étoile
    suivant(0, 0)

    turtle.onkey(turtle.bye, 'x')
    turtle.listen()
    turtle.mainloop()


if __name__ == '__main__':
    main()

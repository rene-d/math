"""
test des programmes géométrie
"""
from unittest.mock import call


def test_pentagone1(mocker, capsys):
    # pi = mocker.patch("math.pi")
    # pi.return_value = 3
    # sin = mocker.patch("math.sin")
    # sin.return_value = 1

    __builtins__['input'] = lambda x: "3"

    # doit être placé après la ligne ci-dessus pour court-circuiter la fonction input()
    import pentagone1       # noqa

    D = 2 * 3 * 0.5877852522924731

    captured = capsys.readouterr()
    assert captured.out.endswith("Côté du pentagone :  {}\n".format(D))


def test_pentagone2(mocker):
    import turtle
    from math import sqrt

    # sin(π/5)
    sin36 = sqrt(-2 * sqrt(5) + 10) / 4

    R = 10
    D = 2 * R * sin36

    # installe les mockers du module turtle
    ni = mocker.patch("turtle.numinput")
    ni.return_value = R
    ww = mocker.patch("turtle.window_width")
    ww.return_value = 100
    wh = mocker.patch("turtle.window_height")
    wh.return_value = 100
    mocker.patch("turtle.setworldcoordinates")
    mocker.patch("turtle.write")
    mocker.patch("turtle.right")
    mocker.patch("turtle.forward")
    mocker.patch("turtle.setheading")
    mocker.patch("turtle.color")
    mocker.patch("turtle.circle")
    mocker.patch("turtle.mainloop")

    # lance le programme pentagone2
    import pentagone2       # noqa

    # teste saisie du rayon
    assert ni.call_count == 1

    # teste calcul du diamètre
    assert pentagone2.D == 2 * 10 * sin36

    # teste dessin du pentagone
    turtle.right.assert_has_calls([call(72)] * 5)
    turtle.forward.assert_has_calls([call(D)] * 5)

    # teste tracé du cercle
    turtle.circle.assert_called_once_with(-R, steps=100)

    # teste l'appel à la mainloop
    turtle.mainloop.assert_called_once_with()

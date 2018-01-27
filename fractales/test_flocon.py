from unittest.mock import call
import flocon_de_Koch as koch
import turtle


def test_gen0(mocker):
    """ test génération 0 : un trait simple de la taille donnée """
    mocker.patch('turtle.forward')
    koch.koch(1, 0)
    turtle.forward.assert_called_once_with(1)


def test_gen1(mocker):
    """ test génération 1: 4 traits : _/\_ """
    mocker.patch.object(turtle, 'forward')
    mocker.patch.object(turtle, 'left')
    mocker.patch.object(turtle, 'right')

    koch.koch(3, 1)

    # quatre traits
    assert turtle.forward.mock_calls == [call(1), call(1), call(1), call(1)]

    # trois virages
    assert turtle.left.mock_calls == [call(60), call(60)]
    assert turtle.right.mock_calls == [call(120)]

def test_flocon0(mocker):
    """ flocon de génération 0: triangle équilatéral """

    mocker.patch.object(turtle, 'forward')
    mocker.patch.object(turtle, 'left')
    mocker.patch.object(turtle, 'right')

    koch.flocon(3, 0)

    assert turtle.forward.mock_calls == [call(3)] * 3
    assert turtle.left.mock_calls == []
    assert turtle.right.mock_calls == [call(120)] * 2


def test_flocon1(mocker):
    """ flocon de génération 1: _/\_ trois fois """
    mocker.patch.object(turtle, 'forward')
    mocker.patch.object(turtle, 'left')
    mocker.patch.object(turtle, 'right')

    koch.flocon(3, 1)

    # trois fois quatre traits _
    assert turtle.forward.mock_calls == [call(1)] * (4 * 3)

    # trois fois deux virages à 60° _/ \_
    assert turtle.left.mock_calls == [call(60)] * (2 * 3)

    # trois fois un virage à 120° /\ 
    # et deux virages à 120° entre les côtés du triangle flocon0
    assert turtle.right.mock_calls == [call(120)] * (1 * 3 + 2)
    
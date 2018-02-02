"""
unit test pour fractales.py
"""

import fractales


def test_Point2D():
    p = fractales.Point2D(1.2, -3.1415926535)
    assert p.x == 1.2
    assert p.y == -3.1415926535
    assert p.str() == "1.20000 x -3.14159"


def test_PointF():
    p = fractales.PointF(0, 1)
    assert p.x == 0
    assert p.y == 1
    assert p.sens is True
    assert p.inverse is False

    p = fractales.PointF(0, 1, True, False)
    assert p.x == 0
    assert p.y == 1
    assert p.sens is True
    assert p.inverse is False

    p = fractales.PointF(0, 1, False, True)
    assert p.x == 0
    assert p.y == 1
    assert p.sens is False
    assert p.inverse is True


def test_Fractale(mocker):
    f = fractales.Fractale()
    assert f.nom == "Koch"
    assert f.max == 7
    assert len(f.gen) == 5
    assert isinstance(f.gen[0], fractales.PointF)
    assert isinstance(f.segments[0][0], fractales.Point2D)


def test_Dessine(mocker):

    pf = fractales.PointF
    p2 = fractales.Point2D

    f = fractales.Fractale()
    f.nom = "test"
    f.max = 1
    f.gen = [pf(0, 0), pf(1, 0), pf(1, 1)]      # г
    f.init_trace()

    assert f.limites == [0, 1, 0, 1]
    assert f.segments == [[p2(0, 0), p2(1, 1)]]

    crt = mocker.patch.object(fractales, 'Crt')
    # TODO: il faut hook crt.conv et create_line puis vérifier la génération
    fractales.Dessine(f, details=False, generation=1)
    assert crt.call_count == 1

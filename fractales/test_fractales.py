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

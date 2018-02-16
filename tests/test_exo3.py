"""
    unittest de calcule.py et valeurs_possibles.py
"""


import sys
from unittest.mock import call
import exo3_calcule as c
import exo3_valeurs_possibles as vp


def test_calcule():
    assert c.calcule(57) == 19
    assert c.calcule(15) == 3
    assert c.calcule(2015) == 8


def test_calcule_main(mocker):
    mocker.patch.object(sys, 'argv', ["prog", "123"])
    mocker.patch.object(c, 'calcule')
    c.main()
    c.calcule.assert_called_once_with(123)

    mocker.patch.object(sys, 'argv', ["prog"])
    mocker.patch.object(c, 'calcule')
    c.main()
    c.calcule.assert_has_calls([call(15), call(2015)])
    assert c.calcule.call_count == 2


def test_vp_calcule():
    assert vp.calcule(57) == 19
    assert vp.calcule(15) == 3
    assert vp.calcule(2015) == 8


def test_vp_possibles(mocker, capsys):
    calcule = mocker.patch.object(vp, 'calcule')
    calcule.return_value = 456
    vp.possibles(2)
    vp.calcule.assert_has_calls([call(1), call(2)])
    captured = capsys.readouterr()
    assert captured.out == "valeurs possibles pour 1 ≤ N ≤ 2 : {456}\n"


def test_vp_main(mocker):
    # test sans argument: 1000 est la valeur par défaut
    mocker.patch.object(sys, 'argv', ["prog"])
    mocker.patch.object(vp, 'possibles')
    vp.main()
    vp.possibles.assert_called_once_with(1000)

    # test avec un argument: 10
    mocker.patch.object(sys, 'argv', ["prog", "10"])
    mocker.patch('exo3_valeurs_possibles.possibles')
    vp.main()
    vp.possibles.assert_called_once_with(10)

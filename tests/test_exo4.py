"""
    unitest de entrainement_2017_exercice_4.py
"""


def test_exo4(capsys):
    import exo4_entrainement_2017 as exo

    # teste la fonction qui compte les chiffres
    assert exo.compte("123", 1) == 1
    assert exo.compte("123", 4) == 0

    # teste le résultat et son affichage
    assert capsys.readouterr().out == 'nombre:  120\nsomme:   6666600\n'

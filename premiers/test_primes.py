import liste_premiers
import decompose


# nombres premiers inférieurs à 100.
primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41,
          43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97]


def test_liste(mocker):
    for i in range(0, 100):
        p = liste_premiers.premier(i)
        assert p == (i in primes)


def test_decompose(mocker):
    n = 48      # 2^4 * 3
    facteurs = decompose.decompose(n)
    facteurs_reduits = decompose.reduit_polynome(facteurs)
    assert facteurs == [2, 2, 2, 2, 3]
    assert facteurs_reduits == ['2^4', '3']

    assert decompose.decompose(34866) == [2, 3, 3, 13, 149]
    assert decompose.decompose(2017) == [2017]
    assert decompose.decompose(65537) == [65537]


def test_decompose_affiche(capsys):
    n = 3 * 13 * 13 * 17 * 43
    assert n == 370617
    decompose.affiche(n)
    assert capsys.readouterr().out == '370617 = 3 ⨯ 13 ⨯ 13 ⨯ 17 ⨯ 43 = 3 ⨯ 13² ⨯ 17 ⨯ 43\n'

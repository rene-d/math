import importlib.util
import liste_premiers
import decompose


# nombres premiers inférieurs à 100.
primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41,
          43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97]


def test_liste(mocker):
    for i in range(0, 100):
        p = liste_premiers.premier(i)
        assert p == (i in primes)


def test_decompose():
    n = 48      # 2^4 * 3
    facteurs = decompose.decompose(n)
    facteurs_reduits = decompose.reduit_polynome(facteurs)
    assert facteurs == [2, 2, 2, 2, 3]
    assert facteurs_reduits == ['2^4', '3']

    assert decompose.decompose(4) == [2, 2]
    assert decompose.decompose(34866) == [2, 3, 3, 13, 149]
    assert decompose.decompose(2017) == [2017]
    assert decompose.decompose(65537) == [65537]
    for i in primes:
        assert decompose.decompose(i) == [i]


def test_decompose_affiche(capsys):
    n = 3 * 13 * 13 * 17 * 43
    assert n == 370617
    decompose.affiche(n)
    assert capsys.readouterr().out == '370617 = 3 ⨯ 13 ⨯ 13 ⨯ 17 ⨯ 43 = 3 ⨯ 13² ⨯ 17 ⨯ 43\n'


def test_premiers(capsys):

    spec = importlib.util.find_spec("premier")
    module = importlib.util.module_from_spec(spec)

    for i in range(0, 100):
        __builtins__['input'] = lambda x: str(i)
        spec.loader.exec_module(module)
        out = capsys.readouterr().out
        if i in primes:
            assert out == str(i) + " est premier !\n"
        elif i < 2:
            assert out == str(i) + " n'est pas premier\n"
        elif i % 2 == 0:
            assert out == str(i) + " est pair\n"
        else:
            assert out.startswith(str(i) + " est multiple de ")
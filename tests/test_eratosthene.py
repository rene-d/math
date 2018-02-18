import eratosthene
import os.path


def lit_reference():

    # utilise en référence la liste des 1000 premiers nombres premiers
    # http://primes.utm.edu/lists/small/1000.txt
    primes = []
    with open(os.path.join(os.path.dirname(__file__), "1000.txt"), "r") as f:
        for i in f:
            try:
                nb = [int(k) for k in i.split()]
                if len(nb) == 10:
                    primes.extend(nb)
            except ValueError:
                pass
    return primes


def _test_crible(cribleur):
    # le 1000e nombre premier est 7919
    # on crible jusqu'à 7921 qui n'est pas premier (=89²)
    N = 7921

    # cherche tous les nombres premiers <= N
    premiers = cribleur(N)

    assert isinstance(premiers, list)
    assert len(premiers) == 1000

    # utilise en référence la liste des 1000 premiers nombres premiers
    # http://primes.utm.edu/lists/small/1000.txt
    reference = lit_reference()
    assert len(premiers) == len(reference)
    assert premiers == reference
    """
    assert len(premiers) <= len(reference)
    for i, v in enumerate(premiers):
        assert v == reference[i]
    """


def test_crible():
    _test_crible(eratosthene.cribler)
    _test_crible(eratosthene.cribler_opti)


def test_cribles():
    reference = lit_reference()
    for n in range(100, 500, 11):
        c1 = eratosthene.cribler(n)
        c2 = eratosthene.cribler_opti(n)
        assert c1 == c2
        for i, v in enumerate(c1):
            assert v == reference[i]


def test_bitfield():
    N = 100
    b = eratosthene.bitfield(N)

    # par défaut, tous les bits sont à 0 (False)
    for i in range(0, N):
        assert not b.is_set(i)

    # vérification du positionnement de 1 bit
    for i in range(0, N):
        b.set(i, True)
        # vérifie qu'il n'y a que le bit i qui est positionné
        for j in range(0, N):
            assert b.is_set(j) == (j == i)
        b.set(i, False)

    # test du positionnement de N bits
    # (peut-être superflu...)
    for i in range(0, N):
        b.set(i, True)
        for j in range(0, N):
            assert b.is_set(j) == (j <= i)

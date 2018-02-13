
# nombres premiers inférieurs à 100.
primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41,
          43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97]


def test_liste(mocker):
    import liste_premiers

    for i in range(0, 100):
        p = liste_premiers.premier(i)
        assert p == (i in primes)

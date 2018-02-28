#! /usr/bin/env python3

import sys


def decompose(n):
    """ décomposition d'un nombre en facteurs premiers """

    facteurs = []

    i = 2
    while i * i <= n:
        while n % i == 0:
            n = n // i
            facteurs.append(i)
        if i >= 3:
            i += 2
        else:
            i += 1

    if n != 1:
        facteurs.append(n)

    return facteurs


def reduit_polynome(facteurs):
    """ réduit les facteurs premiers en puissance p*p*...*p en p^n """

    nb_facteurs = len(facteurs)
    facteurs_reduits = []
    i = 0
    while i < nb_facteurs:
        f = facteurs[i]
        e = 1
        i += 1
        while i < nb_facteurs and f == facteurs[i]:
            e += 1
            i += 1
        if e == 1:
            facteurs_reduits.append('{}'.format(f))
        else:
            facteurs_reduits.append('{}^{}'.format(f, e))

    return facteurs_reduits


def decompose2(n):
    """ réduit les facteurs premiers en puissance p*p*...*p en p^n """

    facteurs = decompose(n)
    nb_facteurs = len(facteurs)
    facteurs_reduits = []
    i = 0
    while i < nb_facteurs:
        f = facteurs[i]
        e = 1
        i += 1
        while i < nb_facteurs and f == facteurs[i]:
            e += 1
            i += 1
        if e == 1:
            facteurs_reduits.append((f, 1))
        else:
            facteurs_reduits.append((f, e))

    return facteurs_reduits


def affiche(n):
    """ affiche la décomposition en facteurs premiers d'un nombre """

    facteurs = decompose(n)
    facteurs_reduits = reduit_polynome(facteurs)

    def expo(x):
        exposants = '⁰¹²³⁴⁵⁶⁷⁸⁹'
        i = x.find('^')
        if i == -1:
            return x
        else:
            return x[0:i] + ''.join([exposants[int(c)] for c in x[i + 1:]])

    expr1 = ' ⨯ '.join([str(i) for i in facteurs])
    expr2 = ' ⨯ '.join([expo(i) for i in facteurs_reduits])

    print('{} = {} = {}'.format(n, expr1, expr2))

    # auto-test !
    assert n == eval('*'.join([str(i) for i in facteurs]))
    assert n == eval('*'.join([i.replace("^", "**") for i in facteurs_reduits]))


def main():
    if len(sys.argv) > 1:
        for arg in sys.argv[1:]:
            affiche(int(arg))
    else:
        n = int(input("Nombre à décomposer : "))
        affiche(n)


if __name__ == '__main__':
    main()

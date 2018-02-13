#! /usr/bin/env python3

import sys


def decompose(n):
    """ décomposition d'un nombre en facteur premier """

    initial = n
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


    def expo(x):
        exposants = '⁰¹²³⁴⁵⁶⁷⁸⁹'
        i = x.find('^')
        if i == -1:
            return x
        else:
            return x[0:i] + ''.join([exposants[int(c)] for c in x[i+1:]])

    expr1 = ' ⨯ '.join([str(i) for i in facteurs])
    expr2 = ' ⨯ '.join([expo(i) for i in facteurs_reduits])

    print(initial, '=', expr1, '=', expr2)

    verif1 = eval('*'.join([str(i) for i in facteurs]))
    verif2 = eval('*'.join([i.replace("^", "**") for i in facteurs_reduits]))

    assert initial == verif1
    assert initial == verif2

    return facteurs, facteurs_reduits


def main():
    decompose(int(sys.argv[1]))


if __name__ == '__main__':
    main()

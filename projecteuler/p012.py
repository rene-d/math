"""
Highly divisible triangular number

https://projecteuler.net/problem=12
"""


def nb_diviseurs(n):
    div = 1
    i = 2
    while i * i <= n:
        q, r = divmod(n, i)
        if r == 0:
            div += 1
            if i != q:
                div += 1
        i += 1
    if n != 1:
        div += 1
    return div


def bruteforce():
    """ solution par bruteforce (lent) """
    i = 0
    n = 0
    nd = 0
    while nd < 500:
        i += 1
        n += i
        nd = nb_diviseurs(n)
    print(n)


def decompose(n):
    """ décomposition d'un nombre en facteurs premiers """
    facteurs = {}
    i = 2
    while i * i <= n:
        while n % i == 0:
            n = n // i
            facteurs[i] = facteurs.get(i, 0) + 1
        if i >= 3:
            i += 2
        else:
            i += 1
    if n > 1:
        facteurs[n] = facteurs.get(n, 0) + 1
    return facteurs


# calcul plus intelligent: le nombre de diviseurs de Tn est calculé
# avec la décomposition de n et n+1 (moins un 2)
i = 2
a = decompose(i)
while True:
    i += 1
    b = decompose(i)

    # fusionne les deux décompositions
    for k, v in b.items():
        a[k] = a.get(k, 0) + v

    # calcule le nombre de diviseurs
    f = 1
    for k, v in a.items():
        if k == 2:
            v -= 1
        f *= v + 1

    if f > 500:
        print(i * (i - 1) // 2)
        break

    a = b

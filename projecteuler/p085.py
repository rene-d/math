"""
Counting rectangles

https://projecteuler.net/problem=85
https://www.hackerrank.com/contests/projecteuler/challenges/euler085/problem
"""


# pour un quadrillage de 1 x N, on peut faire T(N) rectangles
def T(x):
    return x * (x + 1) // 2


# pour un quadrillage de M x N, on peut faire T(M) x T(N) rectangles
def Rect(x, y):
    return T(x) * T(y)


# résoud à peu près x(x+1)/2 = a
def invT(a):
    return int(((8 * a + 1) ** 0.5 - 1) / 2)


def solve(n):
    x_max = invT(n) + 2
    nb_min = 100000
    resultat = 0
    for x in range(1, x_max + 1):
        a = max(x, invT(n / (x * (x + 1) / 2)) - 2)
        for y in range(a, x_max + 1):
            nb = Rect(x, y) - n

            if nb > nb_min:
                break

            nb = abs(nb)
            if nb < nb_min:
                nb_min = nb
                resultat = x * y
            elif nb == nb_min:
                resultat = max(resultat, x * y)

    print(resultat)


def p085():
    solve(2000000)


def hackerrank():
    # échoue sur timeout testcase 13 et 14
    T = int(input())
    for _ in range(T):
        n = int(input())
        solve(n)


def main():
    import os
    if os.getenv('OUTPUT_PATH', '').startswith("/run-"):
        hackerrank()
    else:
        p085()


if __name__ == '__main__':
    main()

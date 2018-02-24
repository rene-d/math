"""
Goldbach's other conjecture

https://projecteuler.net/problem=46
"""

from eulerlib import Crible, exact_sqrt

carres = [i * i for i in range(100)]
crible = Crible(10000)
premiers = crible.liste()

for i in range(35, 10000, 2):

    if crible.est_premier(i):
        continue

    conjecture = False
    for p in premiers:
        if p >= i - 2:
            break

        if (i - p) // 2 in carres:
            r, _ = exact_sqrt((i - p) // 2)
            # print("{} = {} + 2 * {}²".format(i, p, r))
            conjecture = True
            break

    if conjecture is False:
        print(i)
        # print("{} ne pas s'écrire sous la forme p+n²".format(i))
        break

"""

https://projecteuler.net/problem=30
"""

resultat = 0
for i in range(2, 10**6):
    n = i
    s = 0
    for j in range(6):
        n, r = divmod(n, 10)
        s += r ** 5
        if n == 0:
            break
    if s == i:
        # print(i)
        resultat += i
print(resultat)

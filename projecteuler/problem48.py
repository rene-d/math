"""
Self powers

https://projecteuler.net/problem=48
"""

resultat = 0
for i in range(1, 1001):
    resultat = (resultat + pow(i, i)) % 10000000000
print(resultat)

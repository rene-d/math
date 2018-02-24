"""
Distinct powers

https://projecteuler.net/problem=29
"""

resultat = set()
for a in range(2, 101):
    for b in range(2, 101):
        resultat.add(a ** b)
print(len(resultat))

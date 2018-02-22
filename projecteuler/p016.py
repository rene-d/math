"""
Power digit sum

https://projecteuler.net/problem=16
"""

# aucun intérêt puisque Python gère les entiers longs
print(sum(int(c) for c in str(2 ** 1000)))

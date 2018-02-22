"""
Number spiral diagonals

https://projecteuler.net/problem=28
"""

somme = 1
n = 1
for i in range(1, 1 + 1001 // 2):
    for _ in range(4):
        n += i * 2
        somme += n
print(somme)

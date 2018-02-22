"""
"""

p = 0
for i in range(100, 1000):
    for j in range(i, 1000):
        n = i * j
        if str(n) == str(n)[::-1]:
            if p < n:
                p = n
print(p)

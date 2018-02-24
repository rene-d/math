"""
Lexicographic permutations

https://projecteuler.net/problem=24
"""

import itertools

for idx, perm in enumerate(itertools.permutations("0123456789")):
    if idx == 1000000 - 1:
        print(''.join(perm))
        break

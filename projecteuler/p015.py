"""
Lattice paths

https://projecteuler.net/problem=15
"""

import math

"""
Cf. https://en.wikipedia.org/wiki/Lattice_path
"""


def C(n, k):
    """ Coefficient binomial """
    return math.factorial(n) // math.factorial(k) // math.factorial(n - k)


print(C(20 + 20, 20))

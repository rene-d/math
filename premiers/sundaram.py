"""
Crible de Sundaram

https://en.wikipedia.org/wiki/Sieve_of_Sundaram
"""

from eratosthene import bitfield


class Sundaram:
    """
    """

    def __init__(self, n_max):
        self.n_max = n_max

        self.maximum = maximum = (n_max - 3) // 2 + 1
        self.crible = crible = bitfield(maximum)

        for i in range(1, maximum + 1):
            for j in range(1, i + 1):
                m = i + j + 2 * i * j
                if m > maximum:
                    break
                crible.set(m - 1, True)

    def liste(self):
        premiers = [2]
        for i in range(1, self.maximum + 1):
            if not self.crible.is_set(i - 1):
                premiers.append(2 * i + 1)
        return premiers

    def est_premier(self, n):
        if n == 2:
            return True
        elif n % 2 == 0 or n < 2:
            return False
        else:
            return not self.crible.is_set((n - 3) // 2)

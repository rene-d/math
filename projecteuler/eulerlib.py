"""
Fonctions pour les problèmes de Project Euler
"""


def est_premier(n):
    """ teste si le nombre est premier """
    if n <= 1:
        return False
    elif n == 2:
        return True
    elif n % 2 == 0:
        return False
    else:
        i = 3
        while i * i <= n:
            if n % i == 0:
                return False
            i = i + 2
        return True


class bitfield:
    """
    Implémentation d'un bitfield à stockage optimisé
    """

    def __init__(self, taille):
        self.taille = taille
        self.bits = bytearray((taille + 7) // 8)

    def set(self, pos, val):
        """ poitionne le bit `pos` à `val` """
        assert pos >= 0 and pos < self.taille
        if val is True:
            self.bits[pos // 8] = self.bits[pos // 8] | (1 << (pos % 8))
        else:
            self.bits[pos // 8] = self.bits[pos // 8] & ~(1 << (pos % 8))

    def is_set(self, pos):
        """ lit l'état du bit `pos` """
        assert pos >= 0 and pos < self.taille
        return (self.bits[pos // 8] & (1 << (pos % 8))) != 0

    def __getitem__(self, key):
        return self.is_set(key)

    def __setitem__(self, key, value):
        return self.set(key, value)


class Crible:
    """ Crible d'Eratosthène optimisé """

    def __init__(self, n_max):
        self.n_max = n_max

        self.maximum = n = (n_max - 3) // 2 + 1
        self.crible = crible = bitfield(n)

        i = 0
        while i < n:
            while i < n:
                if not crible.is_set(i):
                    break
                i += 1

            k = 3
            while True:
                j = k * i + 3 * (k - 1) // 2
                if j >= n:
                    break
                crible.set(j, True)
                k += 2

            i += 1

    def liste(self):
        premiers = [2]
        for i in range(1, self.maximum + 1):
            if not self.crible.is_set(i - 1):
                premiers.append(2 * i + 1)
        return premiers

    def est_premier(self, n):
        if n == 2:
            return True
        elif n % 2 == 0 or n <= 1:
            return False
        else:
            # n est impair et >= 3
            assert n < self.n_max
            return not self.crible.is_set((n - 3) // 2)


def decompose(n):
    """ décomposition d'un nombre en facteurs premiers """

    facteurs = []

    i = 2
    while i * i <= n:
        while n % i == 0:
            n = n // i
            facteurs.append(i)
        if i >= 3:
            i += 2
        else:
            i += 1

    if n != 1:
        facteurs.append(n)

    return facteurs


def reduit_polynome(facteurs):
    """ réduit les facteurs premiers en puissance p*p*...*p en p^n """

    nb_facteurs = len(facteurs)
    facteurs_reduits = []
    i = 0
    while i < nb_facteurs:
        f = facteurs[i]
        e = 1
        i += 1
        while i < nb_facteurs and f == facteurs[i]:
            e += 1
            i += 1
        if e == 1:
            facteurs_reduits.append('{}'.format(f))
        else:
            facteurs_reduits.append('{}^{}'.format(f, e))

    return facteurs_reduits


def decompose2(n):
    """ réduit les facteurs premiers en puissance p*p*...*p en p^n """

    facteurs = decompose(n)
    nb_facteurs = len(facteurs)
    facteurs_reduits = []
    i = 0
    while i < nb_facteurs:
        f = facteurs[i]
        e = 1
        i += 1
        while i < nb_facteurs and f == facteurs[i]:
            e += 1
            i += 1
        if e == 1:
            facteurs_reduits.append((f, 1))
        else:
            facteurs_reduits.append((f, e))

    return facteurs_reduits


def affiche(n):
    """ affiche la décomposition en facteurs premiers d'un nombre """

    facteurs = decompose(n)
    facteurs_reduits = reduit_polynome(facteurs)

    def expo(x):
        exposants = '⁰¹²³⁴⁵⁶⁷⁸⁹'
        i = x.find('^')
        if i == -1:
            return x
        else:
            return x[0:i] + ''.join([exposants[int(c)] for c in x[i + 1:]])

    expr1 = ' ⨯ '.join([str(i) for i in facteurs])
    expr2 = ' ⨯ '.join([expo(i) for i in facteurs_reduits])

    print('{} = {} = {}'.format(n, expr1, expr2))

    # auto-test !
    assert n == eval('*'.join([str(i) for i in facteurs]))
    assert n == eval('*'.join([i.replace("^", "**") for i in facteurs_reduits]))


def pgcd(a, b):
    """
    retourne le plus grand commun diviseur de deux entiers donnés (algorithme d'Euclide)
    """
    while b != 0:
        a, b = b, a % b
    return a


class Fraction:
    """
    calculs sur ℚ (ensemble des entiers rationnels)
    """

    def __init__(self, num, den=1):
        assert den != 0
        self.num = num
        self.den = den
        self.simplifie()

    def __str__(self):
        if self.den == 1:
            return str(self.num)
        else:
            return "{}/{}".format(self.num, self.den)

    def simplifie(self):
        d = pgcd(self.num, self.den)
        if d != 1:
            self.num = self.num // d
            self.den = self.den // d

    def __add__(self, r):
        if isinstance(r, Fraction):
            n = Fraction(self.num * r.den + self.den * r.num, self.den * r.den)
        elif isinstance(r, int):
            n = Fraction(self.num + self.den * r, self.den)
        else:
            raise TypeError
        n.simplifie()
        return n

    def __sub__(self, r):
        if isinstance(r, Fraction):
            n = Fraction(self.num * r.den - self.den * r.num, self.den * r.den)
        elif isinstance(r, int):
            n = Fraction(self.num - self.den * r, self.den)
        else:
            raise TypeError
        n.simplifie()
        return n

    def __mul__(self, other):
        if isinstance(other, Fraction):
            n = Fraction(self.num * other.num, self.den * other.den)
        elif isinstance(other, int):
            n = Fraction(self.num * other, self.den)
        else:
            raise TypeError
        n.simplifie()
        return n

    def __truediv__(self, other):
        """ f / g ou f / 1 """
        if isinstance(other, Fraction):
            n = Fraction(self.num * other.den, self.den * other.num)
        elif isinstance(other, int):
            n = Fraction(self.num, self.den * other)
        else:
            raise TypeError
        n.simplifie()
        return n

    def __radd__(self, other):
        """ cas de 1 + f """
        return self.__add__(other)

    def __rsub__(self, other):
        """ cas de 1 - f """
        new = self.__sub__(other)
        new.num = -new.num
        return new

    def __rtruediv__(self, other):
        """ 1 / f """
        if isinstance(other, int):
            new = Fraction(self.den * other, self.num)
        else:
            raise TypeError
        new.simplifie()
        return new

    def __neg__(self):
        return Fraction(-self.num, self.den)


# https://gist.github.com/tobin/11233492
def exact_sqrt(x):
    """Calculate the square root of an arbitrarily large integer.

    The result of exact_sqrt(x) is a tuple (a, r) such that a**2 + r = x, where
    a is the largest integer such that a**2 <= x, and r is the "remainder".  If
    x is a perfect square, then r will be zero.

    The algorithm used is the "long-hand square root" algorithm, as described at
    http://mathforum.org/library/drmath/view/52656.html

    Tobin Fricke 2014-04-23
    Max Planck Institute for Gravitational Physics
    Hannover, Germany
    """

    N = 0
    a = 0

    # We'll process the number two bits at a time, starting at the MSB
    L = x.bit_length()
    L += (L % 2)

    for i in range(L, -1, -1):

        # Get the next group of two bits
        n = (x >> (2 * i)) & 0b11

        # Check whether we can reduce the remainder
        if ((N - a * a) << 2) + n >= (a << 2) + 1:
            b = 1
        else:
            b = 0

        a = (a << 1) + b
        N = (N << 2) + n

    return (a, N - a * a)

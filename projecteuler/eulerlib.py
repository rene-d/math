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


class bitset:
    """
    Implémentation d'un bitset à stockage optimisé
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
        self.crible = crible = bitset(n)
        self._premiers = None
        self._phi = None

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
        if self._premiers is None:
            premiers = [2]
            for i in range(1, self.maximum + 1):
                if not self.crible.is_set(i - 1):
                    premiers.append(2 * i + 1)
            self._premiers = premiers
        return self._premiers

    def est_premier(self, n):
        if n == 2:
            return True
        elif n % 2 == 0 or n <= 1:
            return False
        else:
            # n est impair et >= 3
            if n >= self.n_max:
                return est_premier(n)

            assert n < self.n_max
            return not self.crible.is_set((n - 3) // 2)


    def EulerPhi(self):
        if self._phi is None:
            n_max = self.n_max
            phi = [i for i in range(n_max)]
            for p in self.liste():
                for i in range(p, n_max, p):
                    phi[i] //= p
                    phi[i] *= p - 1
            self._phi = phi
        return self._phi


def decompose(n):
    """ décomposition d'un nombre en facteurs premiers """

    # étape 1: trouve tous les facteurs premiers
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

    # étape 2: groupe les facteurs identiques
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

    def expo(f):
        exposants = '⁰¹²³⁴⁵⁶⁷⁸⁹'
        if f[1] == 1:
            return str(f[0])
        else:
            return str(f[0]) + ''.join([exposants[int(c)] for c in str(f[1])])

    return ' ⨯ '.join([expo(f) for f in decompose(n)])


def pgcd(a, b):
    """
    retourne le plus grand commun diviseur de deux entiers donnés (algorithme d'Euclide)
    """
    while b != 0:
        a, b = b, a % b
    return a


def ppcm(nombres):
    """ retourne le plus petit commun multipe d'une liste de nombre """
    p = nombres[0]
    for n in nombres[1:]:
        p = p * n // pgcd(p, n)
    return p


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

    return a, N - a * a


def diviseurs(n):
    div = [1]
    i = 2
    while i * i <= n:
        q, r = divmod(n, i)
        if r == 0:
            div.append(i)
            if i != q:
                div.append(q)
        i += 1
    div.append(n)
    return div


def EulerPhi(n):
    """ calcul de l'Indicatrice d'Euler φ(n) ou totient(n) """
    phi = n
    i = 2
    while i * i <= n:
        if n % i == 0:
            phi -= phi // i
        while n % i == 0:
            n = n // i
        if i != 2:
            i += 2
        else:
            i += 1
    if n > 1:
        phi -= phi // n
    return phi


def EulerPhi_basique(n):
    """ calcul de φ(n) à partir de la formule φ(n) = ∏ (pᵢ-1)*pᵢ^(kᵢ-1) """
    f = decompose(n)
    phi = 1
    for i in f:
        phi *= (i[0] - 1) * (i[0] ** (i[1] - 1))
    return phi

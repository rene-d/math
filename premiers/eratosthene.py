"""
Crible d'Eratosthène
"""


class bitfield:
    """
    Implémentation d'un bitfield
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


def cribler(n_max):
    """
    Crible d'Eratosthène
    """

    # crée un bitfield pour stocker la primalité des entiers de 2 à n
    crible = bitfield(n_max + 1)
    premiers = []

    i = 2
    while i <= n_max:

        # trouve le prochain premier
        while i <= n_max:
            if not crible.is_set(i):
                premiers.append(i)
                break
            i += 1

        # annule les multiples de i
        j = 2 * i
        while j <= n_max:
            crible.set(j, True)
            j += i

        i += 1

    return premiers


def cribler_opti(n_max):
    """
    Version optimisée: on ne considère pas les nombres pairs,
    ni les multiples pairs lors de l'élimination.
    C'est apparemment le Crible de Sundaram: https://en.wikipedia.org/wiki/Sieve_of_Sundaram
    """

    # n_max impair (ex: 11) => (n-3)/2+1 nombres impairs à considérer
    # n_max par (ex: 12) => (n-1-3)/2+1 nombres impairs à considérer
    n = (n_max - 3) // 2 + 1

    # on va stocker uniquement les nombres impairs de 3 à n_max
    crible = bitfield(n)
    premiers = [2]

    # i: itérateur dans le bitfield de taille n
    # la formule qui donne l'impair en fonction de i est : impair ← 2*i+3
    i = 0   # vaut pour le premier impair à tester, 3
    while i < n:

        # trouve le prochain premier
        while i < n:
            if not crible.is_set(i):
                premiers.append(i * 2 + 3)
                break
            i += 1

        # annule les multiples IMPAIRS du nombre représenté par i
        k = 3   # multiplicateur
        while True:
            # la formule ci-après mérite une petite explication:
            #   soit u l'impair associé à l'itérateur i
            #       u = 2*i+3
            #   soit v le multiple de u:
            #       v = k*u = k*(2*i+3) = 2*k*i+3*k
            #   soit j l'itérateur associé à v:
            #       v = 2*j+3
            #   d'où:
            #       j = (v-3)/2 = (2*k*i+3*k-3)/2 = k*i+3*(k-1)/2
            #   k est toujours impair, donc k-1 toujours pair
            #   et par conséquant divisible par 2
            j = k * i + 3 * (k - 1) // 2
            if j >= n:
                break
            crible.set(j, True)
            # passe au multiple suivant
            k += 2

        # passe à l'impair suivant
        i += 1

    return premiers


def main():
    import cProfile as prof

    print("cribler".center(90, "-"))
    prof.run('c1 = cribler(10000)')

    print("cribler_opti".center(90, "-"))
    prof.run('c2 = cribler_opti(10000)')

    assert c1 == c2     # noqa  c1 et c2 sont des globaux définis par les run() ci-dessus


if __name__ == '__main__':
    main()

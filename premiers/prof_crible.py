import eratosthene
import sundaram
from liste_premiers import est_premier
import timeit


def mesure(stmt, globals):
    t = timeit.Timer(stmt, globals=globals)
    return t.timeit(1)


def prof_normal_opti():
    """
    comparaison du crible basique et la version optimisée
    """
    print("liste des premiers <= N".center(90, "="))

    N = 100000
    locals = {"cribler": lambda: eratosthene.cribler(N),
              "cribler_opti": lambda: eratosthene.cribler_opti(N)}

    t = mesure('global c1; c1 = cribler()', locals)
    print("{:<15s} : test avec N={} → {:.6f} s".format("cribler", N, t))

    t = mesure('global c2; c2 = cribler_opti()', locals)
    print("{:<15s} : test avec N={} → {:.6f} s".format("cribler_opti", N, t))

    assert locals['c1'] == locals['c2']


def prof_opti_sundaram(N=100000):
    """
    """
    print("crible opti vs. Sundaram".center(90, "="))

    locals = {"sundaram": lambda: sundaram.Sundaram(N),
              "eratosthene": lambda: eratosthene.Crible(N)}

    t = mesure('global c2; c2 = eratosthene()', locals)
    print("{:<15s} : test avec N={} → {:.6f} s".format("cribler_opti", N, t))

    t = mesure('global c1; c1 = sundaram()', locals)
    print("{:<15s} : test avec N={} → {:.6f} s".format("sundaram", N, t))

    assert locals['c1'].liste() == locals['c2'].liste()


def prof_crible_test(N=100000):
    """
    """
    print("test primalité pour tous les entiers <= N".center(90, "="))

    def t1():
        c = eratosthene.Crible(N)
        for i in range(0, N):
            c.est_premier(i)

    def t2():
        for i in range(0, N):
            est_premier(i)

    t = mesure("run()", {"run": t1})
    print("{:<15s} : test avec N={} → {:.6f} s".format("crible", N, t))

    t = timeit.timeit("run()", number=1, globals={"run": t2})
    print("{:<15s} : test avec N={} → {:.6f} s".format("test primalité", N, t))


if __name__ == '__main__':
    prof_crible_test()
    prof_opti_sundaram()
    prof_normal_opti()

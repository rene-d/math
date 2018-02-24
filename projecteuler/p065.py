"""
Convergents of e

https://projecteuler.net/problem=65
"""

from fractions import Fraction


def fraction_continue_e(f, terme):
    """ fraction continue de e """

    # e = [2; 1,2,1, 1,4,1, 1,6,1 , ... , 1,2k,1, ...].
    if terme == 1:
        k = 2                   # le coef [2; ...
    elif terme % 3 == 0:
        k = 2 * (terme // 3)    # le coef x,2k,x
    else:
        k = 1                   # les coefs 1,x,1

    if f == 0:
        return Fraction(k, 1)

    return k + 1 / f


f = Fraction(0)
for i in range(100, 0, -1):
    f = fraction_continue_e(f, i)
print(sum(int(d) for d in str(f.numerator)))

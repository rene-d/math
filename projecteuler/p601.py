"""
Divisibility streaks

https://projecteuler.net/problem=601
"""

from eulerlib import ppcm

"""
streak(n) = k
    n+1 ≡ 0 mod 2       ⟹   n-1+2 ≡ 0 mod 2     ⟹   n-1 ≡ 0 mod 2
    n+2 ≡ 0 mod 3       ⟹   n-1+3 ≡ 0 mod 3     ⟹   n-1 ≡ 0 mod 3
    ...
    n+k ≡ 0 mod (k+1)   ⟹   n-1+k-1 ≡ 0 mod k   ⟹   n-1 ≡ 0 mod k
    n+k+1 ≢ 0 mod (k+2)
donc n-1 est divisible par 1,2,3,...,k et par conséquent par le ppcm(1..k) ①
mais ne doit pas être divisible par ppcm(1..(k+1)) ②
1 < n < N ⟹ N-2 valeurs doivent vérifier ① et ②
"""


def P(s, N):
    return (N - 2) // ppcm(range(1, s + 1)) - (N - 2) // ppcm(range(1, s + 2))


assert P(3, 14) == 1
assert P(6, 10 ** 6) == 14286

print(sum(P(i, 4 ** i) for i in range(1, 32)))

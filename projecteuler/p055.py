"""
Lychrel numbers

https://projecteuler.net/problem=55
"""


def palindrome(n):
    p = 0
    q = n
    while q != 0:
        q, r = divmod(q, 10)
        p = p * 10 + r
    return p


def lychrel(n):
    # on commence une itération: les palindromes ne sont pas
    # automatiquement des nombres de Lychrel
    p = n + palindrome(n)
    for i in range(50):
        q = palindrome(p)
        if p == q:
            return 0
        p += q
    return 1


print(sum([lychrel(i) for i in range(1, 10001)]))

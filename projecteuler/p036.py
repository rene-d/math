"""
Double-base palindromes

The decimal number, 585 = 10010010012 (binary), is palindromic in both bases.

Find the sum of all numbers, less than one million, which are palindromic in base 10 and base 2.

(Please note that the palindromic number, in either base, may not include leading zeros.)

https://projecteuler.net/problem=36
"""


def est_palindrome(n, base):
    m = 0
    q = n
    while q != 0:
        q, r = divmod(q, base)
        m = r + m * base
    return m == n


resultat = 0
for n in range(1, 1000000, 2):
    if est_palindrome(n, 10) and est_palindrome(n, 2):
        resultat += n
print(resultat)

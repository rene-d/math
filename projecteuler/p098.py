"""
Anagramic squares

https://projecteuler.net/problem=98
"""

import math

words = [s.replace('"', '') for s in open("p098_words.txt").read().split(',')]

# calcule les carrés de 16 à 999950884 inclus (carrés de 2 à 9 chiffres)
squares_n = {}
is_squares_n = {}
for j in range(2, 10):

    def same_digits(i):
        digits = [False] * 10
        while i != 0:
            i, r = divmod(i, 10)
            if digits[r]:
                return True
            digits[r] = True
        return False

    # nota: les j%2 compensent le fait que 10^i soit un carré ou pas
    a = int(math.sqrt(10 ** (j - 1))) + 1 - (j % 2)
    b = int(math.sqrt(10 ** j)) + (j % 2)
    s = []
    for i in range(a, b):
        if not same_digits(i * i):
            s.append(i * i)

    # table des carrés à j chiffres
    squares_n[j] = s

    # set pour vérifier si un nombre est carré
    is_squares_n[j] = set(i for i in s)


# itérateur parmi tous les anagrammes de words
def anagram():
    anagrams = {}
    for s in words:
        key = ''.join(sorted(s))
        v = anagrams.get(key, None)
        if v is not None:
            v.append(s)
        else:
            anagrams[key] = [s]
    for _, v in anagrams.items():
        if len(v) > 1:
            yield v


smax = 0

for a in anagram():

    n = len(a[0])
    squares = squares_n[n]
    is_squares = is_squares_n[n]

    # parcourt tous les carrés de même longueur que le mot
    for square in squares:

        # table de substitution lettre du mot -> chiffre du carré
        square1 = str(square)
        subst = {}
        for i, c in enumerate(a[0]):
            subst[c] = square1[i]

        # pour tous les anagrammes du moy
        for w in a[1:]:
            # applique la substitution
            square2 = int(''.join(subst[c] for c in w))
            if square2 not in is_squares:
                continue

            # on a une solution, on garde que le max
            smax = max(square, square2, smax)
            print(a[0], w, "->", square, square2, subst)

print(smax)

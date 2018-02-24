"""
Coded triangle numbers

The nth term of the sequence of triangle numbers is given by, tn = ½n(n+1); so the first ten
triangle numbers are:

1, 3, 6, 10, 15, 21, 28, 36, 45, 55, ...

By converting each letter in a word to a number corresponding to its alphabetical position and
adding these values we form a word value. For example, the word value for SKY is
19 + 11 + 25 = 55 = t10. If the word value is a triangle number then we shall call the word a
triangle word.

Using words.txt (right click and 'Save Link/Target As...'), a 16K text file containing nearly
two-thousand common English words, how many are triangle words?

https://projecteuler.net/problem=42
"""

words = []
triangles = []

# je sais que ça suffit :) mais on pourrait évaluer la borne max
# en fonction de la liste de mots
for n in range(1, 20):
    triangles.append(n * (n + 1) // 2)

f = open("p042_words.txt")
for word in f.read().split(","):
    words.append(word.replace('"', ''))

resultat = 0
for word in words:
    s = sum(ord(c) - ord('A') + 1 for c in word)
    if s in triangles:
        resultat += 1
print(resultat)

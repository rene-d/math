"""

https://projecteuler.net/problem=22
"""

f = open("p022_names.txt")
pos = 0
somme = 0
names = []
for name in f.read().split(","):
    names.append(name.replace('"', ''))
for name in sorted(names):
    pos += 1
    score = pos * sum(ord(c) - 64 for c in name)
    somme += score
print(somme)

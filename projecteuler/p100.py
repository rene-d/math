"""
Arranged probability

https://projecteuler.net/problem=100
"""

"""
Quelques explications:

P(BB) = p = b/(r+b) * (b-1)/(r+b-1)
avec b=nombre de disques bleu et r=nombre de disques rouges

L'arrangement demandé est p = 1/2
Ce qui conduit à (en exprimant b en fonction de r et en ne retenant que la solution positive):
b = (1+2r+√(8r²+1))/2

Ainsi, 8r²+1 doit être :
- un carré
- impair pour que 1+2r+√ soit divisible par 2

∃𝒙 ∈ ℕ tel que x²=8r²+1
On peut écrire x²-8r²=1
C'est une équation de Pell-Fermat avec n=8

Les solutions peuvent se trouver par récurrence:
cf. https://fr.wikipedia.org/wiki/Équation_de_Pell-Fermat#Cas_m_=_1
"""

# solution minimale de l'équation de Pell x²-8y²=1
# cf. http://mathworld.wolfram.com/PellEquation.html
x1, y1 = 3, 1

x, y = x1, y1
for _ in range(100):

    if x % 2 == 1:
        r = y
        b = (1 + 2 * r + x) // 2
        if r + b > 10 ** 12:
            print(b)
            break

    # formule de récurrence
    x, y = x * x1 + 8 * y * y1, x * y1 + y * x1

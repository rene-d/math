"""
Diophantine reciprocals I

https://projecteuler.net/problem=108
"""

# l'astuce consiste à voir que 1/x + 1/y = 1/n se transforme en n² = r*s avec r=x-n et s=y-n
# dénombrer (x,y) revient à compter les couples (r,s)
# c'est-à-dire le nombre de diviseurs de n²
# pour que les couples (r,s) soient uniques, il faut diviser par 2 (r*s = s*r)

# la deuxième astuce est de voir que compter les diviseurs de n² peut se faire assez rapidement
# avec la décomposition en nombres premiers


def decompose(n):
    """ décomposition d'un nombre en facteurs premiers """
    facteurs = {}
    i = 2
    while i * i <= n:
        while n % i == 0:
            n = n // i
            facteurs[i] = facteurs.get(i, 0) + 1
        if i >= 3:
            i += 2
        else:
            i += 1
    if n > 1:
        facteurs[n] = facteurs.get(n, 0) + 1
    return facteurs


n = 0
while True:
    n += 1
    p = 1
    for _, e in decompose(n).items():
        p *= 2 * e + 1                  # nombre de diviseurs de n²
    if (p + 1) // 2 >= 1000:            # compte-tenu du calcul de la ligne précédente, p est toujours impair!
        print(n)
        break

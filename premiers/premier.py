"""
Test la primalité d'un nombre
"""

# saisie du nombre
n = input('entrez le nombre à tester : ')

# convertit la chaîne de caractères en entier
n = int(n)

# teste si le nombre est pair (% = reste de la division entière)
if n <= 1:
    print(n, "n'est pas premier")
elif n == 2:
    print(n, "est premier !")
elif n % 2 == 0:
    print(n, "est pair")
else:
    i = 3
    est_premier = True
    while i * i < n:
        if n % i == 0:
            print(n, "est multiple de", i)
            est_premier = False
        i = i + 2
    if est_premier:
        print(n, "est premier !")

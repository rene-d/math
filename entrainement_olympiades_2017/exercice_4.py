#! /usr/bin/env python3

"""
EXERCICE 4 : Tous impairs
Quelle est la somme de tous les nombres entiers dont l’écriture décimale ne comporte que les chiffres impairs, tous utilisés une et une seule fois ?
"""

# compte le nombre de fois que le chiffre apparaît dans la chaîne
def compte(chaine, chiffre):
    return chaine.count("%d" % int(chiffre))

total = 0
nombre = 0

# pour tous les nombres de 0 à 99999
for i in range(100000):

    # chaine contient les 5 chiffres du nombre i
    chaine = "%05d" % i

    # est-ce qu'il y a un et un seul chiffre 1 dans le nombre i ?
    if compte(chaine, 1) != 1:
        continue    # non: on continue la boucle

    if compte(chaine, 3) != 1:
        continue

    if compte(chaine, 5) != 1:
        continue

    if compte(chaine, 7) != 1:
        continue

    if compte(chaine, 9) != 1:
        continue

    total += i
    nombre += 1

print("nombre: ", nombre)
print("somme:  ", total)

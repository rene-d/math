"""
Affiche la liste des nombres premiers inférieurs à 300
"""


# teste si le nombre est premier
def premier(n):
    if n <= 1:
        return False
    elif n == 2:
        return True
    elif n % 2 == 0:
        return False
    else:
        i = 3
        while i * i <= n:
            if n % i == 0:
                return False
            i = i + 2
        return True


for n in range(2, 301):
    if premier(n):
        print("%5d est premier" % n)

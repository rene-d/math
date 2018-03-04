"""
Powerful digit counts

https://projecteuler.net/problem=63
"""

# nota: les bornes 200 et 500 sont empiriques,
# mais après les nombres deviennent trop grands
nb = 0
for i in range(1, 200):
    for e in range(1, 500):
        n = i ** e
        if len(str(n)) == e:
            # print("{:>30} = {} ^ {}".format(n, i, e))
            nb += 1
print(nb)

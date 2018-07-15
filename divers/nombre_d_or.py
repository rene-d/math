#! /usr/bin/env python3

# Montre que le rapport de deux termes consécutifs de la suite de Fibonacci
# converge vers le Nombre d'Or

from time import sleep
from math import sqrt

a = 1
b = 1
n = 0

Nombre_Or = (1 + sqrt(5)) / 2

print("{:>3} | {:>11} + {:>11} = {:>11} | {:^16} {:^15}".format("N°", "a", "b", "c", "b / a", "erreur"))
print("----+-----------------------------------------+---------------------------------")

while n < 50:
    n += 1

    c = a + b

    print("{:3} | {:11} + {:11} = {:11} | φ = {:.10f} {:15.12f}".format(n, a, b, c, b / a, b / a - Nombre_Or))

    a = b
    b = c

    sleep(0.2)

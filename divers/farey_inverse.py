# https://fr.wikipedia.org/wiki/Suite_de_Farey
# Code pour engendrer une Suite de Farey d'ordre N dans l'ordre descendant
N = 8
NumTerms = 1
A, B = 1, 1
C, D = N - 1, N
print(A, B)
while A > 0:
      NumTerms += 1
      K = (N + B) // D
      E, F = K * C - A, K * D - B
      A, B = C, D
      C, D = E, F
      print(A, B)
print(NumTerms)
"""
Monopoly odds

https://projecteuler.net/problem=84
"""


import random


class Cartes:
    """ permet de tirer dans un jeu cartes """
    def __init__(self, taille):
        self.cartes = list(range(taille))
        random.shuffle(self.cartes)
        self.index = 0
        self.taille = taille

    def tire(self):
        """ retourne un numéro de carte entre 1 et taille """
        c = self.cartes[self.index]
        self.index = (self.index + 1) % self.taille
        return c + 1


class Monopoly:
    """ définition des cases du Monopoly """
    GO = 0
    A1 = 1
    CC1 = 2
    A2 = 3
    T1 = 4
    R1 = 5
    B1 = 6
    CH1 = 7
    B2 = 8
    B3 = 9
    JAIL = 10
    C1 = 11
    U1 = 12
    C2 = 13
    C3 = 14
    R2 = 15
    D1 = 16
    CC2 = 17
    D2 = 18
    D3 = 19
    FP = 20
    E1 = 21
    CH2 = 22
    E2 = 23
    E3 = 24
    R3 = 25
    F1 = 26
    F2 = 27
    U2 = 28
    F3 = 29
    G2J = 30
    G1 = 31
    G2 = 32
    CC3 = 33
    G3 = 34
    R4 = 35
    CH3 = 36
    H1 = 37
    T2 = 38
    H2 = 39


def suivant(pion, cases):
    """ avance le pion à la prochain case de cases """
    for case in cases:
        if pion < case:
            return case
    return cases[0]


FACES = 4                               # nombre de faces des dés
JETS = 1000000                          # nombre de jets de dés
visites = [0] * 40                      # nombre de visites sur chaque case
pion = 0                                # position sur joueur entre 0 et 39
doubles = 0                             # nombre de jets doubles consécutifs
CC = Cartes(16)                         # cartes communauté
CH = Cartes(16)                         # cartes chance

for i in range(JETS):

    # tire les dés
    de1 = random.randint(1, FACES)
    de2 = random.randint(1, FACES)
    if de1 == de2:
        doubles += 1
    else:
        doubles = 0

    # 3 doubles consécutifs ?
    if doubles == 3:
        pion = Monopoly.JAIL
        doubles = 0
    else:
        # avance le pion
        pion = (pion + de1 + de2) % 40

    # carte Chance
    if pion in [Monopoly.CH1, Monopoly.CH2, Monopoly.CH3]:
        c = CH.tire()
        if c == 1:
            pion = Monopoly.GO
        elif c == 2:
            pion = Monopoly.JAIL
            doubles = 0
        elif c == 3:
            pion = Monopoly.C1
        elif c == 4:
            pion = Monopoly.E3
        elif c == 5:
            pion = Monopoly.H2
        elif c == 6:
            pion = Monopoly.R1
        elif c == 7 or c == 8:
            pion = suivant(pion, [Monopoly.R1, Monopoly.R2, Monopoly.R3, Monopoly.R4])
        elif c == 9:
            pion = suivant(pion, [Monopoly.U1, Monopoly.U2])
        elif c == 10:
            pion = (pion - 3) % 40
            # possibilités: T1 D3 CC3

    # carte Communauté
    if pion in [Monopoly.CC1, Monopoly.CC2, Monopoly.CC3]:
        c = CC.tire()
        if c == 1:
            pion = Monopoly.GO
        elif c == 2:
            pion = Monopoly.JAIL
            doubles = 0

    if pion == Monopoly.G2J:
        pion = Monopoly.JAIL
        doubles = 0

    visites[pion] += 1

modal = sorted(list((v, "%02d" % i) for i, v in enumerate(visites)), reverse=True)
print(''.join(p for _, p in modal[0:3]))


# for k, v in modal:
#     print("{:.3f} {} {}".format(k / JETS * 100, v,
#                                 [i for i in dir(Monopoly) if getattr(Monopoly, i) == int(v)][0]))

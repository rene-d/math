#! /usr/bin/env python3
# rené 2018

""" courbes fractales
https://fr.wikipedia.org/wiki/Flocon_de_Koch
"""

import sys, time, math
import tkinter as tk
from typing import NamedTuple


class point2D(NamedTuple):
    x: float
    y: float


class pointF(NamedTuple):
    x: float
    y: float
    sens: bool


def sqr(x):
    return x * x


def sqrt(x):
    return math.sqrt(x)


class Fractale:

    def __init__(self, nom):
        if nom == "Mandelbrot":
            # «courbe de Mandelbrot» : exemple d'une courbe de Peano
            self.gen = [
                pointF(    -1,                 0, False),    # 0
                pointF(-2 / 3,       sqrt(3) / 3, True),     # 1
                pointF(-1 / 3,   2 * sqrt(3) / 3, True),     # 2
                pointF( 1 / 3,   2 * sqrt(3) / 3, True),     # 3
                pointF( 2 / 3,       sqrt(3) / 3, True),     # 4
                pointF( 1 / 3,   4 * sqrt(3) / 9, False),    # 5
                pointF(     0,   5 * sqrt(3) / 9, False),    # 6
                pointF(-1 / 3,   4 * sqrt(3) / 9, False),    # 7
                pointF(-1 / 3,   2 * sqrt(3) / 9, True),     # 8
                pointF( 1 / 3,   2 * sqrt(3) / 9, True),     # 9
                pointF(    0,        sqrt(3) / 9, False),    # 10
                pointF(-1 / 3,                 0, False),    # 11
                pointF( 1 / 3,                 0, True),     # 12
                pointF(     1,                 0, True),     # 13
            ]

        elif nom == "Koch":
            self.gen = [
                pointF(-1,           0, True),    # 0
                pointF(-1/3,         0, True),    # 1
                pointF(0,  sqrt(3) / 3, True),    # 2
                pointF(1/3,          0, True),    # 3
                pointF(1,            0, True),    # 4
            ]

        elif nom == "Cesaro":
            alpha = math.radians(85)        # angle de la pointe, 60° pour von Koch
            a = 1 / (1 + math.cos(alpha))   # longueur de chaque segment _/\_
            self.gen = [
                pointF(1, 0, True),                     # 0
                pointF(-1 + a, 0, True),                # 1
                pointF(0, a * math.sin(alpha), True),   # 2
                pointF(1 - a, 0, True),                 # 3
                pointF(1, 0, True),                     # 4
            ]

        elif nom == "Peano":
            self.gen = [
                pointF(-3, 0, True),
                pointF(-1, 0, True),
                pointF(-1, 2, True),
                pointF(1, 2, True),
                pointF(1, 0, True),
                pointF(1, -2, True),
                pointF(-1, -2, True),
                pointF(-1, 0, True),
                pointF(1, 0, True),
                pointF(3, 0, True),
            ]


class Crt:
    def __init__(self):
        self.root = tk.Tk()
        self.canvas = tk.Canvas(self.root, width=1024, height=768,
                                borderwidth=0, highlightthickness=0)
        self.canvas.grid()

    def repere(self, x_min, x_max, y_min, y_max):
        bounds = [0, 0, 1024, 768]
        self.coords = [x_min,
                       y_max,
                       (bounds[2] - bounds[0]) / (x_max - x_min),
                       (bounds[3] - bounds[1]) / (y_min - y_max)]

    def conv(self, p):
        return (p.x - self.coords[0]) * self.coords[2], (p.y - self.coords[1]) * self.coords[3]

    def ligne(self, p1, p2, fill="red"):
        x1, y1 = self.conv(p1)
        x2, y2 = self.conv(p2)
        self.canvas.create_line(x1, y1, x2, y2, fill=fill)       # dash=(2,16)

    def clear(self):
        self.canvas.delete("all")

    def bind_key(self, callback):
        self.canvas.bind("<Key>", callback)


class Dessine:
    def __init__(self, nom):
        self.crt = Crt()
        self.fractale = Fractale(nom)
        self.generation = 0
        self.nom = nom

        ratio = 1024 / 768 * 8.
        self.crt.repere(-ratio / 2, ratio / 2, -2, 6)

        self.dessinefractale(point2D(-2, 0), point2D(2, 0), True, 0, "black")

        self.crt.canvas.focus_set()
        self.dessine()

        self.crt.root.mainloop()

    def dessinefractale(self, ori, ext, sensf, ordre, fill="red"):
        # calcul coefficients de la transformation : [seg1,seg2] --> [ori,ext]

        # sensf=true  => similitude directe
        # sensf=false => similitude indirecte
        anti = 1 if sensf else -1

        seg1 = self.fractale.gen[0]
        seg2 = self.fractale.gen[-1]

        dsx = seg1.x - seg2.x
        dsy = seg1.y - seg2.y
        m = sqr(dsx) + sqr(dsy)
        dx = ori.x - ext.x

        dy = ori.y - ext.y
        C = (dsx * dx + dsy * dy * anti) / m
        S = (dsx * dy - dsy * dx * anti) / m

        A = ori.x - (C * seg1.x - S * seg1.y * anti)
        B = ori.y - (S * seg1.x + C * seg1.y * anti)

        # on a : x' = C*x-S*y*anti+A  et  y' = S*x+C*y*anti+B

        ori = None
        sens_ori = None
        for i in self.fractale.gen:
            p = point2D(C * i.x - S * i.y * anti + A, S * i.x + C * i.y * anti + B)
            if ori is not None:
                ext = p

                if ordre == 0:
                    self.crt.ligne(ori, ext, fill)
                else:
                    self.dessinefractale(ori, ext, not sens_ori ^ sensf, ordre - 1, fill)
            ori = p
            sens_ori = i.sens

    def dessine(self):
        self.crt.bind_key(None)
        self.crt.clear()
        self.crt.root.wm_title("Fractales : {} génération {} [en cours...]".format(self.nom, self.generation))
        start_time = time.time()

        couleur = "black" if self.generation == 0 else "red"
        self.dessinefractale(point2D(-2, 0), point2D(2, 0), True, self.generation, fill=couleur)
        self.crt.bind_key(self.callback)

        self.crt.root.wm_title("Fractales : {} génération {} [{:.3f} secondes]".format(self.nom, self.generation, time.time() - start_time))

    def callback(self, event):
        # print("callback:", event)
        old_generation = self.generation
        if event.char == '+' and self.generation < 5:
            self.generation += 1
        elif event.char == '-' and self.generation > 0:
            self.generation -= 1

        if self.generation != old_generation:
            self.dessine()


def main():
    if len(sys.argv) >= 2:
        Dessine(sys.argv[1])
    else:
        Dessine("Koch")


if __name__ == '__main__':
    main()

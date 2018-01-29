#! /usr/bin/env python3
# rené 2018

""" courbes fractales
https://fr.wikipedia.org/wiki/Flocon_de_Koch
http://www.fractalcurves.com/
"""

import sys
import time
import math
import tkinter as tk
from typing import NamedTuple
import argparse


class point2D(NamedTuple):
    x: float
    y: float


class pointF(NamedTuple):
    x: float
    y: float
    sens: bool = True
    inverse: bool = False


def sqr(x):
    return x * x


def sqrt(x):
    return math.sqrt(x)


class Fractale:

    def __init__(self, nom):

        self.max = 5                # génération maximale acceptable
        self.p1 = point2D(-1, 0)
        self.p2 = point2D(1, 0)

        if nom == "Mandelbrot":
            # «courbe de Mandelbrot» : exemple d'une courbe de Peano
            self.gen = [
                pointF(-1,                     0, False),    # 0
                pointF(-2 / 3,       sqrt(3) / 3, True),     # 1
                pointF(-1 / 3,   2 * sqrt(3) / 3, True),     # 2
                pointF(1 / 3,    2 * sqrt(3) / 3, True),     # 3
                pointF(2 / 3,        sqrt(3) / 3, True),     # 4
                pointF(1 / 3,    4 * sqrt(3) / 9, False),    # 5
                pointF(0,        5 * sqrt(3) / 9, False),    # 6
                pointF(-1 / 3,   4 * sqrt(3) / 9, False),    # 7
                pointF(-1 / 3,   2 * sqrt(3) / 9, True),     # 8
                pointF(1 / 3,    2 * sqrt(3) / 9, True),     # 9
                pointF(0,            sqrt(3) / 9, False),    # 10
                pointF(-1 / 3,                 0, False),    # 11
                pointF(1 / 3,                  0, True),     # 12
                pointF(1,                      0, True),     # 13
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
                pointF(-1, 0, True),                    # 0
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

        elif nom == "Dragon Curve":
            self.gen = [
                pointF(0, 0, True),
                pointF(0, 1, False),
                pointF(1, 1, True),
            ]

            self.max = 15
            self.p1 = point2D(0 ,0)
            self.p2 = point2D(1, 1)

        elif nom == "Polya Sweep":
            self.gen = [
                pointF(0, 0, False),
                pointF(0, 1, False),
                pointF(1, 1, True),
            ]

            self.max = 15
            self.p1 = point2D(0, 1)
            self.p2 = point2D(0, 0)

        elif nom == "V1 Dragon":
            self.gen = [
                pointF(0, 0, True, False),
                pointF(1, 1, True, True),
                pointF(2, 1, True, False),
                pointF(2, 0),
            ]

            self.max = 9
            self.p1 = point2D(-1, 0)
            self.p2 = point2D(1, 0)

        elif nom == "Carbajo":
            self.gen = [
                pointF(0, 0, True, True),
                pointF(1, 1, True),
                pointF(2, 1, True),
                pointF(2, 0),
            ]

            self.max = 9
            self.p1 = point2D(-1, 0)
            self.p2 = point2D(1, 0)


class Crt:
    def __init__(self, width, height):
        self.dimensions = [width, height]
        self.root = tk.Tk()
        self.canvas = tk.Canvas(self.root, width=width, height=height,
                                borderwidth=0, highlightthickness=0)
        self.canvas.grid()

    def coords(self, x_min, x_max, y_min, y_max):
        bounds = [0, 0, self.dimensions[0], self.dimensions[1]]

        self.coords_x = [x_min, x_max]
        self.coords_y = [y_min, y_max]

        self.coords_rect = [x_min,
                            y_max,
                            (bounds[2] - bounds[0]) / (x_max - x_min),
                            (bounds[3] - bounds[1]) / (y_min - y_max)]

    def conv(self, p):
        x = (p.x - self.coords_rect[0]) * self.coords_rect[2]
        y = (p.y - self.coords_rect[1]) * self.coords_rect[3]
        return x, y

    def ligne(self, p1, p2, fill="red", **kwargs):
        x1, y1 = self.conv(p1)
        x2, y2 = self.conv(p2)
        self.canvas.create_line(x1, y1, x2, y2, fill=fill, **kwargs)

    def rond(self, p1):
        x1, y1 = self.conv(p1)

        self.canvas.create_oval(x1 - 2, y1 - 2, x1 + 2, y1 + 2)

    def clear(self):
        self.canvas.delete("all")

    def bind_key(self, callback):
        self.canvas.bind("<Key>", callback)

    def repere(self):
        p1 = point2D(self.coords_x[0], 0)
        p2 = point2D(self.coords_x[1], 0)

        p3 = point2D(0, self.coords_y[0])
        p4 = point2D(0, self.coords_y[1])

        self.ligne(p1, p2, dash=(2, 16), fill="blue")
        self.ligne(p3, p4, dash=(2, 16), fill="blue")


class Dessine:
    def __init__(self, nom, debug=False):
        self.nom = nom
        self.debug = debug

        self.fractale = Fractale(nom)
        self.generation = 0

        # self.crt = Crt(1024, 768)
        # ratio = 1024 / 768 * 8.
        # self.crt.coords(-ratio / 2, ratio / 2, -2, 6)

        self.crt = Crt(800, 800)
        self.crt.coords(-2.4, 2.4, -1.2, 3.6)

        self.dessine()

        self.crt.canvas.focus_set()
        self.crt.root.mainloop()

    def dessine(self):
        self.crt.bind_key(None)
        self.crt.clear()
        self.crt.root.wm_title("Fractales : {} - génération {} [en cours...]".format(
                               self.nom, self.generation))
        start_time = time.time()

        self.couleur = "black" if self.generation == 0 else "red"
        self.dessinefractale(self.fractale.p1, self.fractale.p2, True, self.generation)

        self.crt.canvas.update()

        self.crt.root.wm_title("Fractales : {} - génération {} [{:.3f} secondes]".format(
                               self.nom, self.generation, time.time() - start_time))
        self.crt.bind_key(self.callback)

    def callback(self, event):
        print("callback:", event)
        old_generation = self.generation
        if (event.char == '+' or event.keysym == 'Right'):
            if self.generation < self.fractale.max:
                self.generation += 1
        elif (event.char == '-'  or event.keysym == 'Left'):
            if self.generation > 0:
                self.generation -= 1
        elif event.char == 'r':
            self.crt.repere()
        elif event.char == 'u':
            old_generation = None

        if self.generation != old_generation:
            self.dessine()

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
        inverse_ori = None

        for i in self.fractale.gen:
            p = point2D(C * i.x - S * i.y * anti + A, S * i.x + C * i.y * anti + B)
            if ori is not None:
                ext = p

                if ordre == 0:
                    self.crt.ligne(ori, ext, self.couleur)
                else:
                    if inverse_ori:
                        self.dessinefractale(ext, ori, not sens_ori ^ sensf, ordre - 1)
                    else:
                        self.dessinefractale(ori, ext, not sens_ori ^ sensf, ordre - 1)

                    if ordre == 1 and self.debug:
                        self.crt.ligne(ori, ext, fill="blue", dash=(2,6))

            else:
                if self.debug:
                    # dessine un petit rond sur l'origine de la graine
                    self.crt.rond(p)

            ori = p
            sens_ori = i.sens
            inverse_ori = i.inverse

        if self.debug:
            # dessine un petit rond sur l'extrêmité de la graine
            self.crt.rond(ext)


def main():
    parser = argparse.ArgumentParser(description='Courbes Fractales')
    parser.add_argument("-v", "--verbose", action="store_true")
    parser.add_argument("nom", help="Nom de la fractale", default="Koch")
    args = parser.parse_args()

    Dessine(args.nom, args.verbose)


if __name__ == '__main__':
    main()

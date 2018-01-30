#! /usr/bin/env python3
# rené 2018

""" courbes fractales
https://fr.wikipedia.org/wiki/Flocon_de_Koch
http://www.fractalcurves.com/
"""

import time
import math
import tkinter as tk
import tkinter.messagebox as mbox
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

        # valeurs par défaut
        self.max = 5                # génération maximale acceptable
        self.p1 = point2D(-1, 0)
        self.p2 = point2D(1, 0)
        self.coords = [-2.4, 2.4, -1.2, 3.6]

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

            self.max = 4
            self.p1 = point2D(-1.5, 0)
            self.p2 = point2D(1.5, 0)
            self.coords = [-1.5, 1.5, -sqrt(3) / 2, 3 * sqrt(3) / 2]

        elif nom == "Koch":
            self.gen = [
                pointF(-1,          0, True),    # 0
                pointF(-1/3,        0, True),    # 1
                pointF(0, sqrt(3) / 3, True),    # 2
                pointF(1/3,         0, True),    # 3
                pointF(1,           0, True),    # 4
            ]

            self.max = 7
            self.p1 = point2D(-1.5, 0)
            self.p2 = point2D(1.5, 0)
            self.coords = [-1.5, 1.5, 0, sqrt(3) / 2]

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
            self.p1 = point2D(-1, 0)
            self.p2 = point2D(1, 0)
            self.coords = [-1, 1, 0, a]

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
            self.p1 = point2D(-1, 0)
            self.p2 = point2D(1, 0)
            self.coords = [-1, 1, -1, 1]

        elif nom == "Dragon Curve":
            self.gen = [
                pointF(0, 0, True),
                pointF(0, 1, False),
                pointF(1, 1, True),
            ]
            self.max = 20
            self.p1 = point2D(0, 0)
            self.p2 = point2D(1, 1)
            self.coords = [-2 / 3, 1, -1 / 3, 7 / 6]

        elif nom == "Polya Sweep":
            self.gen = [
                pointF(0, 0, False),
                pointF(0, 1, False),
                pointF(1, 1, True),
            ]
            self.max = 15
            self.p1 = point2D(0, 1)
            self.p2 = point2D(0, 0)
            self.coords = [0, 0.5, 0, 1]

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
            self.coords = [-2, 2, -0.5, 2]

        elif nom == "Carbajo":
            self.gen = [
                pointF(0, 0, True, True),
                pointF(1, 1, True),
                pointF(2, 1, True),
                pointF(2, 0),
            ]
            self.max = 10
            self.p1 = point2D(-1, 0)
            self.p2 = point2D(1, 0)
            self.coords = [-1.5, 2, -1, 2]


class Crt:
    def __init__(self, width, height):
        self.dimensions = [width, height]
        self.root = tk.Tk()
        self.canvas = tk.Canvas(self.root, width=width, height=height,
                                borderwidth=0, highlightthickness=0)
        self.canvas.grid()

    def coords(self, x_min, x_max, y_min, y_max, scale=1, margin=24):
        bounds = [0, 0, self.dimensions[0], self.dimensions[1]]

        self.coords_x = [x_min, x_max]
        self.coords_y = [y_min, y_max]

        x_moy = (x_min + x_max) / 2
        y_moy = (y_min + y_max) / 2

        self.coords_rect = [(x_min - x_moy) * scale + x_moy,
                            (y_max - y_moy) * scale + y_moy,
                            (bounds[2] - bounds[0] - margin * 2) / (x_max - x_min) / scale,
                            (bounds[3] - bounds[1] - margin * 2) / (y_min - y_max) / scale]

        self.coords_rect[0] = self.coords_rect[0] - margin / self.coords_rect[2]
        self.coords_rect[1] = self.coords_rect[1] - margin / self.coords_rect[3]

    def conv(self, p):
        x = int((p.x - self.coords_rect[0]) * self.coords_rect[2])
        y = int((p.y - self.coords_rect[1]) * self.coords_rect[3])
        return x, y

    def ligne(self, p1, p2, fill="red", **kwargs):
        x1, y1 = self.conv(p1)
        x2, y2 = self.conv(p2)
        self.canvas.create_line(x1, y1, x2, y2, fill=fill, **kwargs)

    def ligne2(self, p1, p2, sens=True, inverse=False):
        if inverse:
            p1, p2 = p2, p1
        x1, y1 = self.conv(p1)
        x2, y2 = self.conv(p2)
        signe_sens = -1 if sens else 1
        longueur = sqrt(sqr(x1 - x2) + sqr(y1 - y2))
        ax2 = x2 - 10 * (x2 - x1) / longueur
        ay2 = y2 - 10 * (y2 - y1) / longueur
        ax1 = ax2 - 6 * (y2 - y1) / longueur * signe_sens
        ay1 = ay2 + 6 * (x2 - x1) / longueur * signe_sens
        self.canvas.create_polygon([x1, y1, x2, y2, ax1, ay1, ax2, ay2], outline="black", fill="red", width=1)

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
    def __init__(self, nom, debug=False, generation=0):
        self.nom = nom
        self.debug = debug

        self.generation = generation
        self.fractale = Fractale(nom)

        self.smooth = False

        coords = self.fractale.coords

        ratio_width_height = abs((coords[1] - coords[0]) / (coords[3] - coords[2]))
        h = 800
        w = h * ratio_width_height
        if w > 1280:
            w = 1280
            h = w / ratio_width_height

        self.crt = Crt(w, h)
        self.crt.coords(*self.fractale.coords)
        self.dessine()

        self.crt.canvas.focus_set()
        self.crt.root.mainloop()

    def dessine(self):
        self.crt.bind_key(None)
        self.crt.clear()
        self.crt.root.wm_title("Fractales : {} - génération {} [en cours...]".format(
                               self.nom, self.generation))
        start_time = time.time()

        print("dessine {} gen {}".format(self.nom, self.generation))
        self.couleur = "black" if self.generation == 0 else "red"

        self.points = []
        self.minx, self.maxx, self.miny, self.maxy = 0, 0, 0, 0

        self.dessinefractale(self.fractale.p1, self.fractale.p2, True, self.generation)
        if len(self.points) > 0 and not self.debug:
            # x, y = self.points[0], self.points[1]
            # self.crt.canvas.create_oval(x - 4, y - 4, x + 4, y + 4)
            self.crt.canvas.create_line(self.points, smooth=self.smooth)
            print(self.minx, self.maxx, self.miny, self.maxy, len(self.points) // 2)

        self.crt.canvas.update()

        self.crt.root.wm_title("Fractales : {} - génération {} [{:.3f} secondes]".format(
                               self.nom, self.generation, time.time() - start_time))
        self.crt.bind_key(self.callback)

    def callback(self, event):
        # print("callback:", event)
        old_generation = self.generation
        if event.char == '+' or event.keysym == 'Right':
            if self.generation < self.fractale.max:
                self.generation += 1
        elif event.char == '-' or event.keysym == 'Left':
            if self.generation > 0:
                self.generation -= 1
        elif event.char == 'r':
            self.crt.repere()
        elif event.char == 'u':
            old_generation = None
        elif event.char == '0':
            old_generation = None
            self.generation = 0
        elif event.char == 'v':
            self.debug = not self.debug
            old_generation = None
        elif event.char == 's':
            self.smooth = not self.smooth
            old_generation = None
        elif event.keysym == 'Next':
            pass
        elif event.keysym == 'Prior':
            pass
        elif event.char == 'x':
            self.crt.root.quit()
        elif event.char == 'h':
            mbox.showinfo("Fractales", """
h \t: cette aide
x \t: sortir
+ / → \t: avancer d'une génération
- / ← \t: reculer d'une génération
0 \t: génération 0 (graine)
v \t: voir les points de construction
r \t: tracer le repère
u \t: rafraîchir l'affichage
s \t: smooth
""")

        if self.generation != old_generation:
            self.dessine()

    def dessinefractale(self, ori, ext, sensf, ordre, inverse=False, fill="red"):
        # calcul coefficients de la transformation : [seg1,seg2] --> [ori,ext]

        # print("dessinefractale", ori, ext, ordre, sensf, inverse)
        if inverse:
            ori, ext = ext, ori

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
        transf = lambda p: point2D(C * p.x - S * p.y * anti + A, S * p.x + C * p.y * anti + B)

        if not self.debug:
            pts = []

            if inverse:
                ori = None
                for i in reversed(self.fractale.gen):
                    p = transf(i)
                    if ori is not None:
                        ext = p
                        if ordre == 0:
                            # self.crt.ligne(ori, ext, self.couleur)
                            if len(self.points) == 0:
                                pts.append(ori)
                            pts.append(ext)
                        else:
                            self.dessinefractale(ori, ext, not i.sens ^ sensf, ordre - 1, not i.inverse)
                    ori = p
            else:
                ori = None
                sens_ori = None
                inverse_ori = None
                for i in self.fractale.gen:
                    p = transf(i)
                    if ori is not None:
                        ext = p
                        if ordre == 0:
                            # self.crt.ligne(ori, ext, self.couleur)
                            if len(self.points) == 0:
                                pts.append(ori)
                            pts.append(ext)
                        else:
                            self.dessinefractale(ori, ext, not sens_ori ^ sensf, ordre - 1, inverse_ori)
                    ori = p
                    sens_ori = i.sens
                    inverse_ori = i.inverse

            for i in pts:
                if i.x < self.minx: self.minx = i.x
                if i.y < self.miny: self.miny = i.y
                if i.x > self.maxx: self.maxx = i.x
                if i.y > self.maxy: self.maxy = i.y
                self.points.extend(self.crt.conv(i))

        else:
            ori = None
            sens_ori = None
            inverse_ori = None

            for i in self.fractale.gen:
                p = transf(i)
                if ori is not None:
                    ext = p

                    if ordre == 0:
                        if self.generation <= 1:
                            # génération 0 ou 1: on trace des flèches indiquant comment va "germer"
                            # la graine sur chacun des segments
                            self.crt.ligne2(ori, ext, sens=sens_ori, inverse=inverse_ori)
                        else:
                            self.crt.ligne(ori, ext, self.couleur)
                    else:
                        if inverse_ori:
                            self.dessinefractale(ext, ori, not sens_ori ^ sensf, ordre - 1)
                        else:
                            self.dessinefractale(ori, ext, not sens_ori ^ sensf, ordre - 1)

                        if ordre == 1:
                            self.crt.ligne(ori, ext, fill="blue", dash=(2, 6))

                else:
                    # dessine un petit rond sur l'origine de la graine
                    self.crt.rond(p)

                ori = p
                sens_ori = i.sens
                inverse_ori = i.inverse

            # dessine un petit rond sur l'extrêmité de la graine
            self.crt.rond(ext)


def main():
    parser = argparse.ArgumentParser(description='Courbes Fractales')
    parser.add_argument("-v", "--verbose", action="store_true")
    parser.add_argument("-l", "--level", type=int, default=0)
    parser.add_argument("nom", help="Nom de la fractale", nargs='?', default="Koch")
    args = parser.parse_args()

    Dessine(args.nom, args.verbose, generation=args.level)


if __name__ == '__main__':
    main()

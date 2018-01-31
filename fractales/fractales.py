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
import xml.etree.ElementTree as ET


WINDOW_HEIGHT = 960
WINDOW_WIDTH = 1280


# contexte global et unique de Tk
root_tk = None

class Point2D(NamedTuple):
    """ point dans le plan """
    x: float
    y: float
    def str(self):
        """ retourne les coordonnées pour affichage """
        return "{:.5f} x {:.5f}".format(self.x, self.y)


class PointF(NamedTuple):
    """ noeud d'une courbe fractale """
    x: float
    y: float
    sens: bool = True
    inverse: bool = False


class Fractale:

    def __init__(self, nom):

        # valeurs par défaut
        self.max = 5                # génération maximale acceptable
        self.p1 = Point2D(-1, 0)
        self.p2 = Point2D(1, 0)
        self.limites = [-2.4, 2.4, -1.2, 3.6]

        if nom is None:
            return

        if type(nom) is not str:
             self.from_xml(nom)
             return

        sqrt = math.sqrt

        if nom == "Mandelbrot":
            # «courbe de Mandelbrot» : exemple d'une courbe de Peano
            self.gen = [
                PointF(-1,                     0, False),    # 0
                PointF(-2 / 3,       sqrt(3) / 3, True),     # 1
                PointF(-1 / 3,   2 * sqrt(3) / 3, True),     # 2
                PointF(1 / 3,    2 * sqrt(3) / 3, True),     # 3
                PointF(2 / 3,        sqrt(3) / 3, True),     # 4
                PointF(1 / 3,    4 * sqrt(3) / 9, False),    # 5
                PointF(0,        5 * sqrt(3) / 9, False),    # 6
                PointF(-1 / 3,   4 * sqrt(3) / 9, False),    # 7
                PointF(-1 / 3,   2 * sqrt(3) / 9, True),     # 8
                PointF(1 / 3,    2 * sqrt(3) / 9, True),     # 9
                PointF(0,            sqrt(3) / 9, False),    # 10
                PointF(-1 / 3,                 0, False),    # 11
                PointF(1 / 3,                  0, True),     # 12
                PointF(1,                      0, True),     # 13
            ]

            self.max = 4
            self.p1 = Point2D(-1.5, 0)
            self.p2 = Point2D(1.5, 0)
            self.limites = [-1.5, 1.5, -sqrt(3) / 2, 3 * sqrt(3) / 2]

        elif nom == "Koch":
            self.gen = [
                PointF(-1,          0, True),    # 0
                PointF(-1/3,        0, True),    # 1
                PointF(0, sqrt(3) / 3, True),    # 2
                PointF(1/3,         0, True),    # 3
                PointF(1,           0, True),    # 4
            ]

            self.max = 7
            self.p1 = Point2D(-1.5, 0)
            self.p2 = Point2D(1.5, 0)
            self.limites = [-1.5, 1.5, 0, sqrt(3) / 2]

    def from_xml(self, child):

        locals = {}

        def evalm(x):
            return eval(x, { 'sqrt': math.sqrt,
                             'sqr': lambda x: math.pow(x, 2),
                             'sin': math.sin,
                             'cos': math.cos,
                             'radians': math.radians,
                             'pi': math.pi }, locals)

        def tobool(s):
            return True if s.lower() == "true" else False

        self.nom = child.findtext('nom')

        for var in child.findall(u'variables/variable'):
            v = var.attrib['nom']
            x = var.attrib['valeur']
            locals[v] = evalm(x)

        self.gen = []
        for p in child.find(u'générateur'):
            x = evalm(p.attrib['x'])
            y = evalm(p.attrib['y'])
            sens = tobool(p.attrib.get('sens', 'True'))
            inverse = tobool(p.attrib.get('inverse', 'False'))
            p = PointF(x, y, sens, inverse)
            self.gen.append(p)

        tag = child.find(u'génération')
        if tag is not None:
            self.max = int(tag.attrib.get('max'))

        tag = child.find(u'tracé/point1')
        if tag is not None:
            self.p1 = Point2D(evalm(tag.attrib['x']), evalm(tag.attrib['y']))

        tag = child.find(u'tracé/point2')
        if tag is not None:
            self.p2 = Point2D(evalm(tag.attrib['x']), evalm(tag.attrib['y']))

        tag = child.find(u'tracé/limites')
        if tag is not None:
            self.limites = [evalm(tag.attrib['min_x']),
                           evalm(tag.attrib['max_x']),
                           evalm(tag.attrib['min_y']),
                           evalm(tag.attrib['max_y']) ]

class Fractales:
    def __init__(self, fichier="fractales.xml"):
        tree = ET.parse(fichier)
        root = tree.getroot()

        if root.tag != "fractales":
            return

        self.definitions = [i.find('nom').text for i in root.findall("fractale[nom]")]
        self.tree = tree

    def liste(self):
        for i in self.definitions:
            f = self.fractale(i)
            print("{:20s} {:2d} {}".format(i, len(f.gen), ""))

    def fractale(self, nom):
        if self.tree is None:
            return
        child = self.tree.getroot().find("fractale[nom='{}']".format(nom))
        return Fractale(child)

    def cherche(self, nom, incr):
        i = self.definitions.index(nom) + incr
        if i >= 0 and i < len(self.definitions):
            nom = self.definitions[i]
        return nom

class Crt:
    def __init__(self, width, height):
        global root_tk
        self.dimensions = [width, height]
        if root_tk is None: root_tk = tk.Tk()
        self.root = root_tk #tk.Tk()
        self.canvas = tk.Canvas(self.root, width=width, height=height,
                                borderwidth=0, highlightthickness=0)
        self.canvas.grid()
        self.coords = None

    def set_coords(self, x_min, x_max, y_min, y_max, scale=1, margin=24):
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
        longueur = math.sqrt(math.pow(x1 - x2, 2) + math.pow(y1 - y2, 2))
        ax2 = x2 - 10 * (x2 - x1) / longueur
        ay2 = y2 - 10 * (y2 - y1) / longueur
        ax1 = ax2 - 6 * (y2 - y1) / longueur * signe_sens
        ay1 = ay2 + 6 * (x2 - x1) / longueur * signe_sens
        self.canvas.create_polygon([x1, y1, x2, y2, ax1, ay1, ax2, ay2],
                                   outline="black", fill="red", width=1)

    def rond(self, p1):
        x1, y1 = self.conv(p1)

        self.canvas.create_oval(x1 - 2, y1 - 2, x1 + 2, y1 + 2)

    def conv_inverse(self, x, y):
        rx = x  / self.coords_rect[2] + self.coords_rect[0]
        ry = y  / self.coords_rect[3] + self.coords_rect[1]
        return Point2D(rx, ry)

    def clear(self):
        self.canvas.delete("all")
        self.canvas.unbind("<Motion>")
        self.canvas.unbind("<Key>")

    def bind_key(self, callback):
        if callback is not None:
            self.canvas.bind("<Key>", callback)

    def repere(self):
        p1 = Point2D(self.coords_x[0], 0)
        p2 = Point2D(self.coords_x[1], 0)

        p3 = Point2D(0, self.coords_y[0])
        p4 = Point2D(0, self.coords_y[1])

        self.ligne(p1, p2, dash=(2, 8), fill="blue")
        self.ligne(p3, p4, dash=(2, 8), fill="blue")

        for i in range(int(self.coords_x[0]), int(self.coords_x[1]) + 1):
            x, y = self.conv(Point2D(i, 0))
            self.canvas.create_line(x, y - 4, x, y + 4, fill="blue")

        for i in range(int(self.coords_y[0]), int(self.coords_y[1]) + 1):
            x, y = self.conv(Point2D(0, i))
            self.canvas.create_line(x - 4, y, x + 4, y, fill="blue")

        def affiche_xy(event):
            p = self.conv_inverse(event.x, event.y)
            if self.coords is not None:
                self.canvas.delete(self.coords)
            self.coords = self.canvas.create_text(4, 4, text=p.str(), anchor=tk.NW)
        self.canvas.bind("<Motion>", affiche_xy)

        affiche_xy(Point2D(self.root.winfo_pointerx() - self.root.winfo_rootx(),
                           self.root.winfo_pointery() - self.root.winfo_rooty()))

class Dessine:
    def __init__(self, fractale, debug=False, generation=0):
        self.debug = debug
        self.continuer = 0

        self.generation = generation
        self.fractale = fractale

        self.smooth = False

        limites = self.fractale.limites


        ratio_width_height = abs((limites[1] - limites[0]) / (limites[3] - limites[2]))
        h = WINDOW_HEIGHT
        w = h * ratio_width_height
        if w > WINDOW_WIDTH:
            w = WINDOW_WIDTH
            h = w / ratio_width_height

        self.crt = Crt(w, h)
        self.crt.set_coords(*self.fractale.limites)
        self.dessine()

        self.crt.canvas.focus_set()
        self.crt.root.mainloop()
        self.crt.canvas.destroy()

    def dessine(self):
        self.crt.bind_key(None)
        self.crt.clear()
        self.crt.root.wm_title("Fractale : {} - génération {} [en cours...]".format(
                               self.fractale.nom, self.generation))
        start_time = time.time()

        print("dessine {} gen {}".format(self.fractale.nom, self.generation))
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

        duree = time.time() - start_time

        self.crt.root.wm_title("Fractale : {} - génération {} [{:.3f} secondes]".format(
                               self.fractale.nom, self.generation, duree))

        if duree > 4:
            self.fractale.max = self.generation

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
            self.continuer = 1
            self.crt.root.quit()
        elif event.keysym == 'Prior':
            self.continuer = -1
            self.crt.root.quit()
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
        elif event.char == 'p':
            self.crt.canvas.postscript(colormode='color', file='{}_{}{}.ps'.format(self.fractale.nom, self.generation, '_d' if self.debug else ''))

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
        m = dsx * dsx + dsy * dsy
        dx = ori.x - ext.x

        dy = ori.y - ext.y
        C = (dsx * dx + dsy * dy * anti) / m
        S = (dsx * dy - dsy * dx * anti) / m

        A = ori.x - (C * seg1.x - S * seg1.y * anti)
        B = ori.y - (S * seg1.x + C * seg1.y * anti)

        # on a : x' = C*x-S*y*anti+A  et  y' = S*x+C*y*anti+B
        transf = lambda p: Point2D(C * p.x - S * p.y * anti + A, S * p.x + C * p.y * anti + B)

        if not self.debug:
            pts = []
            premier = len(self.points) == 0

            if inverse:
                ori = None
                for i in reversed(self.fractale.gen):
                    p = transf(i)
                    if ori is not None:
                        ext = p
                        if ordre == 0:
                            # self.crt.ligne(ori, ext, self.couleur)
                            if premier:
                                premier = False
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
                            if premier:
                                premier = False
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
    parser.add_argument("-L", "--list", help="liste les fractales connues", action="store_true")
    parser.add_argument("-f", "--file", help="fichier de définition des fractales", default="fractales.xml")
    parser.add_argument("nom", help="nom de la fractale", nargs='?', default="Koch")
    args = parser.parse_args()

    courbes = Fractales(fichier=args.file)

    if args.list:
        courbes.liste()
        return

    nom = args.nom
    while True:
        fractale = courbes.fractale(nom)
        print(fractale.nom)
        o = Dessine(fractale, args.verbose, generation=args.level)
        if o.continuer == 0:
            break
        nom = courbes.cherche(nom, o.continuer)



if __name__ == '__main__':
    main()

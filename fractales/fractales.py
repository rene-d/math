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
import tkinter.messagebox as mbox
from typing import NamedTuple
import argparse
import xml.etree.ElementTree as ET


if sys.version_info < (3,6):
    print("Désolé, il faut au moins Python 3.6")
    sys.exit(2)

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

    def __init__(self, nom=None):

        # valeurs par défaut
        if  isinstance(nom, ET.Element):
            self.from_xml(nom)
            return

        self.nom = "Koch"
        self.gen = [
            PointF(-1, 0),               # 0
            PointF(-1 / 3, 0),           # 1
            PointF(0, math.sqrt(3) / 3), # 2
            PointF(1 / 3, 0),            # 3
            PointF(1, 0),                # 4
        ]
        self.max = 7
        self.init_trace()

    def init_trace(self):
        # par défaut: premier et dernier point du générateur
        self.segments = [[Point2D(self.gen[0].x, self.gen[0].y),
                          Point2D(self.gen[-1].x, self.gen[-1].y)]]

        # par défaut: les min et max des x,y du générateur
        xmin = xmax = ymin = ymax = None
        for i in self.gen:
            if xmin is None or xmin > i.x: xmin = i.x
            if xmax is None or xmax < i.x: xmax = i.x
            if ymin is None or ymin > i.y: ymin = i.y
            if ymax is None or ymax < i.y: ymax = i.y
        self.limites = [xmin, xmax, ymin, ymax]

    def from_xml(self, child):
        variables = {}

        def evalm(x):
            return eval(x, { 'sqrt': math.sqrt,
                             'sqr': lambda x: math.pow(x, 2),
                             'sin': math.sin,
                             'cos': math.cos,
                             'radians': math.radians,
                             'pi': math.pi }, variables)

        def tobool(s):
            return True if s.lower() == "true" else False

        self.nom = child.findtext('nom')

        for var in child.findall(u'variables/variable'):
            v = var.attrib['nom']
            x = var.attrib['valeur']
            variables[v] = evalm(x)

        self.gen = []
        for p in child.find('generateur'):
            x = evalm(p.attrib['x'])
            y = evalm(p.attrib['y'])
            sens = tobool(p.attrib.get('sens', 'True'))
            inverse = tobool(p.attrib.get('inverse', 'False'))
            p = PointF(x, y, sens, inverse)
            self.gen.append(p)

        tag = child.find('generation')
        if tag is not None:
            self.max = int(tag.attrib.get('max'))

        tag = child.find('trace/point1')
        if tag is not None:
            p1 = Point2D(evalm(tag.attrib['x']), evalm(tag.attrib['y']))

            tag = child.find(u'trace/point2')
            if tag is not None:
                p2 = Point2D(evalm(tag.attrib['x']), evalm(tag.attrib['y']))

                self.segments = [[p1, p2]]

        segments = []
        for segment in child.findall(u'trace/segments/segment'):

            tag = segment.find("point1")
            p1 = Point2D(evalm(tag.attrib['x']), evalm(tag.attrib['y']))

            tag = segment.find("point2")
            p2 = Point2D(evalm(tag.attrib['x']), evalm(tag.attrib['y']))

            segments.append([p1, p2])

        if len(segments) > 0:
            self.segments = segments

        tag = child.find(u'trace/limites')
        if tag is not None:
            self.limites = [evalm(tag.attrib['min_x']),
                            evalm(tag.attrib['max_x']),
                            evalm(tag.attrib['min_y']),
                            evalm(tag.attrib['max_y'])]

class Fractales:
    def __init__(self, fichier="fractales.xml"):
        try:
            tree = ET.parse(fichier)
            root = tree.getroot()

            if root.tag != "fractales":
                return

            self.definitions = [i.find('nom').text for i in root.findall("fractale[nom]")]
            self.tree = tree

        except FileNotFoundError:
            self.tree = None
            self.definitions = None

    def liste(self):
        if self.definitions is None:
            return
        for i in self.definitions:
            f = self.fractale(i)
            print("{:20s} {:2d} {}".format(i, len(f.gen), ""))

    def fractale(self, nom):
        if self.tree is None:
            return Fractale()
        child = self.tree.getroot().find("fractale[nom='{}']".format(nom))
        return Fractale(child)

    def cherche(self, nom, incr):
        if self.definitions is None:
            return
        i = self.definitions.index(nom) + incr
        if i >= 0 and i < len(self.definitions):
            nom = self.definitions[i]
        return nom

class Crt:
    def __init__(self, ratio_width_height=1):
        global root_tk

        if root_tk is None: root_tk = tk.Tk()
        self.root = root_tk #tk.Tk()

        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()

        width = screen_width * 0.9
        height = screen_height * 0.9

        if height * ratio_width_height > width:
            height = width / ratio_width_height
        else:
            width = height * ratio_width_height

        self.dimensions = [width, height]

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

    def titre(self, texte):
        self.root.wm_title(texte)

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
    def __init__(self, fractale, details=False, generation=0):
        self.details = details
        self.continuer = 0

        self.generation = generation
        self.fractale = fractale

        self.smooth = False
        self.auto_sauve = False

        limites = self.fractale.limites
        ratio_width_height = abs((limites[1] - limites[0]) / (limites[3] - limites[2]))

        self.crt = crt = Crt(ratio_width_height)
        crt.set_coords(*self.fractale.limites)
        self.dessine()

        crt.canvas.focus_set()
        crt.root.mainloop()
        crt.canvas.destroy()

    def dessine(self):
        crt = self.crt
        crt.bind_key(None)
        crt.clear()
        crt.titre("Fractale : {} - génération {} [en cours...]".format(
                          self.fractale.nom, self.generation))
        start_time = time.time()

        print("dessine {} gen {}".format(self.fractale.nom, self.generation))
        self.couleur = "black" if self.generation == 0 else "red"
        self.minx, self.maxx, self.miny, self.maxy = 0, 0, 0, 0

        for segment in self.fractale.segments:
            self.points = []

            self.dessinefractale(segment[0], segment[1], True, self.generation)

            if len(self.points) > 0 and not self.details:
                # print(self.points)
                # x, y = self.points[0], self.points[1]
                # self.crt.canvas.create_oval(x - 4, y - 4, x + 4, y + 4)
                crt.canvas.create_line(self.points, smooth=self.smooth)

        if len(self.points) > 0 and not self.details:
            print(self.minx, self.maxx, self.miny, self.maxy, len(self.points) // 2)

        self.crt.canvas.update()

        duree = time.time() - start_time

        crt.titre("Fractale : {} [{:.3f} secondes]".format(self.titre(), duree))

        if self.auto_sauve:
            self.sauve()

        if duree > 4:
            self.fractale.max = self.generation

        crt.bind_key(self.callback)

    def titre(self):
        return "{} {}- génération {}".format(self.fractale.nom,
                                               "(lissé) " if self.smooth else "",
                                               self.generation)

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
            self.details = not self.details
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
        elif event.char == 'x' or event.char == 'q':
            self.crt.root.quit()
        elif event.char == 'h':
            mbox.showinfo("Fractales", """
h \t: cette aide
x, q \t: sortir
+ / → \t: avancer d'une génération
- / ← \t: reculer d'une génération
0 \t: génération 0 (graine)
v \t: voir les points de construction
r \t: tracer le repère
u \t: rafraîchir l'affichage
s \t: smooth
p \t: sauver le dessin en PostScript
""")
        elif event.char == 'p':
            self.sauve()
        elif event.char == 'P':
            self.auto_sauve = not self.auto_sauve
            self.sauve()

        if self.generation != old_generation:
            self.dessine()

    def sauve(self):
        fichier = '{}_{}'.format(self.fractale.nom, self.generation)
        if self.smooth: fichier += '_lisse'
        if self.details: fichier += '_d'
        fichier += ".ps"

        # TODO déplacer cette portion dans Crt
        self.crt.canvas.create_text(
                self.crt.canvas.winfo_width() / 2,
                self.crt.canvas.winfo_height() - 4,
                text=self.titre(),
                fill="blue",
                justify=tk.CENTER,
                anchor=tk.S,
                font=('Helvetica', '14', 'italic') )

        self.crt.canvas.postscript(colormode='color', file=fichier)
        print("Canevas sauvegardé dans", fichier)

    def dessinefractale(self, ori, ext, sensf, ordre, inverse=False, fill="red"):

        # print("dessinefractale", ori, ext, ordre, sensf, inverse)
        if inverse:
            ori, ext = ext, ori

        # calcul coefficients de la transformation : [seg1,seg2] --> [ori,ext]

        # sensf=true  => similitude directe
        # sensf=false => similitude indirecte
        anti = 1 if sensf else -1

        seg1 = self.fractale.gen[0]     # premier point
        seg2 = self.fractale.gen[-1]    # dernier point

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

        if not self.details:
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
        o = Dessine(fractale, details=args.verbose, generation=args.level)
        if o.continuer == 0:
            break
        nom = courbes.cherche(nom, o.continuer)


if __name__ == '__main__':
    main()

#! /usr/bin/env python3
# rené 2018

""" courbes fractales

https://fr.wikipedia.org/wiki/Flocon_de_Koch

"""

import sys
import tkinter as tk
from typing import NamedTuple
import math


class point2D(NamedTuple):
    x: float
    y: float


class pointF(NamedTuple):
    x: float
    y: float
    sens: bool

class rect2D(NamedTuple):
    x1: float
    y1: float
    x2: float
    y2: float


root = None
repere = None
courant = None
canvas = None
couleur = "red"


def sqr(x):
    return x * x


def sqrt(x):
    return math.sqrt(x)


def initFract(nom):
    global gen

    if nom == "Mandelbrot":
        # «courbe de Mandelbrot» : exemple d'une courbe de Peano
        gen = [
            pointF(-1,                0, False),    #0
            pointF(-2/3.,     sqrt(3)/3, True),     #1
            pointF(-1/3.,   2*sqrt(3)/3, True),     #2
            pointF( 1/3.,   2*sqrt(3)/3, True),     #3
            pointF( 2/3.,     sqrt(3)/3, True),     #4
            pointF( 1/3.,   4*sqrt(3)/9, False),    #5
            pointF(    0,   5*sqrt(3)/9, False),    #6
            pointF(-1/3.,   4*sqrt(3)/9, False),    #7
            pointF(-1/3.,   2*sqrt(3)/9, True),     #8
            pointF( 1/3.,   2*sqrt(3)/9, True),     #9
            pointF(    0,     sqrt(3)/9, False),    #10
            pointF(-1/3.,             0, False),    #11
            pointF( 1/3.,             0, True),     #12
            pointF(    1,             0, True),     #13
        ]

    elif nom == "Koch":
        gen = [
            pointF(-1,          0, True),    #0
            pointF(-1/3.,       0, True),    #1
            pointF(0,   sqrt(3)/3, True),    #2
            pointF(1/3.,        0, True),    #3
            pointF(1,           0, True),    #4
        ]

    elif nom == "Cesaro":
        alpha = math.radians(85)        # angle de la pointe, 60° pour von Koch
        a = 1 / (1 + math.cos(alpha))   # longueur de chaque segment _/\_
        gen = [
            pointF(    -1,                   0, True),    #0
            pointF(-1 + a,                   0, True),    #1
            pointF(     0, a * math.sin(alpha), True),    #2
            pointF( 1 - a,                   0, True),    #3
            pointF(     1,                   0, True),    #4
        ]        

    elif nom == "Peano":
        gen = [
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

premier = True


def conv(p):
    x,y = (p.x - repere.x1) * repere.x2, (p.y - repere.y1) * repere.y2
    return x,y


def initgraphique():
    global canvas, repere, courant, root
    root = tk.Tk()
    canvas = tk.Canvas(root, width=1024, height=768, borderwidth=0, highlightthickness=0)
    canvas.grid()
    

def fenetre(x1, x2, y1, y2):
    global canvas, repere, courant, root

    bounds = [0,0,1024,768]
    repere = rect2D(
        x1, 
        y2,
        (bounds[2] - bounds[0]) / (x2 - x1),
        (bounds[3] - bounds[1]) / (y1 - y2) 
    )

def deplace(p):
    global canvas, repere, courant
    courant = p

def trace(p, fill="red"):
    global canvas, repere, courant
    x1, y1 = conv(courant)
    x2, y2 = conv(p)
    #canvas.create_oval(x1-2,y1-2,x1+2,y1+2)
    canvas.create_line(x1, y1, x2, y2, fill=fill)
    courant = p

def trait(x1, y1, x2,y2):
    xx1, yy1 = conv(point2D(x1, y1))
    xx2, yy2 = conv(point2D(x2, y2))
    canvas.create_line(xx1, yy1, xx2, yy2, fill="black", dash=(2, 16))

def zz():
    root = tk.Tk()
    canvas = tk.Canvas(root, width=1024, height=768, borderwidth=0, highlightthickness=0)
    canvas.grid()
    canvas.create_oval(0,0,50,30)
    canvas.create_line(0,0,300,300, fill="red")
    canvas.create_line(0, 100, 200, 0, fill="red", dash=(4, 4))
    canvas.create_rectangle(50, 25, 150, 75, fill="blue")
    print(canvas.canvasx(400))
    print(canvas.canvasy(400))

    root.wm_title("Circles and Arcs")
    root.mainloop()


def dessinefractale(ori, ext, sensf, ordre, fill="red"):
    global sens, gen, premier

    # calcul coefficients de la transformation : [seg1,seg2] --> [ori,ext] 

    # sensf=true  => similitude directe
    # sensf=false => similitude indirecte
    anti = 1 if sensf else -1

    seg1 = gen[0]
    seg2 = gen[len(gen) - 1]

    dsx = seg1.x - seg2.x
    dsy =seg1.y-seg2.y
    m = sqr(dsx)+sqr(dsy)
    dx =ori.x-ext.x

    dy=ori.y-ext.y
    C=(dsx*dx+dsy*dy*anti)/m
    S=(dsx*dy-dsy*dx*anti)/m

    A=ori.x-(C*seg1.x-S*seg1.y*anti)
    B=ori.y-(S*seg1.x+C*seg1.y*anti)

    # { on a : x' = C*x-S*y*anti+A  et  y' = S*x+C*y*anti+B }

    if ordre <= 0:
        for i in gen:
            p = point2D(C*i.x-S*i.y*anti+A, S*i.x+C* i.y*anti+B)   
            if premier: 
                deplace(p)
                premier = False
            else:
                trace(p, fill)
    else:
        ori = None
        sens_ori = None
        for i in gen:
            p = point2D(C*i.x-S*i.y*anti+A, S*i.x+C*i.y*anti+B)    
            if ori is not None:
                ext = p
                dessinefractale(ori, ext, not sens_ori ^ sensf, ordre - 1, fill)
            ori = p
            sens_ori = i.sens


nn = 0

def callback(event):
    global canvas, repere, courant, root, nn, premier
    #print("callback:", event)
    if event.char == '+' and nn < 5:
        nn += 1
        canvas.delete("all")
        premier = True
        dessinefractale(point2D(-2, 0), point2D(2, 0), True, nn)
    elif event.char == '-' and nn > 0:
        nn -= 1
        canvas.delete("all")
        premier = True
        dessinefractale(point2D(-2, 0), point2D(2, 0), True, nn)


def dessine(nom):    
    global canvas, repere, courant
    initgraphique()

    initFract(nom)

    ratio = 1024 / 768 * 8.
    fenetre(-ratio/2, ratio/2, -2, 6)

    dessinefractale(point2D(-2,0), point2D(2,0), True, 0, "black")

    canvas.bind("<Key>", callback)
    canvas.focus_set()

    root.mainloop()


def main():
    if len(sys.argv) >= 2:
        dessine(sys.argv[1])
    else:
        dessine("Koch")

if __name__ == '__main__':
    main()

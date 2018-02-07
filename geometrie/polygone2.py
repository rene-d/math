#! /usr/bin/env python3

import sys
import math
import tkinter as tk
from tkinter import ttk
from raise_app import *


n = 10 if len(sys.argv) < 2 else int(sys.argv[1])
height = 500

root = tk.Tk()

bar = ttk.Frame(root)
bar.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.S))

ttk.Button(bar, text="⟵", command=lambda: callback('Left')).pack(side="left")
ttk.Button(bar, text="⟶", command=lambda: callback('Right')).pack(side="left")
ttk.Label(bar, text="étoile").pack(side="left")

ttk.Button(bar, text="︎︎↑", command=lambda: callback('Up')).pack(side="right")
ttk.Button(bar, text="↓", command=lambda: callback('Down')).pack(side="right")
ttk.Label(bar, text="côtés").pack(side="right")

canvas = tk.Canvas(root, width=height, height=height, borderwidth=0, highlightthickness=0)
canvas.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N))

R = height / 2 * 0.9
m = height / 2
sommets = []
g = 2
n = 5


def calcule():
    """ calcule les sommets du polygone à n côtés """
    global sommets
    sommets = [(R * math.cos(2 * math.pi / n * i), R * math.sin(2 * math.pi / n * i))
               for i in range(n)]


def dessine():
    """ dessine le polygone ou l'étoile à n côtés """
    canvas.delete("all")
    if g == 1:
        root.wm_title("Polygone à %d côtés" % n)
    else:
        root.wm_title("Etoile à %d côtés - %d" % (n, g))

    for i in range(n):
        for j in range(-1, 2, 2):
                a = sommets[i]
                b = sommets[(i + j * g) % n]

                canvas.create_line(a[0] + m, a[1] + m, b[0] + m, b[1] + m)

    canvas.create_oval(m - R, m - R, m + R, m + R, outline="red")


def callback(event):
    """ traitement des boutons et touches """
    global g, n

    # print(event)

    if isinstance(event, str):
        a = tk.Event()
        a.keysym = event
        a.char = ''
        event = a

    if event.keysym == 'Right':
        if g < (n - 1) // 2:
            g += 1
            dessine()
    elif event.keysym == 'Left':
        if g > 1:
            g -= 1
            dessine()
    elif event.keysym == 'Up' or event.char == '+':
        if n < 40:
            n += 1
            calcule()
            dessine()
    elif event.keysym == 'Down' or event.char == '-':
        if n > 3:
            n -= 1
            if g > (n - 1) // 2:
                g -= 1
            calcule()
            dessine()
    elif event.char == 'q':
        root.quit()


calcule()
dessine()

root.bind('<Key>', callback)
root.focus_set()
raise_app()
root.mainloop()

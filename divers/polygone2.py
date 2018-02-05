#! /usr/bin/env python3

import sys
import os
import math
import tkinter as tk
from raise_app import *


n = 10 if len(sys.argv) < 2 else int(sys.argv[1])

height = 500

root = tk.Tk()

contour = tk.IntVar()
menubar = tk.Menu(root)
menu = tk.Menu(menubar)
menu.add_checkbutton(label="Contour", variable=contour, command=lambda: print(contour.get()))
menu.add_separator()
menu.add_command(label='Quitter', command=root.quit)
menubar.add_cascade(label="Polygones", menu=menu)
root.config(menu=menubar)

canvas = tk.Canvas(root, width=height, height=height, borderwidth=0, highlightthickness=0)
canvas.grid()

R = height / 2 * 0.9
m = height / 2
sommets = []
opt = 2
g = 2
n = 5

def calc():
    global sommets, n, R
    sommets = [(R * math.cos(2 * math.pi / n * i), R * math.sin(2 * math.pi / n * i))
            for i in range(n)]


def dessine():
    global opt, n, m, R, sommets, g, canvas, root
    canvas.delete("all")
    if g == 1:
        root.wm_title("Polygone à %d côtés" % n)
    else:
        root.wm_title("Etoile à %d côtés - %d" % (n, g))
    if opt == 1:
        for i in range(n):
            for j in range(n):
                if (i - j + n) % n in range(2, int((n - 1) / 2 + 1)):
                    a = sommets[i]
                    b = sommets[j]

                    canvas.create_line(a[0] + m, a[1] + m, b[0] + m, b[1] + m)

        canvas.create_oval(m - R, m - R, m + R, m + R, outline="red")

    elif opt == 2:
        for i in range(n):
            for j in range(-1, 2, 2):
                    a = sommets[i]
                    b = sommets[(i + j * g) % n]

                    canvas.create_line(a[0] + m, a[1] + m, b[0] + m, b[1] + m)

        canvas.create_oval(m - R, m - R, m + R, m + R, outline="red")

calc()
dessine()

def callback(event):
    global g, root, n
    print(event)
    if event.keysym == 'Right':
        if g < (n - 1) // 2:
            g += 1
            dessine()
    elif event.keysym == 'Left':
        if g > 1:
            g -= 1
            dessine()
    elif event.keysym == 'Up':
        if n < 30:
            n += 1
            calc()
            dessine()
    elif event.keysym == 'Down':
        if n > 3:
            n -= 1
            if g > (n - 1) // 2:
                g -= 1
            calc()
            dessine()
    elif event.char == 'q':
        root.quit()


canvas.bind('<Key>', callback)

raise_app()
canvas.focus_set()
root.mainloop()

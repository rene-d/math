#!/usr/bin/env python3

"""
https://en.wikipedia.org/wiki/Hyperbola#As_locus_of_points
"""

import argparse
import math
import subprocess
import typing as t
from functools import partial
from io import BytesIO
from pathlib import Path
from tkinter import BOTH, Canvas, Event, Frame, Tk
import numpy as np
from PIL import Image
import tabulate


def circle_intersect(A: complex, rA: float, B: complex, rB: float) -> t.Tuple[complex, complex]:
    """
    cf. https://math.stackexchange.com/a/1367732
    """
    xA, yA = A.real, A.imag
    xB, yB = B.real, B.imag

    R2 = (xA - xB) ** 2 + (yA - yB) ** 2

    a = (rA * rA - rB * rB) / (2 * R2)
    c2 = 2 * (rA**2 + rB**2) / R2 - (rA * rA - rB * rB) ** 2 / R2**2 - 1
    if c2 < 0:
        return None, None
    c = math.sqrt(c2)

    fx = (xA + xB) / 2 + a * (xB - xA)
    gx = c * (yB - yA) / 2
    xP = fx + gx
    xQ = fx - gx

    fy = (yA + yB) / 2 + a * (yB - yA)
    gy = c * (xA - xB) / 2
    yP = fy + gy
    yQ = fy - gy

    P = xP + yP * 1j
    Q = xQ + yQ * 1j

    return P, Q


def save_as_png(canvas: Canvas):
    if hasattr(canvas, "frame_number"):
        canvas.update()
        eps = canvas.postscript(colormode="color")
        img = Image.open(BytesIO(bytes(eps, "utf-8")))
        filename = Path(f"frame{canvas.frame_number}")
        img.save(filename.with_suffix(".png"), "png")
        canvas.frame_number += 1


def make_animation(canvas: Canvas):
    if hasattr(canvas, "frame_number"):
        cmd = ["magick", "-delay", "10", "-loop", "0"]
        frames = []
        frames.extend(f"frame{i}.png" for i in range(canvas.frame_number))
        cmd.extend(frames)
        cmd.append("hyperbole.gif")
        print(f"animation avec {canvas.frame_number} images")
        subprocess.run(cmd)
        for i in frames:
            Path(i).unlink()


def key_callback(root: Tk, canvas: Canvas, event: Event):
    print(event)
    if event.keysym == "Escape" or event.keysym == "q":
        root.quit()
    elif event.keysym == "s":
        make_animation(canvas)
        root.quit()
    else:
        print(f"évenement inconnu: {event}")


parser = argparse.ArgumentParser(
    description="Dessine l'ensemble des points C tels que CA=CB+d."
    " A,B sont les foyers d'une l'hyperbole d'excentricité AB/d."
)
parser.add_argument("-d", type=float, default=5, help="difference (2a)")
parser.add_argument("-A", type=complex, default=-3, help="coordonnées du point A (complex)")
parser.add_argument("-B", type=complex, default=3, help="coordonnées du point B (complex)")
parser.add_argument("-s", "--save", action="store_true", help="active l'enregistrement de l'animation")
args = parser.parse_args()


A: complex = args.A
B: complex = args.B
d: float = args.d

if abs(A - B) <= d:
    parser.error(f"d = {d} doit être < {abs(A - B)}")

if A.real == B.real:
    parser.error("axe focal vertical non géré")

####

# données d'entrée
O = (A + B) / 2
a = d / 2
c = abs(A - B) / 2

b = math.sqrt(c**2 - a**2)
e = c / a
h = (c**2 - a**2) / c
f = a**2 / c
p = (c**2 - a**2) / a

table = []
table.append(("F₁", (A.real, A.imag), "foyer hyperbole"))
table.append(("F₂", (B.real, B.imag), "foyer hyperbole"))
table.append(("O", (O.real, O.imag), "centre de l'hyperbole"))
table.append(["a", a, "distance entre le centre de l'hyperbole et un de ses sommets"])
table.append(["c", c, "distance séparant le centre de l'hyperbole et un des foyers"])
table.append(["e", e, "excentricité de l’hyperbole"])
table.append(["b/a", b / a, "pente (en valeur absolue) que font les asymptotes avec l'axe focal"])
table.append(["p", p, "« paramètre » de l’hyperbole"])
table.append(["f", f, "distance séparant le centre de l’hyperbole et une de ses deux directrices"])
table.append(["h", h, "distance séparant un foyer F de sa directrice (d) associée"])
for row in table:
    if isinstance(row[1], float):
        row[1] = f"{row[1]:.4g}"
print(tabulate.tabulate(table))

####


root = Tk()
root.geometry("800x800")
f = Frame()
f.pack(fill=BOTH, expand=1)
canvas = Canvas(f, background="black")


canvas.pack(fill=BOTH, expand=1)
root.bind("<Key>", partial(key_callback, root, canvas))

canvas.update()

if args.save:
    canvas.frame_number = 0

SX = canvas.winfo_width()
SY = canvas.winfo_height() * 1j

MIN_X = -10
MAX_X = 10

MIN_Y = -10j
MAX_Y = 10j

canvas.create_rectangle(0, 0, canvas.winfo_width(), canvas.winfo_height(), outline="black", fill="black")
canvas.pack(fill=BOTH, expand=1)


def coord(pt: complex) -> t.Tuple[float, float]:
    x = (pt.real - MIN_X) * SX / (MAX_X - MIN_X)
    y = (MAX_Y.imag - pt.imag) * SY.imag / (MAX_Y.imag - MIN_Y.imag)
    return x, y


def line(A: complex, B: complex, **kwargs):
    return canvas.create_line(*coord(A), *coord(B), kwargs)


def circle(A: complex, r: float, **kwargs):
    ur = A + r * (1 + 1j)
    ll = A - r * (1 + 1j)
    return canvas.create_oval(*coord(ll), *coord(ur), kwargs)


def cross(A: complex, **kwargs):
    line(A - 0.2, A + 0.2, **kwargs)
    line(A - 0.2j, A + 0.2j, **kwargs)


# dessine le repère orthonormé
line(MIN_X, MAX_X, fill="blue", width=1)
line(MIN_Y, MAX_Y, fill="blue", width=1)

x = -1
while x > MIN_X:
    line(x + MIN_Y, x + MAX_Y, fill="gray18", width=1)
    line(x - 0.1j, x + 0.1j, fill="blue", width=1)
    x -= 1
x = 1
while x < MAX_X:
    line(x + MIN_Y, x + MAX_Y, fill="gray18", width=1)
    line(x - 0.1j, x + 0.1j, fill="blue", width=1)
    x += 1

y = -1j
while y.imag > MIN_Y.imag:
    line(y + MIN_X, y + MAX_X, fill="gray18", width=1)
    line(y - 0.1, y + 0.1, fill="blue", width=1)
    y -= 1j
y = 1j
while y.imag < MAX_Y.imag:
    line(y + MIN_X, y + MAX_X, fill="gray18", width=1)
    line(y - 0.1, y + 0.1, fill="blue", width=1)
    y += 1j


# centre des cercles/foyers hyberbole
cross(A, fill="cyan", width=1)
cross(B, fill="cyan", width=1)

# centre hyperbole
cross(O, fill="yellow")

# matrice de rotation (Ox) -> axe focal
M = np.array([[B.real - A.real, A.imag - B.imag], [B.imag - A.imag, B.real - A.real]]) / abs(A - B)


def rotation(x: complex) -> complex:
    x = x - O
    x = np.array([x.real, x.imag])
    r = np.dot(M, x)
    return complex(r[0], r[1]) + O


def droite(x: complex, p: float) -> complex:
    assert x.imag == 0
    y = p * (x.real - O.real) + O.imag
    return x + y * 1j


# axe focal
line(rotation(droite(-20, 0)), rotation(droite(20, 0)), dash="-", fill="yellow")


# asymptotes
line(rotation(droite(-20, b / a)), rotation(droite(20, b / a)), dash=".", fill="green")
line(rotation(droite(-20, -b / a)), rotation(droite(20, -b / a)), dash=".", fill="green")


cA, cB = None, None
dot_radius = 0.1 if args.save else 0.03


def intersect(r, d, min_r):
    global cA, cB

    P, Q = circle_intersect(A, r, B, r + d)
    if not P:
        return

    if d > 0:
        if cA:
            canvas.delete(cA)
        if cB:
            canvas.delete(cB)

        cA = circle(A, r, outline="red")
        cB = circle(B, r + d, outline="red")

    circle(P, dot_radius, fill="white")
    circle(Q, dot_radius, fill="white")

    save_as_png(canvas)

    # rend l'animation plus fluide
    if r - min_r > 2:
        e = 0.2
    elif r - min_r > 1:
        e = 0.1
    elif r - min_r > 0.1:
        e = 0.05
    else:
        e = 0.01
    r -= e

    if r > 0:
        root.after(20, lambda: intersect(r, d, min_r))


root.title("Construction par ensemble de points d'une hyperbole")
intersect(12, d, c - a)
intersect(12 + d, -d, c + a)

root.mainloop()

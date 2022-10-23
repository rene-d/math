#!/usr/bin/env python3

from tkinter import Tk, Canvas, Frame, BOTH
from typing import List
import random


root = Tk()
root.geometry("600x600")
f = Frame()
f.pack(fill=BOTH, expand=1)
canvas = Canvas(f, background="black")
root.title("Catch me if you can")

vA = 2 + 3j
vP = abs(vA) * 0.6
count = 0
coef = [1, 1]


def pursuit(A: complex, P: List[complex], oA=None, oP=None):

    global vA, Vp, count, coef

    count += 1
    if count >= 2000:
        canvas.create_text(canvas.winfo_width() / 2, canvas.winfo_height() / 2, text="YOU WIN 😁")
        return

    A2 = A + vA + random.randint(-2, 2) + random.randint(-2, 2) * 1j

    if A2.real > canvas.winfo_width() * 0.98:

        vA = -abs(vA.real) * random.randint(7, 13) / 10 + vA.imag * 1j
        while A2.real > canvas.winfo_width() * 0.98:
            A2 += vA

    elif A2.real < 0:
        vA = abs(vA.real) * random.randint(7, 13) / 10 + vA.imag * 1j
        while A2.real < 0:
            A2 += vA

    if A2.imag > canvas.winfo_height() * 0.98:
        vA = vA.real + abs(vA.imag) * -1j * random.randint(7, 13) / 10
        while A2.imag > canvas.winfo_height() * 0.98:
            A2 += vA

    elif A2.imag < 0:
        vA = vA.real + abs(vA.imag) * 1j * random.randint(7, 13) / 10
        while A2.imag < 0:
            A2 += vA

    if count % 16 == 0:
        coef[0] = random.randint(7, 13) / 10
        coef[1] = random.randint(7, 13) / 10

    P2 = list(p + (A - p) / abs(A - p) * vP * coef[i] for i, p in enumerate(P))

    if oA:
        canvas.delete(oA)
    if oP:
        for o in oP:
            canvas.delete(o)

    canvas.create_line(A.real, A.imag, A2.real, A2.imag, fill="green")
    oA = canvas.create_oval(A2.real - 4, A2.imag - 4, A2.real + 4, A2.imag + 4)

    oP = []
    for i, (p, p2) in enumerate(zip(P, P2)):
        canvas.create_line(p.real, p.imag, p2.real, p2.imag, fill=["red", "magenta"][i % 2])
        o = canvas.create_oval(p2.real - 4, p2.imag - 4, p2.real + 4, p2.imag + 4)
        oP.append(o)

    canvas.update()

    A, P = A2, P2
    delta = min(abs(A2 - p2) for p2 in P2)
    if delta < 5:
        canvas.create_text(canvas.winfo_width() / 2, canvas.winfo_height() / 2, text="GAME OVER")
        return

    delay = 1
    root.after(delay, lambda: pursuit(A, P, oA, oP))


def callback(event):
    if event.keysym == "Escape" or event.keysym == "q":
        root.quit()
    else:
        pass  # print(f"unknown event: {event}")


canvas.pack(fill=BOTH, expand=1)
canvas.update()

SX = canvas.winfo_width()
SY = canvas.winfo_height() * 1j

canvas.create_rectangle(0, 0, canvas.winfo_width(), canvas.winfo_height(), outline="black", fill="black")
canvas.pack(fill=BOTH, expand=1)

root.bind("<Key>", callback)

A = (SX + SY) * 0.05
P = [
    SX * 0.95 + SY * 0.05,
    SX * 0.05 + SY * 0.95,
]
pursuit(A, P)

root.mainloop()

#! /usr/bin/env python3
"""
Spirale d'Ulam

https://fr.wikipedia.org/wiki/Spirale_d%27Ulam
"""

import tkinter as tk


# teste si le nombre est premier
def premier(n):
    if n < 2:
        return False
    elif n == 2:
        return True
    elif n % 2 == 0:
        return False
    else:
        i = 3
        while i * i <= n:
            if n % i == 0:
                return False
            i = i + 2
        return True


root = tk.Tk()
root.wm_title("Spirale d'Ulam")

canvas = tk.Canvas(root, width=800, height=800)
canvas.grid()
canvas.update()

x = canvas.winfo_height() / 2
y = canvas.winfo_width() / 2

n = 0
C = 3
c = (C - 1) // 2


def ligne(i, dx, dy):
    global n, x, y

    for _ in range(i):
        n = n + 1
        if premier(n):
            canvas.create_rectangle(x - c, y - c, x + c, y + c, fill="black", outline="black")
        x += dx * C
        y += dy * C


i = 1
while n < 100000:
    ligne(i, 1, 0)
    ligne(i, 0, -1)
    i += 1
    ligne(i, -1, 0)
    ligne(i, 0, 1)
    i += 1

root.mainloop()

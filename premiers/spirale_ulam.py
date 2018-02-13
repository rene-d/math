#! /usr/bin/env python3
"""
Spirale d'Ulam

https://fr.wikipedia.org/wiki/Spirale_d%27Ulam
"""

import tkinter as tk
import time
from raise_app import raise_app


LENT = True


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
raise_app()

canvas = tk.Canvas(root, width=800, height=800)
canvas.grid()
canvas.update()

x = canvas.winfo_height() / 2
y = canvas.winfo_width() / 2

n = 0
C = 23
c = (C - 1) // 2 - 2


def ligne(i, dx, dy, couleur):
    global n, x, y

    for _ in range(i):
        canvas.create_line(x, y, x + dx * C, y + dy * C, width=3)

        n = n + 1
        if premier(n):
            canvas.create_rectangle(x - c, y - c, x + c, y + c, fill=couleur, outline=couleur)
            canvas.create_text(x, y, text=str(n), anchor=tk.CENTER, fill="white", font=('Arial', 8))
        else:
            canvas.create_rectangle(x - c, y - c, x + c, y + c, fill="white", outline=couleur)
            canvas.create_text(x, y, text=str(n), anchor=tk.CENTER, fill=couleur, font=('Arial', 8))

        x += dx * C
        y += dy * C
        if LENT:
            time.sleep(0.005)
            canvas.update()


i = 1
while (n + i * 4 + 2) < 1000:
    print(i,n)
    ligne(i, 1, 0, "black")
    ligne(i, 0, -1, "green")
    i += 1
    ligne(i, -1, 0, "blue")
    ligne(i, 0, 1, "red")
    i += 1

root.mainloop()

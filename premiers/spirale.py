"""
Spirale d'Ulam

https://fr.wikipedia.org/wiki/Spirale_d%27Ulam
"""

import tkinter as tk
import time


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

canvas = tk.Canvas(root, width=800, height=800)
canvas.grid()
canvas.update()

x = canvas.winfo_height() / 2
y = canvas.winfo_width() / 2

n = 0
C = 23
c = (C - 1) // 2 - 1


def ligne(i, dx, dy):
    global n, x, y

    for _ in range(i):
        canvas.create_line(x, y, x + dx * C, y + dy * C, width=3)

        n = n + 1
        if premier(n):
            canvas.create_rectangle(x - c, y - c, x + c, y + c, fill="black", outline="black")
            canvas.create_text(x, y, text=str(n), anchor=tk.CENTER, fill="white")
        else:
            canvas.create_rectangle(x - c, y - c, x + c, y + c, fill="white", outline="black")
            canvas.create_text(x, y, text=str(n), anchor=tk.CENTER, fill="black")

        x += dx * C
        y += dy * C
        if LENT:
            time.sleep(0.01)
            canvas.update()


i = 1
while (n + i * 4 + 2) < 1000:
    ligne(i, 1, 0)
    ligne(i, 0, -1)
    i += 1
    ligne(i, -1, 0)
    ligne(i, 0, 1)
    i += 1

root.mainloop()

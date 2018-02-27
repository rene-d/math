"""
Marsh Crossing

https://projecteuler.net/problem=607
"""

from p607 import *
import tkinter as tk


y0, y1, y2, y3, y4, y5 = res.x

w, h = 519, 321
m1, m2 = 175, 366

xA, yA = m1 - (m2 - m1) * (v2 - 1) / 2, 150
xB, yB = m2 + (m2 - m1) * (v2 - 1) / 2, 150

w, h = w * 2, h * 2
xB, yB = xB * 2, yB * 2
xA, yA = xA * 2, yA * 2

scale_x, scale_y = (xB - xA) / 100, -5.4


def tr(x, y):
    x, y = (x + y) / v2, (y - x) / v2
    return xA + (x - xa) * scale_x, yA + (y - ya) * scale_y


def point(x, y, size=1):
    x, y = tr(x, y)
    if size == 2:
        canvas.create_oval(x - 8, y - 8, x + 8, y + 8, fill="black", outline="black")
    elif size == 1:
        canvas.create_oval(x - 5, y - 5, x + 5, y + 4, fill="red", outline="red")
    else:
        canvas.create_oval(x - 3, y - 3, x + 3, y + 3, fill="blue", outline="blue")


root = tk.Tk()

canvas = tk.Canvas(root, width=w, height=h, borderwidth=0, highlightthickness=0)
canvas.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N))

image = tk.PhotoImage(file="p607_marsh.png")
image = image.zoom(2, 2)
canvas.create_image(0, 0, anchor=tk.NW, image=image)

canvas.create_line(tr(xa, ya), tr(xb, yb), width=2, fill="red")
canvas.create_line(tr(xa, ya), tr(x0, y0), tr(x1, y1), tr(x2, y2),
                   tr(x3, y3), tr(x4, y4), tr(x5, y5), tr(xb, yb), width=4, fill="green")

point(xa, ya, 2)
point(x0, y0)
point(x1, y1)
point(x2, y2)
point(x3, y3)
point(x4, y4)
point(x5, y5)
point(xb, yb, 2)

point(x0, x0, 0)
point(x1, x1, 0)
point(x2, x2, 0)
point(x3, x3, 0)
point(x4, x4, 0)
point(x5, x5, 0)

# pour régler scale_y
xx = None


def callback(event):
    global scale_y, xx
    if event.keysym == 'Right':
        scale_y -= 1
    elif event.keysym == 'Left':
        scale_y += 1
    elif event.keysym == 'Down':
        scale_y -= 0.1
    elif event.keysym == 'Up':
        scale_y += 0.1
    else:
        return
    print(scale_y)
    if xx is not None:
        canvas.delete(xx)
    xx = point(x0, y0, 0)


root.bind('<Key>', callback)

root.focus_set()
root.mainloop()

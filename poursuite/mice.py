#!/usr/bin/env python3

# The Mice problem
# https://en.wikipedia.org/wiki/Mice_problem

# Nota: for animation purpose, the mice do not move at regular speed
# but reduce the distance with the same ratio at each iteration.

import subprocess
from tkinter import Tk, Canvas, Frame, BOTH
import numpy as np
from PIL import Image
from pathlib import Path
import random
import argparse


for p in Path(".").glob("frame*.gif"):
    p.unlink()

root = Tk()
root.geometry("600x600")
f = Frame()
f.pack(fill=BOTH, expand=1)
canvas = Canvas(f, background="black")


def step(mice, speed):
    new_mice = []
    n = len(mice)
    for i in range(n):
        a = mice[i]
        b = mice[(i + 1) % n]
        new_mice.append(a + (b - a) * speed)
    return new_mice


def contour(mice):
    field = [(z.real, z.imag) for z in mice]
    field.append((mice[0].real, mice[0].imag))
    canvas.create_line(field)


def save_as_gif(canvas):
    if hasattr(canvas, "frame_number"):
        frame_number = canvas.frame_number

        canvas.update()
        canvas.postscript(file="frame.eps", colormode="color")

        img = Image.open("frame.eps")
        filename = Path(f"frame{frame_number}")
        img.save(filename.with_suffix(".gif"), "gif")

        Path("frame.eps").unlink()
        canvas.frame_number += 1


def pursuit(mice, speed, path=True, field=True, animation=False, colors=False):

    if isinstance(colors, list):
        pass
    elif isinstance(colors, str):
        colors = [colors]
    elif colors:
        colors = ["red", "blue", "orange", "green", "magenta", "yellow", "lightgreen", "gray", "beige"]
    else:
        colors = ["white"]

    while True:
        mice2 = step(mice, speed)

        if field:
            contour(mice2)

        if path:
            for i, (a, b) in enumerate(zip(mice, mice2)):
                canvas.create_line(a.real, a.imag, b.real, b.imag, fill=colors[i % len(colors)], width=6)

        delta = abs(mice[1] - mice[0])
        if delta < 5:
            root.title("Caught")
            return
        mice = mice2

        save_as_gif(canvas)

        if animation:
            delay = min(500, int(animation * delta))
            root.after(delay, lambda: pursuit(mice, speed=speed, path=path, field=field, animation=animation, colors=colors))
            break


def callback(event):
    if event.keysym == "Escape" or event.keysym == "q":
        root.quit()
    elif event.keysym == "s":
        if hasattr(canvas, "frame_number"):
            cmd = ["convert", "-delay", "10", "-loop", "0"]
            frames = []
            frames.extend(f"frame{i}.gif" for i in range(canvas.frame_number))
            cmd.extend(frames)
            cmd.extend(list(reversed(frames)))
            cmd.append("mice.gif")
            print(f"making animation with {canvas.frame_number} frames")
            subprocess.run(cmd)
            for i in range(canvas.frame_number):
                Path(f"frame{i}.gif").unlink()
            print("done")
            delattr(canvas, "frame_number")
    elif event.keysym == "o":
        root.quit()
        subprocess.run(["open", "mice.gif"])
    else:
        print(f"unknown event: {event}")


def ranged_type(value_type, min_value, max_value):
    def range_checker(arg: str):
        try:
            f = value_type(arg)
        except ValueError:
            raise argparse.ArgumentTypeError(f"must be a valid {value_type}")
        if f < min_value or f > max_value:
            raise argparse.ArgumentTypeError(f"must be within [{min_value}, {min_value}]")
        return f

    return range_checker


parser = argparse.ArgumentParser()
parser.add_argument("-s", "--speed", type=ranged_type(float, 0.0001, 0.9), default=0.1)
parser.add_argument("-m", "--mice", type=ranged_type(int, 3, 16), default=7)
parser.add_argument("-r", "--random", action="store_true")

args = parser.parse_args()

canvas.pack(fill=BOTH, expand=1)
canvas.update()

O = (canvas.winfo_width() + canvas.winfo_height() * 1j) / 2
R = min(canvas.winfo_width(), canvas.winfo_height()) / 2 * 0.9
mice = []
for i in range(args.mice):
    z = O + R * np.exp(2j * np.pi * i / args.mice - 2j * np.pi / 4)
    if args.random:
        z += random.randint(-100, 100) + 1j * random.randint(-100, 100)
    mice.append(z)

canvas.create_rectangle(0, 0, canvas.winfo_width(), canvas.winfo_height(), outline="black", fill="black")
contour(mice)
canvas.pack(fill=BOTH, expand=1)

canvas.frame_number = 0
save_as_gif(canvas)

pursuit(mice, args.speed, True, True, animation=0.1, colors=True)

root.bind("<Key>", callback)

root.mainloop()


for p in Path(".").glob("frame*.gif"):
    p.unlink()

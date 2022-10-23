#!/usr/bin/env python3

# The Dog problem
# https://en.wikipedia.org/wiki/Pursuit_curve

import subprocess
from tkinter import Tk, Canvas, Frame, BOTH
import numpy as np
from PIL import Image
from pathlib import Path
import argparse
from typing import List


for p in Path(".").glob("frame*.gif"):
    p.unlink()

root = Tk()
root.geometry("600x600")
f = Frame()
f.pack(fill=BOTH, expand=1)
canvas = Canvas(f, background="black")


def save_as_gif(canvas):
    if hasattr(canvas, "frame_number"):
        frame_number = canvas.frame_number

        canvas.update()
        canvas.postscript(file="frame.eps", colormode="color")

        img = Image.open("frame.eps")
        # img = img.rotate(15 * frame_number)
        filename = Path(f"frame{frame_number}")
        img.save(filename.with_suffix(".gif"), "gif")

        Path("frame.eps").unlink()
        canvas.frame_number += 1


def pursuit(A: complex, P: List[complex], oA=None, oP=None, animation=True):

    vA = 2 + 10j
    vP = 15

    while True:

        A2 = A + vA
        P2 = list(p + (A - p) / abs(A - p) * vP for p in P)

        if oA:
            canvas.delete(oA)
        if oP:
            for o in oP:
                canvas.delete(o)

        canvas.create_line(A.real, A.imag, A2.real, A2.imag, fill="blue")
        oA = canvas.create_oval(A2.real - 4, A2.imag - 4, A2.real + 4, A2.imag + 4)

        oP = []
        for p, p2 in zip(P, P2):
            canvas.create_line(p.real, p.imag, p2.real, p2.imag, fill="red")
            o = canvas.create_oval(p2.real - 4, p2.imag - 4, p2.real + 4, p2.imag + 4)
            oP.append(o)

        save_as_gif(canvas)

        A, P = A2, P2
        delta = min(abs(A2 - p2) for p2 in P2)
        if delta < 5:
            root.title("Caught")
            return

        if animation:
            delay = 0 if hasattr(canvas, "frame_number") else 100
            root.after(delay, lambda: pursuit(A, P, oA, oP, animation=animation))
            break


def pursuit_circle(C: complex, A: complex, angle: float, P: List[complex], speed=1.1, oA=None, oP=None, animation=True):

    R = 130  # radius of pursuee (A) path
    vA = 2 + 10j  # speed of pursuee
    vP = abs(vA) * speed  # speed of pursuer (P)

    vA_angular = abs(vA) / R  # angular speed

    if not A:
        A = C + R
        angle = 0

    while True:
        A2 = C + R * np.exp(1j * angle)
        P2 = list(p + (A - p) / abs(A - p) * vP for p in P)

        if oA:
            canvas.delete(oA)
        if oP:
            for o in oP:
                canvas.delete(o)

        canvas.create_line(A.real, A.imag, A2.real, A2.imag, fill="blue")
        oA = canvas.create_oval(A2.real - 4, A2.imag - 4, A2.real + 4, A2.imag + 4)

        oP = []
        for p, p2 in zip(P, P2):
            canvas.create_line(p.real, p.imag, p2.real, p2.imag, fill="red")
            o = canvas.create_oval(p2.real - 4, p2.imag - 4, p2.real + 4, p2.imag + 4)
            oP.append(o)

        save_as_gif(canvas)

        A, P = A2, P2
        angle += vA_angular

        delta = min(abs(A2 - p2) for p2 in P2)
        if delta < 10:
            root.title("Caught")
            return

        if animation:
            delay = 0 if hasattr(canvas, "frame_number") else 100
            root.after(delay, lambda: pursuit_circle(C, A, angle, P, speed=speed, oA=oA, oP=oP, animation=animation))
            break


def callback(event):
    if event.keysym == "Escape" or event.keysym == "q":
        root.quit()
    elif event.keysym == "s":
        if hasattr(canvas, "frame_number"):
            cmd = ["convert", "-delay", "20", "-loop", "0"]
            frames = []
            frames.extend(f"frame{i}.gif" for i in range(canvas.frame_number))
            cmd.extend(frames)
            cmd.append("dog.gif")
            print(f"making animation with {canvas.frame_number} frames")
            subprocess.run(cmd)
            for i in range(canvas.frame_number):
                Path(f"frame{i}.gif").unlink()
            print("done")
            delattr(canvas, "frame_number")
    elif event.keysym == "o":
        root.quit()
        subprocess.run(["open", "dog.gif"])
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
parser.add_argument("-s", "--speed", type=ranged_type(float, 0.1, 3), default=1.05)
parser.add_argument("-c", "--circle", action="store_true")
parser.add_argument("-4", "--circle4", action="store_true")

args = parser.parse_args()

canvas.pack(fill=BOTH, expand=1)
canvas.update()

SX = canvas.winfo_width()
SY = canvas.winfo_height() * 1j

canvas.create_rectangle(0, 0, canvas.winfo_width(), canvas.winfo_height(), outline="black", fill="black")
canvas.pack(fill=BOTH, expand=1)

root.bind("<Key>", callback)

canvas.frame_number = 0
save_as_gif(canvas)

if args.circle:
    A = 170 + SY * 0.5
    P = [SX * 0.95 + SY * 0.2]
    pursuit_circle(A, None, None, P, args.speed)

elif args.circle4:
    A = SX * 0.5 + SY * 0.5
    P = [
        SX * 0.95 + SY * 0.05,
        SX * 0.95 + SY * 0.95,
        SX * 0.05 + SY * 0.95,
        SX * 0.05 + SY * 0.05,
    ]
    pursuit_circle(A, None, None, P, args.speed)

else:
    A = (SX + SY) * 0.05
    P = [SX * 0.95 + SY * 0.3]
    pursuit(A, P)


root.mainloop()


for p in Path(".").glob("frame*.gif"):
    p.unlink()

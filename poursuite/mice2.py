#!/usr/bin/env python3

# The Mice problem
# https://en.wikipedia.org/wiki/Mice_problem

# Nota: for animation purpose, the mice do not move at regular speed
# but reduce the distance with the same ratio at each iteration.

import numpy as np
from PIL import Image, ImageDraw
from pathlib import Path
import random
import argparse
from typing import Tuple, List, Union
import subprocess


def c2xy(c: Union[complex, List[complex]]) -> Tuple[float, float]:
    """
    Convert a complex c to a tuple (x,y), or a list of c into a list of (x,y).
    """
    if isinstance(c, complex):
        return (round(c.real), round(c.imag))
    elif isinstance(c, list):
        return list(map(c2xy, c))
    else:
        raise ValueError()


def next_position(mice, speed):
    """
    Calculate the next position of mice.
    """
    new_mice = []
    n = len(mice)
    for i in range(n):
        a = mice[i]
        b = mice[(i + 1) % n]
        new_mice.append(a + (b - a) * speed)
    return new_mice


def pursuit(field_size, mice, speed, path=True, field=True, colors=True, animation=False, rotate=False):
    """
    Make mice pursue themselves in a regular polygon.
    """

    # color for the mice path
    if isinstance(colors, list):
        pass
    elif isinstance(colors, str):
        colors = [colors]
    elif colors:
        colors = ["red", "blue", "orange", "green", "magenta", "yellow", "lightgreen", "gray", "beige"]
    else:
        colors = ["white"]

    frame_number = 0

    im = Image.new("RGB", c2xy(field_size), (0, 0, 0))
    draw = ImageDraw.Draw(im)

    draw.polygon(c2xy(mice), outline="white", width=1)
    if animation:
        if rotate:
            z = mice[1] - mice[0]
            angle = np.arctan2(z.imag, z.real) * 180 / np.pi
            im2 = im.rotate(angle)
        else:
            im2 = im
        im2.save(f"frame{frame_number}.gif", "gif")

    # draw the path and the field until the mice catch themself
    while True:
        mice2 = next_position(mice, speed)

        if field:
            draw.polygon(c2xy(mice2), outline="white", width=1)

        if path:
            for i, (a, b) in enumerate(zip(mice, mice2)):
                draw.line((a.real, a.imag, b.real, b.imag), fill=colors[i % len(colors)], width=6)

        mice = mice2

        delta = abs(mice[1] - mice[0])
        if delta < 5:
            break

        if animation:
            # save the current image into a .gif
            if rotate:
                z = mice[1] - mice[0]
                angle = np.arctan2(z.imag, z.real) * 180 / np.pi
                im2 = im.rotate(angle)
            else:
                im2 = im
            im2.save(f"frame{frame_number}.gif", "gif")
            frame_number += 1

    if animation:
        # make a animated gif
        cmd = ["convert", "-delay", "10", "-loop", "0"]
        frames = []
        frames.extend(f"frame{i}.gif" for i in range(frame_number))
        cmd.extend(frames)
        cmd.extend(list(reversed(frames)))
        cmd.append("mice2.gif")
        print(f"making animation with {frame_number} frames")
        subprocess.run(cmd)
        for i in range(frame_number):
            Path(f"frame{i}.gif").unlink()

    else:
        if rotate:
            # make a spinning animation
            cmd = ["convert", "-delay", "5", "-loop", "0"]
            angle = 5
            for i in range(360 // angle):
                im2 = im.rotate(i * -angle)
                f = f"frame{i}.gif"
                im2.save(f, "gif")
                cmd.append(f)
            cmd.append("rotation.gif")
            print(f"making animation")
            subprocess.run(cmd)
            for i in range(360 // angle):
                Path(f"frame{i}.gif").unlink()
        else:
            # display the final image
            im.show()


def ranged_type(value_type, min_value, max_value):
    def range_checker(arg: str):
        try:
            f = value_type(arg)
        except ValueError:
            raise argparse.ArgumentTypeError(f"must be a valid {value_type}")
        if f < min_value or f > max_value:
            raise argparse.ArgumentTypeError(f"must be within [{min_value}, {max_value}]")
        return f

    return range_checker


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-s", "--speed", type=ranged_type(float, 0.0001, 0.9), default=0.1)
    parser.add_argument("-m", "--mice", type=ranged_type(int, 3, 16), default=7)
    parser.add_argument("-r", "--random", action="store_true")
    parser.add_argument("-a", "--animation", action="store_true")
    parser.add_argument("--rotate", action="store_true")
    parser.add_argument("-w", "--width", type=ranged_type(int, 100, 2048), default=512)

    args = parser.parse_args()

    field_size = (1 + 1j) * args.width

    O = field_size / 2
    R = min(field_size.real, field_size.imag) / 2 * 0.9
    mice = []
    for i in range(args.mice):
        z = O + R * np.exp(2j * np.pi * i / args.mice - 2j * np.pi / 4)
        if args.random:
            z += random.randint(-100, 100) + 1j * random.randint(-100, 100)
        mice.append(z)

    pursuit(field_size, mice, args.speed,  animation=args.animation, rotate=args.rotate)


if __name__ == "__main__":
    main()

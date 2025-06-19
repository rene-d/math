#!/usr/bin/env python3

from PIL import Image
import numpy as np
from imgcat import imgcat
import imageio
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("R", nargs="?", default=100, type=float)
args = parser.parse_args()

width = 800
height = 800
C = width / 10
R = args.R

with imageio.get_writer("anim.gif", mode="I") as writer:

    for a in range(0, 100, 1):

        im = Image.new("RGB", (width, height), (255, 255, 255))

        P = complex(width / 2, height / 2)

        delta = -a * 2 + 50j

        rho = np.exp(1j * np.deg2rad(a))
        rho /= 1 + a / 50

        for x in range(width):
            for y in range(height):

                z = np.complex64(x, y) - P

                # translation
                z = z + delta

                # rotation/homothétie
                z = z * rho

                # inversion
                z = (R + a / 2) ** 2 / (z + 0.0000001)

                # coloration échiquier
                z /= C
                color = (np.floor(z.real) + np.floor(z.imag)) % 2 == 1

                if color:
                    r = int((220) / width * x) % 256
                    g = int(a)
                    b = int((200) / height * y) % 256

                    im.putpixel((x, y), (r, g, b))

        imgcat(im, height=15)
        writer.append_data(im)

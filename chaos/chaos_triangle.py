#!/usr/bin/env python3
"""
Jeu du chaos sur un triangle ABC quelconque (tkinter, stdlib uniquement).

Algorithme :
    P_{n+1} = milieu(P_n, V) avec V tiré uniformément dans {A, B, C}
    P_0 tiré uniformément dans le triangle.
Seuls les P_n (n > skip) sont affichés.

Rendu : buffer stocké directement en scanlines PNG (octet de filtre inclus)
-> zlib -> base64 -> tk.PhotoImage. Le handler PPM de Tk ne décode pas le
base64, contrairement au handler PNG ; d'où l'encodage PNG.

Deux modes : rendu immédiat ("Dessiner") ou animation incrémentale
("Animer"), qui réutilise le même raster et ne fait que le ré-encoder.
"""

import base64
import os
import random
import struct
import tempfile
import time
import tkinter as tk
import zlib
from itertools import islice
from tkinter import ttk, messagebox

# --------------------------------------------------------------- paramètres
W, H = 900, 720            # taille du rendu en pixels
MARGIN = 24                # marge en pixels
BG = (14, 14, 18)
COLORS = ((255, 86, 86), (80, 220, 130), (105, 160, 255))   # A, B, C
MONO = (235, 235, 235)
SKIP = 20                  # points du transitoire non tracés
BATCH = 5000               # points par frame d'animation (défaut)
FRAME_MS = 16              # période d'affichage visée (~60 images/s)


# ------------------------------------------------------------ partie "pure"
def triangle_area2(A, B, C):
    """Double aire signée."""
    return (B[0] - A[0]) * (C[1] - A[1]) - (C[0] - A[0]) * (B[1] - A[1])


def iter_points(A, B, C, n, skip=SKIP, rng=None):
    """Génère n couples ((x, y), index_du_sommet_choisi)."""
    rng = rng or random.Random()
    verts = (A, B, C)

    # P0 uniforme dans le triangle (repliement du carré unité)
    u, v = rng.random(), rng.random()
    if u + v > 1.0:
        u, v = 1.0 - u, 1.0 - v
    x = A[0] + u * (B[0] - A[0]) + v * (C[0] - A[0])
    y = A[1] + u * (B[1] - A[1]) + v * (C[1] - A[1])

    randrange = rng.randrange
    for _ in range(skip):
        vx, vy = verts[randrange(3)]
        x, y = (x + vx) * 0.5, (y + vy) * 0.5

    for _ in range(n):
        k = randrange(3)
        vx, vy = verts[k]
        x, y = (x + vx) * 0.5, (y + vy) * 0.5
        yield (x, y), k


def fit_transform(A, B, C, w=W, h=H, margin=MARGIN):
    """Affine monde -> pixels, isotrope (pas de déformation), y inversé."""
    xs, ys = (A[0], B[0], C[0]), (A[1], B[1], C[1])
    minx, maxx, miny, maxy = min(xs), max(xs), min(ys), max(ys)
    spanx, spany = max(maxx - minx, 1e-12), max(maxy - miny, 1e-12)
    s = min((w - 2 * margin) / spanx, (h - 2 * margin) / spany)
    offx = (w - s * spanx) * 0.5 - s * minx
    offy = (h - s * spany) * 0.5 - s * miny
    return s, offx, offy


class Raster:
    """Buffer RGB8 stocké au format scanline PNG : chaque ligne est précédée
    de son octet de filtre (0 = None). Encoder = zlib.compress(self.raw).
    """

    def __init__(self, w=W, h=H, bg=BG):
        self.w, self.h = w, h
        self.stride = 1 + 3 * w
        row = b"\x00" + bytes(bg) * w
        self.raw = bytearray(row * h)

    def set(self, px, py, col):
        if 0 <= px < self.w and 0 <= py < self.h:
            i = py * self.stride + 1 + 3 * px
            self.raw[i:i + 3] = col
            return True
        return False

    def png(self, level=1):
        def chunk(tag, data):
            body = tag + data
            return (struct.pack(">I", len(data)) + body
                    + struct.pack(">I", zlib.crc32(body) & 0xFFFFFFFF))

        ihdr = struct.pack(">IIBBBBB", self.w, self.h, 8, 2, 0, 0, 0)
        return (b"\x89PNG\r\n\x1a\n"
                + chunk(b"IHDR", ihdr)
                + chunk(b"IDAT", zlib.compress(bytes(self.raw), level))
                + chunk(b"IEND", b""))


def palette(color_by_vertex):
    return ([bytes(c) for c in COLORS] if color_by_vertex
            else [bytes(MONO)] * 3)


def plot_into(raster, points, tf, cols):
    """Trace des points ((x, y), k) dans le raster. Retourne le nb tracés."""
    s, offx, offy = tf
    h = raster.h
    drawn = 0
    for (x, y), k in points:
        drawn += raster.set(int(s * x + offx), h - 1 - int(s * y + offy),
                            cols[k])
    return drawn


def render_png(A, B, C, n, color_by_vertex=True, skip=SKIP, rng=None,
               w=W, h=H):
    """Rendu complet en un coup. Retourne (bytes PNG, nb de points tracés)."""
    if abs(triangle_area2(A, B, C)) < 1e-12:
        raise ValueError("Triangle dégénéré (A, B, C alignés ou confondus).")
    raster = Raster(w, h)
    drawn = plot_into(raster, iter_points(A, B, C, n, skip, rng),
                      fit_transform(A, B, C, w, h), palette(color_by_vertex))
    return raster.png(), drawn


# ------------------------------------------------------------------- la GUI
class App(ttk.Frame):
    DEFAULTS = {"Ax": "0", "Ay": "0", "Bx": "1", "By": "0",
                "Cx": "0.5", "Cy": "0.8660254", "N": "200000", "seed": "",
                "batch": str(BATCH)}

    def __init__(self, master):
        super().__init__(master, padding=8)
        self.grid(sticky="nsew")
        master.columnconfigure(0, weight=1)
        master.rowconfigure(0, weight=1)

        self.vars = {k: tk.StringVar(value=v) for k, v in self.DEFAULTS.items()}
        self.color_var = tk.BooleanVar(value=True)
        self.photo = None
        self.img_id = None
        self._anim_id = None          # id du after() en cours, None si arrêt
        self._gen = None

        bar = ttk.Frame(self)
        bar.grid(row=0, column=0, sticky="ew", pady=(0, 8))

        def field(parent, label, key, width=9):
            ttk.Label(parent, text=label).pack(side="left", padx=(6, 2))
            e = ttk.Entry(parent, textvariable=self.vars[key], width=width)
            e.pack(side="left")
            e.bind("<Return>", lambda _e: self.draw())
            return e

        for name, kx, ky in (("A", "Ax", "Ay"), ("B", "Bx", "By"),
                             ("C", "Cx", "Cy")):
            field(bar, f"{name}x", kx)
            field(bar, f"{name}y", ky)

        bar2 = ttk.Frame(self)
        bar2.grid(row=1, column=0, sticky="ew", pady=(0, 8))
        field(bar2, "N", "N", 12)
        field(bar2, "seed", "seed", 10)
        field(bar2, "pts/frame", "batch", 8)
        ttk.Checkbutton(bar2, text="couleur par sommet",
                        variable=self.color_var).pack(side="left", padx=10)
        ttk.Button(bar2, text="Dessiner", command=self.draw).pack(side="left")
        # width fixe : sinon "Animer" -> "Stop" retaille la barre d'outils.
        self.anim_btn = ttk.Button(bar2, text="Animer", width=8,
                                   command=self.toggle_anim)
        self.anim_btn.pack(side="left", padx=4)
        ttk.Button(bar2, text="Triangle aléatoire",
                   command=self.randomize).pack(side="left", padx=6)

        # Le statut a sa propre ligne : dans la barre d'outils, sa largeur
        # variable redimensionnait la fenêtre à chaque frame.
        self.status = ttk.Label(self, text="", anchor="w")
        self.status.grid(row=3, column=0, sticky="w", pady=(4, 0))

        self.canvas = tk.Canvas(self, width=W, height=H, bg="#0e0e12",
                                highlightthickness=0)
        self.canvas.grid(row=2, column=0, sticky="nsew")
        self.columnconfigure(0, weight=1)
        self.rowconfigure(2, weight=1)

        master.protocol("WM_DELETE_WINDOW", self._on_close)
        self.after(50, self.draw)

    # ------------------------------------------------------------- helpers
    def _read(self):
        f = lambda k: float(self.vars[k].get().replace(",", "."))
        A = (f("Ax"), f("Ay"))
        B = (f("Bx"), f("By"))
        C = (f("Cx"), f("Cy"))
        if abs(triangle_area2(A, B, C)) < 1e-12:
            raise ValueError("Triangle dégénéré (A, B, C alignés ou "
                             "confondus).")
        n = int(float(self.vars["N"].get()))
        if n <= 0:
            raise ValueError("N doit être > 0.")
        batch = int(float(self.vars["batch"].get()))
        if batch <= 0:
            raise ValueError("pts/frame doit être > 0.")
        seed = self.vars["seed"].get().strip()
        rng = random.Random(seed) if seed else random.Random()
        return A, B, C, n, batch, rng

    @staticmethod
    def _b64(png):
        return base64.b64encode(png).decode("ascii")

    def _show(self, png):
        """Affiche le PNG ; réutilise le même PhotoImage entre les frames.

        "put" écrase les pixels en place, alors que configure(-data) vide
        l'image avant de la relire : c'est ce blanc fugitif qui faisait
        scintiller l'animation.
        """
        b64 = self._b64(png)
        if self.photo is None:
            self.photo = self._make_photo(png)
            self.img_id = self.canvas.create_image(0, 0, image=self.photo,
                                                   anchor="nw")
            return
        try:
            self.tk.call(self.photo, "put", b64, "-format", "png",
                         "-to", 0, 0)
        except tk.TclError:                   # Tk trop ancien pour put -format
            self.photo = self._make_photo(png)
            self.canvas.itemconfigure(self.img_id, image=self.photo)

    @staticmethod
    def _make_photo(png):
        """base64 -> PhotoImage ; repli sur un fichier temporaire si le Tk
        local refuse les données inline."""
        b64 = base64.b64encode(png).decode("ascii")
        try:
            return tk.PhotoImage(data=b64, format="png")
        except tk.TclError:
            fd, path = tempfile.mkstemp(suffix=".png")
            try:
                with os.fdopen(fd, "wb") as fh:
                    fh.write(png)
                return tk.PhotoImage(file=path, format="png")
            finally:
                try:
                    os.unlink(path)
                except OSError:
                    pass

    def randomize(self):
        self.stop_anim()
        rng = random.Random()
        while True:
            pts = [(rng.uniform(0, 1), rng.uniform(0, 1)) for _ in range(3)]
            if abs(triangle_area2(*pts)) > 0.08:
                break
        for (px, py), (kx, ky) in zip(pts, (("Ax", "Ay"), ("Bx", "By"),
                                            ("Cx", "Cy"))):
            self.vars[kx].set(f"{px:.4f}")
            self.vars[ky].set(f"{py:.4f}")
        self.draw()

    # --------------------------------------------------------- rendu direct
    def draw(self):
        self.stop_anim()
        try:
            A, B, C, n, _batch, rng = self._read()
        except ValueError as exc:
            messagebox.showerror("Paramètres invalides", str(exc))
            return
        self.status.config(text="calcul...")
        self.update_idletasks()
        t0 = time.perf_counter()
        png, drawn = render_png(A, B, C, n, self.color_var.get(), rng=rng)
        dt = time.perf_counter() - t0
        self._show(png)
        self.status.config(text=f"{drawn} points  |  {dt * 1000:.0f} ms")

    # ------------------------------------------------------------ animation
    def toggle_anim(self):
        if self._anim_id is not None:
            self.stop_anim(note=" (arrêté)")
        else:
            self.start_anim()

    def start_anim(self):
        try:
            A, B, C, n, batch, rng = self._read()
        except ValueError as exc:
            messagebox.showerror("Paramètres invalides", str(exc))
            return
        self._raster = Raster()
        self._tf = fit_transform(A, B, C)
        self._cols = palette(self.color_var.get())
        self._gen = iter_points(A, B, C, n, SKIP, rng)
        self._total, self._done, self._batch = n, 0, batch
        self._t0 = time.perf_counter()
        self._show(self._raster.png())
        self.anim_btn.config(text="Stop")
        self._anim_id = self.after(10, self._anim_step)

    def stop_anim(self, note=""):
        if self._anim_id is not None:
            self.after_cancel(self._anim_id)
            self._anim_id = None
            self._gen = None
            self.anim_btn.config(text="Animer")
            if note:
                self.status.config(text=self.status.cget("text") + note)

    def _anim_step(self):
        self._anim_id = None
        t0 = time.perf_counter()
        chunk = list(islice(self._gen, self._batch))
        self._done += plot_into(self._raster, chunk, self._tf, self._cols)
        self._show(self._raster.png())
        frame_ms = (time.perf_counter() - t0) * 1000
        pct = 100.0 * self._done / max(self._total, 1)
        self.status.config(
            text=f"{self._done}/{self._total} points ({pct:.1f} %)  |  "
                 f"{frame_ms:.0f} ms/frame  |  "
                 f"{time.perf_counter() - self._t0:.1f} s")
        if len(chunk) < self._batch:          # générateur épuisé
            self._gen = None
            self.anim_btn.config(text="Animer")
            return
        # On laisse respirer la boucle Tk : enchaînées toutes les 1 ms, les
        # demandes de redessin arrivaient bien plus vite que l'écran ne
        # rafraîchit. Régler la vitesse avec pts/frame, pas avec le délai.
        self._anim_id = self.after(max(1, int(FRAME_MS - frame_ms)),
                                   self._anim_step)

    def _on_close(self):
        self.stop_anim()
        self.master.destroy()


def main():
    root = tk.Tk()
    root.title("Jeu du chaos - triangle ABC")
    App(root)
    root.mainloop()


if __name__ == "__main__":
    main()

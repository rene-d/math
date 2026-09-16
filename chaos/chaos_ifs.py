#!/usr/bin/env python3
"""
Jeu du chaos généralisé : IFS affines quelconques + polygones avec règles
de transition (chaînes de Markov sur les sommets).

Réutilise l'ossature de chaos_triangle.py (Raster scanline-PNG, animation
incrémentale via after()). Stdlib uniquement.

Convention : rapport de CONTRACTION s, soit P' = V + s*(P - V) pour les
jeux "sommet", et P' = (a x + b y + e, c x + d y + f) pour les IFS affines.
Attention : P' = P + r*(V - P) contracte d'un facteur (1 - r), pas r.
"""

import base64
import math
import os
import random
import struct
import tempfile
import time
import tkinter as tk
import zlib
from bisect import bisect
from itertools import islice
from tkinter import ttk, messagebox

W, H = 900, 720
MARGIN = 24
BG = (14, 14, 18)
SKIP = 30
BBOX_SAMPLE = 20000
BATCH = 8000
FRAME_MS = 16              # période d'affichage visée (~60 images/s)
PALETTE = ((255, 86, 86), (80, 220, 130), (105, 160, 255), (255, 196, 70),
           (220, 110, 255), (90, 230, 230), (245, 245, 245), (255, 140, 60))


# -------------------------------------------------------------- générateurs
def poly_vertices(n, radius=1.0):
    a0 = math.pi / 2
    return [(radius * math.cos(a0 + 2 * math.pi * k / n),
             radius * math.sin(a0 + 2 * math.pi * k / n)) for k in range(n)]


def poly_points(verts, s, rule, n, skip=SKIP, rng=None):
    """Jeu du chaos sur des sommets, avec règle de transition optionnelle.
    rule : None | 'norepeat' (jamais deux fois le même sommet)
                | 'noopp'    (jamais le sommet diamétralement opposé)
                | 'noadj'    (jamais un sommet adjacent au précédent)
    """
    rng = rng or random.Random()
    nv = len(verts)
    u, v = rng.random(), rng.random()
    if u + v > 1.0:
        u, v = 1.0 - u, 1.0 - v
    A, B, C = verts[0], verts[1 % nv], verts[2 % nv]
    x = A[0] + u * (B[0] - A[0]) + v * (C[0] - A[0])
    y = A[1] + u * (B[1] - A[1]) + v * (C[1] - A[1])

    if rule is None:
        allowed = list(range(nv))
    elif rule == 'norepeat':
        allowed = [d for d in range(nv) if d != 0]
    elif rule == 'noopp':
        allowed = [d for d in range(nv) if d != nv // 2]
    elif rule == 'noadj':
        allowed = [d for d in range(nv) if d not in (1, nv - 1)]
    else:
        raise ValueError(f"règle inconnue : {rule}")
    if not allowed:
        raise ValueError("règle trop restrictive : aucun sommet autorisé")

    prev = rng.randrange(nv)
    choice = rng.choice
    for i in range(n + skip):
        k = (prev + choice(allowed)) % nv if rule else rng.randrange(nv)
        vx, vy = verts[k]
        x, y = vx + s * (x - vx), vy + s * (y - vy)
        prev = k
        if i >= skip:
            yield (x, y), k


def ifs_points(maps, probs, n, skip=SKIP, rng=None):
    """maps : liste de (a, b, c, d, e, f) ; x' = a x + b y + e, y' = c x + d y + f."""
    rng = rng or random.Random()
    cum, acc = [], 0.0
    for p in probs:
        acc += p
        cum.append(acc)
    x = y = 0.0
    rnd = rng.random
    for i in range(n + skip):
        k = bisect(cum, rnd() * acc)
        if k >= len(maps):
            k = len(maps) - 1
        a, b, c, d, e, f = maps[k]
        x, y = a * x + b * y + e, c * x + d * y + f
        if i >= skip:
            yield (x, y), k


def det_probs(maps, floor=0.01):
    """Probabilités ~ |det| (heuristique de Barnsley) : équirépartit le temps
    de calcul sur l'aire couverte. Ne change PAS l'attracteur, seulement la
    mesure invariante -- donc la vitesse de remplissage du rendu."""
    w = [max(abs(a * d - b * c), floor) for a, b, c, d, _e, _f in maps]
    t = sum(w)
    return [x / t for x in w]


# ------------------------------------------------------------------ presets
def _koch():
    r, h = 1 / 3, math.sqrt(3) / 6
    c, s = math.cos(math.pi / 3) / 3, math.sin(math.pi / 3) / 3
    return [(r, 0, 0, r, 0, 0),
            (c, -s, s, c, 1 / 3, 0),
            (c, s, -s, c, 1 / 2, h),
            (r, 0, 0, r, 2 / 3, 0)]


def _grid_ifs(keep, m=3):
    """Sous-carrés d'une grille m x m, rapport 1/m. keep : liste de (i, j)."""
    return [(1 / m, 0, 0, 1 / m, i / m, j / m) for i, j in keep]


PHI = (1 + 5 ** 0.5) / 2
PRESETS = {}


def _add(name, kind, data, note=""):
    PRESETS[name] = (kind, data, note)


_add("Sierpinski (triangle, s=1/2)", "poly", (3, 0.5, None), "dim log3/log2")
_add("Carré s=1/2 (dégénéré)", "poly", (4, 0.5, None),
     "aucune structure : les 4 copies pavent le carré, dim 2")
_add("Carré s=1/2, sans répétition", "poly", (4, 0.5, 'norepeat'),
     "sous-décalage de type fini, dim log3/log2")
_add("Carré s=1/2, sans opposé", "poly", (4, 0.5, 'noopp'), "dim log3/log2")
_add("Carré s=1/3 (poussière)", "poly", (4, 1 / 3, None), "dim log4/log3")
_add("Pentaflake (s=1/phi^2)", "poly", (5, 1 / PHI ** 2, None),
     "dim log5/log(phi^2)")
_add("Hexaflake (s=1/3)", "poly", (6, 1 / 3, None), "dim log6/log3")
_add("Tapis de Sierpinski", "ifs",
     (_grid_ifs([(i, j) for i in range(3) for j in range(3)
                 if (i, j) != (1, 1)]), None), "dim log8/log3")
_add("Fractale de Vicsek", "ifs",
     (_grid_ifs([(1, 1), (0, 0), (2, 0), (0, 2), (2, 2)]), None),
     "dim log5/log3")
_add("Courbe de Koch", "ifs", (_koch(), None), "dim log4/log3")
_add("Dragon de Heighway", "ifs",
     ([(0.5, -0.5, 0.5, 0.5, 0, 0), (-0.5, -0.5, 0.5, -0.5, 1, 0)], None),
     "dim 2 (intérieur non vide) ; le bord est de dim ~1.5236")
_add("Courbe C de Lévy", "ifs",
     ([(0.5, 0.5, -0.5, 0.5, 0, 0), (0.5, -0.5, 0.5, 0.5, 0.5, -0.5)], None),
     "les deux moitiés se raccordent en (1/2, -1/2)")
_add("Fougère de Barnsley", "ifs",
     ([(0, 0, 0, 0.16, 0, 0),
       (0.85, 0.04, -0.04, 0.85, 0, 1.6),
       (0.2, -0.26, 0.23, 0.22, 0, 1.6),
       (-0.15, 0.28, 0.26, 0.24, 0, 0.44)],
      [0.01, 0.85, 0.07, 0.07]), "probabilités non uniformes indispensables")


def make_generator(preset, n, rng):
    kind, data, _note = PRESETS[preset]
    if kind == "poly":
        nv, s, rule = data
        return poly_points(poly_vertices(nv), s, rule, n, SKIP, rng)
    maps, probs = data
    return ifs_points(maps, probs or det_probs(maps), n, SKIP, rng)


# ------------------------------------------------------------------- raster
class Raster:
    """Buffer RGB8 stocké au format scanline PNG (octet de filtre inclus)."""

    def __init__(self, w=W, h=H, bg=BG):
        self.w, self.h = w, h
        self.stride = 1 + 3 * w
        self.raw = bytearray((b"\x00" + bytes(bg) * w) * h)

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

        return (b"\x89PNG\r\n\x1a\n"
                + chunk(b"IHDR", struct.pack(">IIBBBBB", self.w, self.h,
                                             8, 2, 0, 0, 0))
                + chunk(b"IDAT", zlib.compress(bytes(self.raw), level))
                + chunk(b"IEND", b""))


def bbox_of(preset, rng_seed, sample=BBOX_SAMPLE):
    """Pré-passe : l'attracteur d'un IFS quelconque n'a pas de boîte connue
    a priori, on l'estime sur un échantillon."""
    g = make_generator(preset, sample, random.Random(rng_seed))
    xs0 = ys0 = float("inf")
    xs1 = ys1 = float("-inf")
    for (x, y), _k in g:
        xs0, xs1 = min(xs0, x), max(xs1, x)
        ys0, ys1 = min(ys0, y), max(ys1, y)
    if not (xs1 > xs0 or ys1 > ys0):
        raise ValueError("attracteur dégénéré (ponctuel)")
    return xs0, xs1, ys0, ys1


def fit_transform(bbox, w=W, h=H, margin=MARGIN):
    xs0, xs1, ys0, ys1 = bbox
    spanx, spany = max(xs1 - xs0, 1e-12), max(ys1 - ys0, 1e-12)
    s = min((w - 2 * margin) / spanx, (h - 2 * margin) / spany)
    return s, (w - s * spanx) * 0.5 - s * xs0, (h - s * spany) * 0.5 - s * ys0


def plot_into(raster, points, tf, cols):
    s, offx, offy = tf
    h = raster.h
    drawn = 0
    for (x, y), k in points:
        drawn += raster.set(int(s * x + offx), h - 1 - int(s * y + offy),
                            cols[k % len(cols)])
    return drawn


def render_png(preset, n, mono=False, seed=None, w=W, h=H):
    rng = random.Random(seed)
    raster = Raster(w, h)
    tf = fit_transform(bbox_of(preset, seed), w, h)
    cols = [bytes((235, 235, 235))] * 8 if mono else [bytes(c) for c in PALETTE]
    drawn = plot_into(raster, make_generator(preset, n, rng), tf, cols)
    return raster.png(), drawn


# ---------------------------------------------------------------------- GUI
class App(ttk.Frame):
    def __init__(self, master):
        super().__init__(master, padding=8)
        self.grid(sticky="nsew")
        master.columnconfigure(0, weight=1)
        master.rowconfigure(0, weight=1)

        self.preset = tk.StringVar(value=next(iter(PRESETS)))
        self.n_var = tk.StringVar(value="300000")
        self.batch_var = tk.StringVar(value=str(BATCH))
        self.seed_var = tk.StringVar(value="")
        self.mono = tk.BooleanVar(value=False)
        self.photo = self.img_id = self._anim_id = self._gen = None

        bar = ttk.Frame(self)
        bar.grid(row=0, column=0, sticky="ew", pady=(0, 6))
        ttk.Label(bar, text="fractale").pack(side="left", padx=(0, 4))
        cb = ttk.Combobox(bar, textvariable=self.preset, values=list(PRESETS),
                          state="readonly", width=32)
        cb.pack(side="left")
        cb.bind("<<ComboboxSelected>>", lambda _e: self.draw())
        for label, var, wdt in (("N", self.n_var, 10),
                                ("pts/frame", self.batch_var, 7),
                                ("seed", self.seed_var, 7)):
            ttk.Label(bar, text=label).pack(side="left", padx=(10, 2))
            e = ttk.Entry(bar, textvariable=var, width=wdt)
            e.pack(side="left")
            e.bind("<Return>", lambda _e: self.draw())
        ttk.Checkbutton(bar, text="mono", variable=self.mono).pack(side="left",
                                                                   padx=8)
        ttk.Button(bar, text="Dessiner", command=self.draw).pack(side="left")
        # width fixe : sinon "Animer" -> "Stop" retaille la barre d'outils.
        self.anim_btn = ttk.Button(bar, text="Animer", width=8,
                                   command=self.toggle_anim)
        self.anim_btn.pack(side="left", padx=4)

        self.note = ttk.Label(self, text="")
        self.note.grid(row=1, column=0, sticky="w", pady=(0, 6))
        self.status = ttk.Label(self, text="")
        self.status.grid(row=3, column=0, sticky="w", pady=(4, 0))

        self.canvas = tk.Canvas(self, width=W, height=H, bg="#0e0e12",
                                highlightthickness=0)
        self.canvas.grid(row=2, column=0, sticky="nsew")
        self.columnconfigure(0, weight=1)
        self.rowconfigure(2, weight=1)
        master.protocol("WM_DELETE_WINDOW", self._on_close)
        self.after(50, self.draw)

    def _read(self):
        n = int(float(self.n_var.get()))
        batch = int(float(self.batch_var.get()))
        if n <= 0 or batch <= 0:
            raise ValueError("N et pts/frame doivent être > 0.")
        seed = self.seed_var.get().strip() or None
        return self.preset.get(), n, batch, seed

    def _cols(self):
        return ([bytes((235, 235, 235))] * 8 if self.mono.get()
                else [bytes(c) for c in PALETTE])

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

    def draw(self):
        self.stop_anim()
        try:
            preset, n, _b, seed = self._read()
        except ValueError as exc:
            messagebox.showerror("Paramètres invalides", str(exc))
            return
        self.note.config(text=PRESETS[preset][2])
        self.status.config(text="calcul...")
        self.update_idletasks()
        t0 = time.perf_counter()
        png, drawn = render_png(preset, n, self.mono.get(), seed)
        self._show(png)
        self.status.config(text=f"{drawn} points  |  "
                                f"{(time.perf_counter() - t0) * 1000:.0f} ms")

    def toggle_anim(self):
        if self._anim_id is not None:
            self.stop_anim(note=" (arrêté)")
        else:
            self.start_anim()

    def start_anim(self):
        try:
            preset, n, batch, seed = self._read()
        except ValueError as exc:
            messagebox.showerror("Paramètres invalides", str(exc))
            return
        self.note.config(text=PRESETS[preset][2])
        self._raster = Raster()
        self._tf = fit_transform(bbox_of(preset, seed))
        self._pal = self._cols()
        self._gen = make_generator(preset, n, random.Random(seed))
        self._total, self._done, self._batch = n, 0, batch
        self._t0 = time.perf_counter()
        self._show(self._raster.png())
        self.anim_btn.config(text="Stop")
        self._anim_id = self.after(10, self._anim_step)

    def stop_anim(self, note=""):
        if self._anim_id is not None:
            self.after_cancel(self._anim_id)
            self._anim_id = self._gen = None
            self.anim_btn.config(text="Animer")
            if note:
                self.status.config(text=self.status.cget("text") + note)

    def _anim_step(self):
        self._anim_id = None
        t0 = time.perf_counter()
        chunk = list(islice(self._gen, self._batch))
        self._done += plot_into(self._raster, chunk, self._tf, self._pal)
        self._show(self._raster.png())
        frame_ms = (time.perf_counter() - t0) * 1000
        pct = 100.0 * self._done / max(self._total, 1)
        self.status.config(text=f"{self._done}/{self._total} ({pct:.1f} %)  |  "
                                f"{frame_ms:.0f} ms/frame  |  "
                                f"{time.perf_counter() - self._t0:.1f} s")
        if len(chunk) < self._batch:
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
    root.title("Jeu du chaos - IFS")
    App(root)
    root.mainloop()


if __name__ == "__main__":
    main()

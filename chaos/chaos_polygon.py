#!/usr/bin/env python3
"""Jeu du chaos sur un n-gone, à rapport de contraction réglable.

Script indépendant (stdlib seule) : il n'a qu'un sujet, le jeu des sommets

    f_k(P) = V_k + s * (P - V_k),   V_k sommets du n-gone régulier

avec n, s et la règle de transition réglables, et un balayage de s. Le
catalogue de fractales (IFS affines, Koch, dragon, fougère...) est dans
chaos_ifs.py, qui est un programme séparé.

Attention : P' = P + r*(V - P) contracte d'un facteur (1 - r), pas r. Ici s
est le rapport de contraction lui-même ; s = 1/2 est le jeu classique.

Trois seuils, calculés et non codés en dur :

  s*        contact. Deux copies se rencontrent quand (1-s)(V_j - V_i) entre
            dans s(K - K), soit (1-s)d = s*w(u) avec w(u) la largeur du
            polygone dans la direction de l'arête :  s* = min d/(d + w(u)).
            Redonne 1/2 (n=3,4), 1/phi^2 (n=5), 1/3 (n=6).
  s_aire    n^(-1/2) : en deçà, log n / log(1/s) < 2, donc aire nulle. C'est
            garanti, la dimension de similitude étant toujours un majorant.
  s_centre  le centre du polygone est couvert : 1/2 si n est pair,
            1/(1 + cos(pi/n)) si n est impair (2/3 pour le triangle).

En dessous de s*, poussière totalement discontinue de dimension
log n / log(1/s) ; à s*, le cas jointif (Sierpinski pour n = 3) ; au-dessus,
recouvrement, puis remplissage du polygone.

Le cadrage est FIXE (disque unité) : sinon l'attracteur paraîtrait garder sa
taille pendant le balayage, alors que c'est justement lui qui grossit.
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
from itertools import islice
from tkinter import ttk, messagebox

W, H = 900, 720
MARGIN = 24
BG = (14, 14, 18)
SKIP = 30
BATCH = 8000
FRAME_MS = 16              # période d'affichage visée (~60 images/s)
PALETTE = ((255, 86, 86), (80, 220, 130), (105, 160, 255), (255, 196, 70),
           (220, 110, 255), (90, 230, 230), (245, 245, 245), (255, 140, 60))
RULES = ("aucune", "norepeat", "noopp", "noadj")


# -------------------------------------------------------------- moteur
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

def plot_into(raster, points, tf, cols):
    s, offx, offy = tf
    h = raster.h
    drawn = 0
    for (x, y), k in points:
        drawn += raster.set(int(s * x + offx), h - 1 - int(s * y + offy),
                            cols[k % len(cols)])
    return drawn

# ------------------------------------------------------ seuils du n-gone
def touch_ratio(verts):
    """Rapport au-dessus duquel deux copies se recouvrent (cf. en-tête)."""
    best = 1.0
    n = len(verts)
    for i in range(n):
        for j in range(i + 1, n):
            dx, dy = verts[j][0] - verts[i][0], verts[j][1] - verts[i][1]
            d = math.hypot(dx, dy)
            ux, uy = dx / d, dy / d
            proj = [v[0] * ux + v[1] * uy for v in verts]
            best = min(best, d / (d + max(proj) - min(proj)))
    return best


def center_ratio(n):
    """Rapport à partir duquel le centre du polygone est couvert."""
    return 0.5 if n % 2 == 0 else 1.0 / (1.0 + math.cos(math.pi / n))


def transient(s, pixels=900):
    """Itérations pour ramener l'écart initial sous le pixel : s^k < 1/pixels.

    Un SKIP fixe conviendrait pour s=1/2 (10 pas) mais pas pour s=0.95, qui
    en demande 133 : le transitoire laisserait une traînée visible vers le
    point de départ.
    """
    if s <= 1e-9:
        return 1
    return max(5, min(600, math.ceil(math.log(1 / pixels) / math.log(s))))


def fixed_transform(w=W, h=H, margin=MARGIN, r=1.05):
    """Cadrage constant sur le disque unité : comparable d'un s à l'autre."""
    sc = min((w - 2 * margin) / (2 * r), (h - 2 * margin) / (2 * r))
    return sc, w * 0.5, h * 0.5          # l'origine tombe au centre du cadre


# ---------------------------------------------------------------------- GUI
class App(ttk.Frame):
    def __init__(self, master):
        super().__init__(master, padding=8)
        self.grid(sticky="nsew")
        master.columnconfigure(0, weight=1)
        master.rowconfigure(0, weight=1)

        self.n_var = tk.IntVar(value=3)
        self.s_var = tk.DoubleVar(value=0.5)
        self.rule_var = tk.StringVar(value="aucune")
        self.pts_var = tk.StringVar(value="200000")
        self.batch_var = tk.StringVar(value=str(BATCH))
        self.seed_var = tk.StringVar(value="")
        self.mono = tk.BooleanVar(value=False)
        self.photo = self.img_id = self._anim_id = self._gen = None
        self._sweep_id = None
        self._quiet = False              # garde : s modifié par programme
        self._tf = fixed_transform()

        bar = ttk.Frame(self)
        bar.grid(row=0, column=0, sticky="ew", pady=(0, 6))
        ttk.Label(bar, text="sommets").pack(side="left", padx=(0, 4))
        ttk.Spinbox(bar, from_=3, to=12, width=4, wrap=True, state="readonly",
                    textvariable=self.n_var,
                    command=self.draw).pack(side="left")
        ttk.Label(bar, text="règle").pack(side="left", padx=(12, 4))
        cb = ttk.Combobox(bar, textvariable=self.rule_var, values=RULES,
                          state="readonly", width=9)
        cb.pack(side="left")
        cb.bind("<<ComboboxSelected>>", lambda _e: self.draw())
        for label, var, wdt in (("points", self.pts_var, 9),
                                ("pts/frame", self.batch_var, 7),
                                ("seed", self.seed_var, 6)):
            ttk.Label(bar, text=label).pack(side="left", padx=(12, 2))
            e = ttk.Entry(bar, textvariable=var, width=wdt)
            e.pack(side="left")
            e.bind("<Return>", lambda _e: self.draw())
        ttk.Checkbutton(bar, text="mono", variable=self.mono,
                        command=self.draw).pack(side="left", padx=10)

        bar2 = ttk.Frame(self)
        bar2.grid(row=1, column=0, sticky="ew", pady=(0, 6))
        ttk.Label(bar2, text="s =").pack(side="left")
        self.s_lbl = ttk.Label(bar2, text="0.5000", width=7)   # largeur figée
        self.s_lbl.pack(side="left", padx=(2, 6))
        ttk.Scale(bar2, from_=0.02, to=0.98, length=360, variable=self.s_var,
                  command=self.on_slide).pack(side="left")
        for txt, cmd, w in (("Dessiner", self.draw, 9),
                            ("Animer", self.toggle_anim, 9),
                            ("Balayer s", self.toggle_sweep, 10),
                            ("s = s*", self.goto_touch, 8)):
            b = ttk.Button(bar2, text=txt, width=w, command=cmd)
            b.pack(side="left", padx=(6, 0))
            if txt == "Animer":
                self.anim_btn = b
            elif txt == "Balayer s":
                self.sweep_btn = b

        self.info = ttk.Label(self, text="", anchor="w")
        self.info.grid(row=2, column=0, sticky="w", pady=(0, 6))
        self.canvas = tk.Canvas(self, width=W, height=H, bg="#0e0e12",
                                highlightthickness=0)
        self.canvas.grid(row=3, column=0, sticky="nsew")
        self.status = ttk.Label(self, text="", anchor="w")
        self.status.grid(row=4, column=0, sticky="w", pady=(4, 0))
        self.columnconfigure(0, weight=1)
        self.rowconfigure(3, weight=1)

        master.bind("<Left>", lambda _e: self.nudge(-0.005))
        master.bind("<Right>", lambda _e: self.nudge(+0.005))
        master.protocol("WM_DELETE_WINDOW", self._on_close)
        self.after(50, self.draw)

    # -------------------------------------------------------- paramètres
    def _read(self):
        npts = int(float(self.pts_var.get()))
        batch = int(float(self.batch_var.get()))
        if npts <= 0 or batch <= 0:
            raise ValueError("points et pts/frame doivent être > 0.")
        seed = self.seed_var.get().strip() or None
        return npts, batch, seed

    def _params(self):
        n = int(self.n_var.get())
        s = min(0.98, max(0.02, float(self.s_var.get())))
        rule = self.rule_var.get()
        return n, s, (None if rule == "aucune" else rule)

    def _cols(self):
        return ([bytes((235, 235, 235))] * len(PALETTE) if self.mono.get()
                else [bytes(c) for c in PALETTE])

    def _generator(self, npts, rng):
        n, s, rule = self._params()
        return poly_points(poly_vertices(n), s, rule, npts, transient(s), rng)

    def _describe(self):
        n, s, _rule = self._params()
        st, sc = touch_ratio(poly_vertices(n)), center_ratio(n)
        sa = n ** -0.5
        dim = math.log(n) / math.log(1 / s)
        if abs(s - st) <= 5e-4:
            regime, dtxt = "contact exact, cas jointif", f"dim = {dim:.4f}"
        elif s < st:
            regime, dtxt = "copies disjointes, poussière", f"dim = {dim:.4f}"
        elif s < sa:
            regime, dtxt = "recouvrement, aire nulle", f"dim <= {dim:.4f}"
        elif s < sc:
            regime = "recouvrement, trous persistants"
            dtxt = f"dim <= min(2, {dim:.3f}) = 2"
        else:
            regime = "centre couvert, remplissage"
            dtxt = f"dim <= min(2, {dim:.3f}) = 2"
        return (f"s* = {st:.4f}   s_aire = {sa:.4f}   s_centre = {sc:.4f}"
                f"   |   {regime}   |   {dtxt}   |   {transient(s)} pas jetés")

    # ------------------------------------------------------- le curseur s
    def on_slide(self, _v):
        """Aperçu léger pendant le glissement ; rendu complet au relâchement
        ou par « Dessiner »."""
        if self._quiet:
            return
        self.s_lbl.config(text=f"{float(self.s_var.get()):.4f}")
        if self._anim_id is None and self._sweep_id is None:
            self.draw(points=25000, light=True)

    def nudge(self, ds):
        self.s_var.set(min(0.98, max(0.02, self.s_var.get() + ds)))
        self.on_slide(None)

    def goto_touch(self):
        self.s_var.set(touch_ratio(poly_vertices(int(self.n_var.get()))))
        self.draw()

    # ------------------------------------------------------------- rendu
    def draw(self, points=None, light=False):
        if not light:
            self.stop_all()
        try:
            npts, _batch, seed = self._read()
        except ValueError as exc:
            messagebox.showerror("Paramètres invalides", str(exc))
            return
        npts = points or npts
        self.s_lbl.config(text=f"{float(self.s_var.get()):.4f}")
        self.info.config(text=self._describe())
        t0 = time.perf_counter()
        raster = Raster()
        gen = self._generator(npts, random.Random(seed))
        drawn = plot_into(raster, gen, self._tf, self._cols())
        self._show(raster.png())
        self.status.config(text=f"{drawn}/{npts} points dans le cadre  |  "
                                f"{(time.perf_counter() - t0) * 1000:.0f} ms")

    # --------------------------------------------- animation incrémentale
    def toggle_anim(self):
        if self._anim_id is not None:
            self.stop_all(note=" (arrêté)")
        else:
            self.start_anim()

    def start_anim(self):
        self.stop_all()
        try:
            npts, batch, seed = self._read()
        except ValueError as exc:
            messagebox.showerror("Paramètres invalides", str(exc))
            return
        self.info.config(text=self._describe())
        self._raster = Raster()
        self._pal = self._cols()
        self._gen = self._generator(npts, random.Random(seed))
        self._total, self._done, self._batch = npts, 0, batch
        self._show(self._raster.png())
        self.anim_btn.config(text="Stop")
        self._anim_id = self.after(10, self._anim_step)

    def _anim_step(self):
        self._anim_id = None
        t0 = time.perf_counter()
        chunk = list(islice(self._gen, self._batch))
        self._done += plot_into(self._raster, chunk, self._tf, self._pal)
        self._show(self._raster.png())
        frame_ms = (time.perf_counter() - t0) * 1000
        pct = 100.0 * self._done / max(self._total, 1)
        self.status.config(
            text=f"{self._done}/{self._total} ({pct:.1f} %)  |  "
                 f"{frame_ms:.0f} ms/frame")
        if len(chunk) < self._batch:
            self._gen = None
            self.anim_btn.config(text="Animer")
            return
        # On laisse respirer la boucle Tk : enchaînées toutes les 1 ms, les
        # demandes de redessin arrivent plus vite que l'écran ne rafraîchit.
        self._anim_id = self.after(max(1, int(FRAME_MS - frame_ms)),
                                   self._anim_step)

    # ------------------------------------------------------ balayage de s
    def toggle_sweep(self):
        if self._sweep_id is not None:
            self.stop_all()
        else:
            self.start_sweep()

    def start_sweep(self):
        self.stop_all()
        self._sweep_s = 0.05
        self.sweep_btn.config(text="Stop")
        self._sweep_id = self.after(10, self._sweep_step)

    def _sweep_step(self):
        self._sweep_id = None
        t0 = time.perf_counter()
        self._quiet = True               # ne pas déclencher l'aperçu
        self.s_var.set(self._sweep_s)
        self._quiet = False
        try:
            batch = int(float(self.batch_var.get()))
        except ValueError:
            batch = BATCH
        self.draw(points=max(batch, 20000), light=True)
        self._sweep_s += 0.01
        if self._sweep_s > 0.95:
            self.sweep_btn.config(text="Balayer s")
            return
        frame_ms = (time.perf_counter() - t0) * 1000
        self._sweep_id = self.after(max(1, int(FRAME_MS - frame_ms)),
                                    self._sweep_step)

    @staticmethod
    def _b64(png):
        return base64.b64encode(png).decode("ascii")

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

    # --------------------------------------------------------- affichage
    def stop_all(self, note=""):
        stopped = False
        for attr, btn, txt in (("_anim_id", "anim_btn", "Animer"),
                               ("_sweep_id", "sweep_btn", "Balayer s")):
            if getattr(self, attr) is not None:
                self.after_cancel(getattr(self, attr))
                setattr(self, attr, None)
                getattr(self, btn).config(text=txt)
                stopped = True
        self._gen = None
        if stopped and note:
            self.status.config(text=self.status.cget("text") + note)

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

    def _on_close(self):
        self.stop_all()
        self.master.destroy()


def main():
    root = tk.Tk()
    root.title("Jeu du chaos - polygone paramétrique")
    App(root)
    root.mainloop()


if __name__ == "__main__":
    main()

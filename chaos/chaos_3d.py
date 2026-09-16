#!/usr/bin/env python3
"""Pyramide de Sierpinski (tétraèdre) par jeu du chaos, en rotation lente.

Script indépendant (stdlib seule), comme les autres fichiers du dossier : le
raster scanline-PNG est la copie conforme de celui de chaos_ifs.py.

Le jeu du chaos passe en dimension 3 sans rien changer : on tire un sommet au
hasard parmi les quatre du tétraèdre régulier et on va au milieu.

    f_k(P) = (P + V_k) / 2,   k = 0..3

Quatre similitudes de rapport 1/2, jointives (elles se touchent aux milieux
des arêtes), donc l'équation de Moran donne

    4 * (1/2)^D = 1   =>   D = log 4 / log 2 = 2

exactement : la pyramide de Sierpinski est un fractal de dimension entière.
Elle a un volume nul mais l'aire de ses faces ne décroît pas -- chaque étape
remplace un tétraèdre par quatre tétraèdres d'arête moitié, soit la même aire
totale.

Sommets, tétraèdre régulier de rayon circonscrit 1, pointe en haut :

    V_0 = (0, 1, 0)
    V_k = (r cos(pi/2 + 2pi k/3), -1/3, r sin(pi/2 + 2pi k/3)),  r = sqrt(8)/3

Rendu : les points sont semés par paquets pendant que la pyramide tourne --
on voit la forme apparaître, comme dans l'animation de référence -- puis
chaque image ne fait plus que reprojeter le nuage complet.

Rotation d'azimut autour de l'axe vertical, puis inclinaison de la caméra
autour de l'axe horizontal ; projection orthographique, à échelle fixe (le
nuage tient dans la sphère unité) pour que l'objet ne respire pas pendant la
rotation.

    x' = x cos(a) + z sin(a)          a : azimut
    z' = z cos(a) - x sin(a)
    px = x'
    py = y cos(e) - z' sin(e)         e : élévation de la caméra
    profondeur = y sin(e) + z' cos(e)

La profondeur sert deux fois : quantifiée sur 256 niveaux elle alimente un
tampon de profondeur (les points proches masquent les lointains), et ses 4
bits de poids fort choisissent une nuance parmi 16 (les points lointains sont
assombris). L'angle avance avec le temps réel, pas avec le compteur d'images,
pour que la vitesse ne dépende pas de la charge.
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
FRAME_MS = 16              # période d'affichage visée (~60 images/s)
NIVEAUX = 16               # nuances de profondeur par sommet
POINTS_MAX = 1500          # taille maximale du nuage
SEMIS = 20                 # points semés par seconde
TAILLE = 4                 # côté d'un point, en pixels
PALETTE = ((255, 86, 86), (80, 220, 130), (105, 160, 255), (255, 196, 70))
MONO = (235, 235, 235)


# ------------------------------------------------------------- géométrie 3D
def tetra_vertices():
    """Tétraèdre régulier de rayon circonscrit 1, un sommet vers le haut."""
    r = math.sqrt(8) / 3
    base = [(r * math.cos(math.pi / 2 + 2 * math.pi * k / 3), -1 / 3,
             r * math.sin(math.pi / 2 + 2 * math.pi * k / 3))
            for k in range(3)]
    return [(0.0, 1.0, 0.0)] + base


def sierpinski_points(n, rng, skip=SKIP):
    """Génère n points (x, y, z, k) sur la pyramide de Sierpinski.

    k est l'indice du dernier sommet tiré : il donne la couleur, donc chaque
    teinte dessine l'une des quatre copies de rapport 1/2. Générateur, et non
    liste, pour que l'animation puisse remplir le nuage par paquets pendant
    que la pyramide tourne.
    """
    verts = tetra_vertices()
    x, y, z = 0.0, 0.0, 0.0
    randrange = rng.randrange
    for i in range(n + skip):
        k = randrange(4)
        vx, vy, vz = verts[k]
        x, y, z = (x + vx) * 0.5, (y + vy) * 0.5, (z + vz) * 0.5
        if i >= skip:
            yield (x, y, z, k)


def sierpinski_cloud(n, rng, skip=SKIP):
    """Le nuage complet, d'un coup."""
    return list(sierpinski_points(n, rng, skip))


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


# ----------------------------------------------------------------- nuances
def shade_table(mono=False, taille=TAILLE, niveaux=NIVEAUX):
    """Pour chaque sommet, les nuances de la plus lointaine (sombre) à la plus
    proche (pleine intensité).

    Chaque nuance est déjà répétée sur la largeur d'un point : le rendu pose
    une ligne du carré en une seule affectation de tranche. Avec un nuage de
    quelques centaines de points, un pixel isolé serait invisible.
    """
    couleurs = [MONO] * 4 if mono else PALETTE
    return [[bytes(int(v * (0.30 + 0.70 * l / (niveaux - 1))) for v in c)
             * taille for l in range(niveaux)] for c in couleurs]


def render(raster, zbuf, pts, azim, elev, scale, ombrage=True,
           occlusion=True, taille=TAILLE):
    """Projette le nuage dans le raster ; retourne le nombre de points posés.

    pts : liste de (x, y, z, nuances), nuances étant la table du sommet tiré,
    déjà répétée sur la largeur d'un point. La boucle écrit directement dans
    raster.raw : un appel de méthode par point (Raster.set) coûterait plus
    cher que toute l'arithmétique.

    Le test de profondeur porte sur le pixel central du carré ; deux points
    qui se chevauchent partiellement peuvent donc empiéter l'un sur l'autre,
    ce qui ne se voit pas à ces densités.
    """
    ca, sa = math.cos(elev), math.sin(elev)
    cz, sz = math.cos(azim), math.sin(azim)
    w, h, stride, raw = raster.w, raster.h, raster.stride, raster.raw
    ox, oy = w * 0.5, h * 0.5
    cxs, sxs = cz * scale, sz * scale
    demi, large = taille // 2, 3 * taille
    bx, by = w - taille, h - taille
    posés = 0
    for x, y, z, nuances in pts:
        zp = cz * z - sz * x                      # profondeur après azimut
        px = int(cxs * x + sxs * z + ox) - demi
        if px < 0 or px >= bx:
            continue
        py = int(oy - (ca * y - sa * zp) * scale) - demi
        if py < 0 or py >= by:
            continue
        d = int((sa * y + ca * zp + 1.0) * 127.0) + 1      # 1..255, 0 = vide
        if occlusion:
            j = (py + demi) * w + px + demi
            if d <= zbuf[j]:
                continue
            zbuf[j] = d
        col = nuances[d >> 4] if ombrage else nuances[-1]
        i = py * stride + 1 + 3 * px
        for _ in range(taille):
            raw[i:i + large] = col
            i += stride
        posés += 1
    return posés


# ---------------------------------------------------------------------- GUI
class App(ttk.Frame):
    def __init__(self, master):
        super().__init__(master, padding=8)
        self.grid(sticky="nsew")
        master.columnconfigure(0, weight=1)
        master.rowconfigure(0, weight=1)

        self.pts_var = tk.StringVar(value=str(POINTS_MAX))
        self.semis_var = tk.StringVar(value=str(SEMIS))   # points par seconde
        self.taille_var = tk.StringVar(value=str(TAILLE))
        self.vit_var = tk.StringVar(value="15")       # degrés par seconde
        self.elev_var = tk.StringVar(value="20")      # degrés
        self.seed_var = tk.StringVar(value="")
        self.mono = tk.BooleanVar(value=False)
        self.ombrage = tk.BooleanVar(value=True)
        self.occlusion = tk.BooleanVar(value=True)

        self.azim = 0.0
        self.photo = self.img_id = self._anim_id = None
        self._cloud = []
        self._pts = []
        self._gen = None                  # remplissage en cours si non None
        self._total = 0
        self._reliquat = 0.0              # points dus, fraction reportée
        self._table = shade_table()
        self._drag = None
        self._fps = 0.0
        self.scale = min(W, H) * 0.5 - MARGIN
        self.raster = Raster()
        self._fond = bytes(self.raster.raw)        # fond, pour effacer
        self.zbuf = bytearray(W * H)
        self._zvide = bytes(self.zbuf)

        bar = ttk.Frame(self)
        bar.grid(row=0, column=0, sticky="ew", pady=(0, 6))
        for label, var, wdt in ((f"points (≤ {POINTS_MAX})", self.pts_var, 6),
                                ("pts/s", self.semis_var, 5),
                                ("taille", self.taille_var, 4),
                                ("°/s", self.vit_var, 5),
                                ("élévation", self.elev_var, 5),
                                ("seed", self.seed_var, 6)):
            ttk.Label(bar, text=label).pack(side="left", padx=(0, 2))
            e = ttk.Entry(bar, textvariable=var, width=wdt)
            e.pack(side="left", padx=(0, 10))
            e.bind("<Return>", lambda _e: self.rebuild())
        for txt, var in (("mono", self.mono), ("ombrage", self.ombrage),
                         ("occlusion", self.occlusion)):
            ttk.Checkbutton(bar, text=txt, variable=var,
                            command=self.refresh).pack(side="left", padx=4)

        bar2 = ttk.Frame(self)
        bar2.grid(row=1, column=0, sticky="ew", pady=(0, 6))
        # width figée : sinon "Animer" -> "Stop" retaille la barre d'outils.
        self.anim_btn = ttk.Button(bar2, text="Animer", width=9,
                                   command=self.toggle_anim)
        self.anim_btn.pack(side="left", padx=(0, 6))
        self.spin_btn = ttk.Button(bar2, text="Tourner", width=9,
                                   command=self.toggle_spin)
        self.spin_btn.pack(side="left", padx=(0, 6))
        for txt, cmd in (("Image fixe", self.refresh),
                         ("Nuage complet", self.rebuild)):
            ttk.Button(bar2, text=txt, width=14,
                       command=cmd).pack(side="left", padx=(0, 6))
        ttk.Label(bar2, text="glisser pour tourner à la main, "
                            "flèches pour ajuster").pack(side="left", padx=10)

        self.info = ttk.Label(self, text="", anchor="w")
        self.info.grid(row=2, column=0, sticky="w", pady=(0, 6))
        self.canvas = tk.Canvas(self, width=W, height=H, bg="#0e0e12",
                                highlightthickness=0)
        self.canvas.grid(row=3, column=0, sticky="nsew")
        self.status = ttk.Label(self, text="", anchor="w")
        self.status.grid(row=4, column=0, sticky="w", pady=(4, 0))
        self.columnconfigure(0, weight=1)
        self.rowconfigure(3, weight=1)

        self.canvas.bind("<ButtonPress-1>", self._drag_start)
        self.canvas.bind("<B1-Motion>", self._drag_move)
        master.bind("<Left>", lambda _e: self.turn(-3))
        master.bind("<Right>", lambda _e: self.turn(+3))
        master.protocol("WM_DELETE_WINDOW", self._on_close)
        self.after(50, self.animate)

    # -------------------------------------------------------- paramètres
    def _read(self):
        """Le nombre de points est plafonné à POINTS_MAX, et le champ est
        corrigé pour que l'affichage ne mente pas sur ce qui est tracé."""
        n = int(float(self.pts_var.get()))
        semis = float(self.semis_var.get().replace(",", "."))
        taille = int(float(self.taille_var.get()))
        if n <= 0 or semis <= 0 or taille <= 0:
            raise ValueError("points, pts/s et taille doivent être > 0.")
        if n > POINTS_MAX:
            n = POINTS_MAX
            self.pts_var.set(str(n))
        taille = min(taille, 20)
        vitesse = math.radians(float(self.vit_var.get().replace(",", ".")))
        elev = math.radians(float(self.elev_var.get().replace(",", ".")))
        seed = self.seed_var.get().strip() or None
        return n, semis, taille, vitesse, elev, seed

    def rebuild(self):
        """Recalcule le nuage : c'est la seule étape coûteuse, les images ne
        font ensuite que le reprojeter."""
        tournait = self._anim_id is not None
        self.stop_spin()
        try:
            n, _s, _t, _v, _e, seed = self._read()
        except ValueError as exc:
            messagebox.showerror("Paramètres invalides", str(exc))
            return
        self.status.config(text="calcul du nuage...")
        self.update_idletasks()
        t0 = time.perf_counter()
        self._cloud = sierpinski_cloud(n, random.Random(seed))
        self._gen_ms = (time.perf_counter() - t0) * 1000
        self._prepare()
        self.refresh()
        if tournait:
            self.start_spin()

    def _prepare(self):
        """Fige la table de nuances dans le nuage : une indirection de moins
        par point et par image."""
        try:
            taille = min(int(float(self.taille_var.get())), 20)
        except ValueError:
            taille = TAILLE
        table = shade_table(self.mono.get(), taille)
        self._table = table
        self._pts = [(x, y, z, table[k]) for x, y, z, k in self._cloud]

    # ------------------------------------------------------------- rendu
    def refresh(self):
        if not self._cloud:
            return
        self._prepare()
        self.frame()

    def frame(self):
        try:
            _n, _s, taille, _v, elev, _se = self._read()
        except ValueError:
            taille, elev = TAILLE, math.radians(20)
        t0 = time.perf_counter()
        self.raster.raw[:] = self._fond
        self.zbuf[:] = self._zvide
        posés = render(self.raster, self.zbuf, self._pts, self.azim, elev,
                       self.scale, self.ombrage.get(), self.occlusion.get(),
                       taille)
        self._show(self.raster.png())
        ms = (time.perf_counter() - t0) * 1000
        deg = math.degrees(self.azim) % 360
        self.info.config(
            text=f"pyramide de Sierpinski : 4 copies de rapport 1/2, "
                 f"dim = log4/log2 = 2   |   {len(self._pts)} points   |   "
                 f"azimut {deg:5.1f}°")
        avance = (f"{len(self._pts)}/{self._total} points semés  |  "
                  if self._gen is not None else "")
        self.status.config(
            text=f"{avance}{posés} points visibles  |  {ms:.0f} ms/image"
                 f"  |  {self._fps:4.1f} images/s")
        return ms

    # --------------------------------------------------------- rotation
    def toggle_anim(self):
        if self._anim_id is not None and self._gen is not None:
            self.stop_spin()
        else:
            self.animate()

    def animate(self):
        """Repart d'un nuage vide : les points sont semés par paquets pendant
        que la pyramide tourne."""
        self.stop_spin()
        try:
            n, _s, taille, _v, _e, seed = self._read()
        except ValueError as exc:
            messagebox.showerror("Paramètres invalides", str(exc))
            return
        self._table = shade_table(self.mono.get(), taille)
        self._cloud, self._pts = [], []
        self._gen = sierpinski_points(n, random.Random(seed))
        self._total = n
        self._reliquat = 0.0
        self.azim = 0.0
        self._last = time.perf_counter()
        self.anim_btn.config(text="Stop")
        self.spin_btn.config(text="Tourner")
        self._anim_id = self.after(10, self._spin)

    def toggle_spin(self):
        if self._anim_id is not None:
            self.stop_spin()
        else:
            self.start_spin()

    def start_spin(self):
        """Rotation seule, sur le nuage tel qu'il est."""
        if not self._cloud:
            return
        self._last = time.perf_counter()
        self.spin_btn.config(text="Stop")
        self._anim_id = self.after(10, self._spin)

    def stop_spin(self):
        if self._anim_id is not None:
            self.after_cancel(self._anim_id)
            self._anim_id = None
        self._gen = None
        self.anim_btn.config(text="Animer")
        self.spin_btn.config(text="Tourner")

    def _spin(self):
        self._anim_id = None
        try:
            _n, semis, _t, vitesse, _e, _s = self._read()
        except ValueError:
            semis, vitesse = SEMIS, math.radians(15)
        maintenant = time.perf_counter()
        dt = maintenant - self._last
        self._last = maintenant
        # L'angle suit le temps réel : la vitesse de rotation ne dépend donc
        # pas de la charge ni du nombre de points, qui varie du simple au
        # décuple entre le début et la fin du remplissage.
        self.azim += vitesse * dt
        self._fps = 1.0 / dt if dt > 0 else 0.0
        if self._gen is not None:
            # Semis indexé sur le temps : le reliquat fractionnaire est
            # reporté d'une image à l'autre, donc 20 pts/s restent 20 pts/s
            # quelle que soit la cadence d'affichage.
            self._reliquat += semis * dt
            paquet = int(self._reliquat)
            self._reliquat -= paquet
            if paquet:
                self._seed_batch(paquet)
        ms = self.frame()
        self._anim_id = self.after(max(1, int(FRAME_MS - ms)), self._spin)

    def _seed_batch(self, batch):
        """Ajoute un paquet de points au nuage, sans rien recalculer du
        reste : le tirage reprend exactement où il s'était arrêté."""
        table = self._table
        cloud, pts = self._cloud, self._pts
        n = 0
        for x, y, z, k in islice(self._gen, batch):
            cloud.append((x, y, z, k))
            pts.append((x, y, z, table[k]))
            n += 1
        if n < batch:                      # générateur épuisé
            self._gen = None
            self.anim_btn.config(text="Animer")
            self.spin_btn.config(text="Stop")   # la rotation, elle, continue

    def turn(self, degres):
        self.azim += math.radians(degres)
        if self._anim_id is None:
            self.frame()

    def _drag_start(self, ev):
        self._drag = (ev.x, ev.y)

    def _drag_move(self, ev):
        if self._drag is None:
            return
        dx = ev.x - self._drag[0]
        dy = ev.y - self._drag[1]
        self._drag = (ev.x, ev.y)
        self.azim += dx * 0.01
        try:
            elev = float(self.elev_var.get().replace(",", ".")) + dy * 0.5
        except ValueError:
            elev = 20.0
        self.elev_var.set(f"{max(-89.0, min(89.0, elev)):.0f}")
        if self._anim_id is None:
            self.frame()

    # -------------------------------------------------------- affichage
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
        self.stop_spin()
        self.master.destroy()


def main():
    root = tk.Tk()
    root.title("Jeu du chaos - pyramide de Sierpinski")
    App(root)
    root.mainloop()


if __name__ == "__main__":
    main()

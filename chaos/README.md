# Jeu du chaos — systèmes de fonctions itérées

Quatre programmes Python indépendants (bibliothèque standard seule, interface
tkinter), qui tracent des fractales par *jeu du chaos* : on itère au hasard
des contractions du plan et on marque les points visités. Chaque fichier
tourne seul, sans import croisé — le moteur partagé est dupliqué, c'est
assumé.

| fichier | contenu |
| --- | --- |
| `chaos_triangle.py` | le cas d'école : triangle ABC quelconque, saisi à la main |
| `chaos_ifs.py` | 13 exemples — polygones avec règles de transition, et IFS affines |
| `chaos_polygon.py` | le jeu des sommets seul : `n`, `s` et règle au curseur |
| `chaos_3d.py` | la pyramide de Sierpinski en 3D, en rotation lente |

```sh
python3 chaos_ifs.py        # menu déroulant « fractale »
python3 chaos_triangle.py   # sommets A, B, C éditables
python3 chaos_polygon.py    # n-gone : n, s et règle réglables
python3 chaos_3d.py         # tétraèdre en rotation, glisser pour tourner
```

Commandes communes : `N` (nombre de points), `pts/frame` (vitesse de
l'animation), `seed` (germe, vide = aléatoire), `mono`, **Dessiner** (rendu
en un coup) et **Animer** (rendu incrémental à ~60 images/s).

---

## 1. Ce que calcule le programme

### 1.1 Système de fonctions itérées

Soit $f_1,\dots,f_m$ des contractions du plan, de rapports
$s_1,\dots,s_m < 1$. L'opérateur de Hutchinson agit sur les compacts non
vides :

$$
F(K) = f_1(K)\cup f_2(K)\cup\dots\cup f_m(K)
$$

$F$ est contractante pour la distance de Hausdorff. Le théorème du point fixe
de Banach donne donc un unique compact $A$ tel que

$$
A = f_1(A)\cup\dots\cup f_m(A)
$$

et $F^{n}(K)\to A$ pour **n'importe quel** compact de départ $K$. C'est
l'*attracteur* de l'IFS : la fractale. Il ne dépend que des cartes $f_i$.

### 1.2 Le jeu du chaos

Plutôt que d'itérer $F$ sur des ensembles (coûteux), on suit une seule orbite
aléatoire :

$$
x_{n+1} = f_{k_n}(x_n), \qquad k_n \sim (p_1,\dots,p_m), \quad p_i > 0
$$

Presque sûrement, l'adhérence de $\lbrace x_n : n\ge N\rbrace$ est exactement
$A$, et la mesure empirique des points converge vers l'unique mesure
invariante

$$
\mu = \sum_{i=1}^{m} p_i\,\bigl(\mu\circ f_i^{-1}\bigr)
\qquad\text{(théorème ergodique d'Elton)}
$$

Conséquence pratique, et c'est tout l'intérêt du paramètre `probs` :
**les probabilités ne changent pas le dessin** (le support $A$), seulement la
densité des points, donc la vitesse à laquelle l'image se remplit.

Le transitoire (`SKIP = 30` points jetés) sert à oublier le point de départ :
la distance à $A$ est multipliée à chaque pas par le rapport de la carte
tirée. Pour un rapport moyen $\exp\bigl(\sum_i p_i\ln s_i\bigr)$ de l'ordre
de $0{,}73$ — le pire cas du catalogue, la fougère — il reste
$0{,}73^{30}\approx 8\cdot 10^{-5}$ de l'écart initial, très en dessous du
pixel.

### 1.3 Dimension

Si les copies $f_i(A)$ sont « juste jointives » (condition de l'ouvert, *OSC* :
il existe un ouvert $U$ avec $f_i(U)\subset U$ deux à deux disjoints), la
dimension de Hausdorff est donnée par l'équation de Moran–Hutchinson :

$$
\sum_{i=1}^{m} s_i^{D} = 1
$$

Pour $m$ similitudes de **même** rapport $s$, cela se résout tout de suite :

$$
m\,s^{D} = 1
\quad\Longrightarrow\quad
D = \frac{\log m}{\log(1/s)}
$$

C'est la formule qui produit tous les $\log a/\log b$ du catalogue ci-dessous.
Quand les copies se recouvrent (dragon, courbe de Lévy, fougère), l'équation
ne donne qu'une borne supérieure et il faut un argument spécifique.

---

## 2. Les deux familles de générateurs

### 2.1 Jeu des sommets — `poly_points`

Sommets d'un `n`-gone régulier inscrit dans le cercle unité, premier sommet en
haut (`poly_vertices`) :

$$
V_k = \Bigl(\cos\bigl(\tfrac{\pi}{2} + \tfrac{2\pi k}{n}\bigr),\;
\sin\bigl(\tfrac{\pi}{2} + \tfrac{2\pi k}{n}\bigr)\Bigr),
\qquad k = 0,\dots,n-1
$$

et, pour un rapport de contraction $s$ :

$$
f_k(P) = V_k + s\,(P - V_k)
$$

> **Attention à la convention.** L'autre écriture courante,
> $P' = P + r (V - P)$, contracte d'un facteur $1 - r$, pas $r$.
> Le code utilise partout le rapport de contraction $s$ lui-même ;
> le jeu classique du triangle, c'est $s = 1/2$ (milieu).

`chaos_polygon.py` rend ce `s` réglable et affiche, pour le `n`-gone courant,
les trois seuils qui découpent les régimes : $s^{*}$ (contact des copies, où
Moran s'applique), $n^{-1/2}$ (au-delà, la dimension de similitude dépasse 2)
et le seuil de couverture du centre. Son bouton **Balayer s** parcourt
l'intervalle et montre le passage poussière → jointif → recouvrement →
polygone plein.

### 2.2 Règles de transition — chaînes de Markov sur les sommets

Le paramètre `rule` interdit certains enchaînements de sommets. Les adresses
admissibles forment alors un [sous-décalage de type
fini](https://en.wikipedia.org/wiki/Subshift_of_finite_type). La règle étant
invariante par rotation, sa matrice de transition est *circulante* : elle
autorise un ensemble d'écarts $\mathcal{D}\subset\mathbb{Z}/n\mathbb{Z}$
entre sommets consécutifs. Toutes ses lignes ont la même somme
$\lvert\mathcal{D}\rvert$, donc sa valeur propre de Perron vaut
$\lvert\mathcal{D}\rvert$, le nombre de mots admissibles de longueur $n$
croît comme $\lvert\mathcal{D}\rvert^{n}$, et (copies jointives) :

$$
D = \frac{\log\lvert\mathcal{D}\rvert}{\log(1/s)}
$$

| `rule` | écarts autorisés | $\lvert\mathcal{D}\rvert$ |
| --- | --- | --- |
| `None` | tous | $n$ |
| `'norepeat'` | $\ne 0$ — jamais deux fois le même sommet | $n-1$ |
| `'noopp'` | $\ne n/2$ — jamais le sommet opposé | $n-1$ |
| `'noadj'` | $\notin\lbrace 1, n-1\rbrace$ — jamais un sommet voisin | $n-2$ |

Cas limite instructif (aucun preset ne l'utilise) : `'noadj'` sur le carré ne
laisse que les écarts $\lbrace 0,2\rbrace$, donc l'indice reste dans une paire
de sommets opposés et l'attracteur s'effondre sur **une diagonale**, de
dimension
$\log 2/\log 2 = 1$. Les points tracés sont alors exactement alignés.

### 2.3 IFS affine général — `ifs_points`

Chaque carte est un sextuplet `(a, b, c, d, e, f)` :

$$
\begin{pmatrix} x' \\ y' \end{pmatrix}
= \underbrace{\begin{pmatrix} a & b \\ c & d \end{pmatrix}}_{M}
  \begin{pmatrix} x \\ y \end{pmatrix}
+ \underbrace{\begin{pmatrix} e \\ f \end{pmatrix}}_{t}
\qquad\text{soit}\qquad f(P) = MP + t
$$

Une similitude de rapport $s$ et d'angle $\theta$ s'écrit $M = s R(\theta)$ :

$$
M = s\begin{pmatrix}
\cos\theta & -\sin\theta \\
\sin\theta & \cos\theta
\end{pmatrix},
\qquad \det M = s^{2}
$$

C'est cette lecture qui permet de retrouver, plus bas, « rotation de 60°,
rapport 1/3 » derrière les coefficients bruts de la courbe de Koch.

### 2.4 Probabilités — `det_probs`

À défaut de probabilités explicites, le code applique l'heuristique de
Barnsley $p_i\propto\lvert\det M_i\rvert$ : le temps de calcul est réparti
proportionnellement
à l'aire couverte par chaque copie, ce qui remplit l'image de façon homogène.
Le plancher `floor = 0.01` protège les cartes dégénérées (`det = 0`, comme la
tige de la fougère) qui, sinon, ne seraient jamais tirées.

Rappel du §1.2 : ce choix **ne change pas l'attracteur**, seulement la mesure
invariante — donc la vitesse de remplissage, pas la forme.

### 2.5 Les couleurs

Chaque point est colorié selon l'indice `k` de la dernière carte appliquée.
L'image colorée montre donc directement la décomposition de niveau 1,
$A = f_1(A)\cup\dots\cup f_m(A)$ : une couleur par copie. La case `mono`
désactive ce codage.

---

## 3. Catalogue des exemples

Tous les rapports `s` ci-dessous sont des rapports de contraction, et toutes
les dimensions sont des dimensions de Hausdorff (= box-counting ici).

### 3.1 Sierpiński — triangle, $s = 1/2$

$$
n = 3, \qquad f_k(P) = \tfrac{1}{2}\,(P + V_k), \qquad k = 0,1,2
$$

$$
3\left(\tfrac{1}{2}\right)^{D} = 1
\quad\Longrightarrow\quad
D = \frac{\log 3}{\log 2} \approx 1{,}5850
$$

Le jeu du chaos historique : les trois demi-copies du triangle se touchent par
les milieux des côtés (OSC vérifiée), le trou central est ce qu'aucune copie
n'atteint.

[Wikipédia (fr)](https://fr.wikipedia.org/wiki/Triangle_de_Sierpi%C5%84ski) ·
[MathWorld](https://mathworld.wolfram.com/SierpinskiSieve.html)

### 3.2 Carré $s = 1/2$ — le contre-exemple

$$
n = 4, \qquad s = \tfrac{1}{2}, \qquad
4\left(\tfrac{1}{2}\right)^{D} = 1
\quad\Longrightarrow\quad D = 2
$$

Les quatre demi-copies **pavent** le carré : l'attracteur est le carré plein,
et les adresses aléatoires ne sont rien d'autre que les chiffres d'un
quadtree tirés uniformément. Aucune structure n'apparaît.

C'est le témoin à garder en tête : le hasard ne fabrique pas de fractale,
c'est le *déficit* de recouvrement qui la fabrique. Pour obtenir une structure
il faut soit contracter davantage (§3.4), soit contraindre les enchaînements
(§3.3).

[Jeu du chaos (Wikipédia, en)](https://en.wikipedia.org/wiki/Chaos_game) ·
[MathWorld](https://mathworld.wolfram.com/ChaosGame.html)

### 3.3 Carré $s = 1/2$, sans répétition / sans opposé

Deux restrictions sur le même carré dégénéré du §3.2.

$$
\texttt{norepeat} : k_{i+1}\ne k_i
\qquad\qquad
\texttt{noopp} : k_{i+1}\ne k_i + 2 \pmod 4
$$

Dans les deux cas l'adresse est une suite de chiffres du quadtree soumise à
une interdiction, donc le nombre de cellules de côté $2^{-n}$ rencontrées est
$4\cdot 3^{n-1}$ :

$$
D = \lim_{n\to\infty}
\frac{\log\bigl(4\cdot 3^{\,n-1}\bigr)}{\log 2^{\,n}}
= \frac{\log 3}{\log 2} \approx 1{,}5850
$$

Même dimension, mais **deux ensembles différents** : sur une grille 16×16,
seules 63 cellules sont communes aux deux. C'est l'illustration que la
dimension ne caractérise pas la forme.

[Sous-décalage de type fini](https://en.wikipedia.org/wiki/Subshift_of_finite_type) ·
[Chaos game (variantes avec restriction)](https://en.wikipedia.org/wiki/Chaos_game)

### 3.4 Carré $s = 1/3$ — poussière de Cantor

$$
n = 4, \qquad s = \tfrac{1}{3}, \qquad
4\left(\tfrac{1}{3}\right)^{D} = 1
\quad\Longrightarrow\quad
D = \frac{\log 4}{\log 3} \approx 1{,}2619
$$

Cette fois les quatre copies sont **disjointes** : il reste un ensemble
totalement discontinu, le produit $C\times C$ de l'ensemble triadique de
Cantor par lui-même (à rotation près, les sommets formant ici un losange).
$D = 2\log 2/\log 3 = \log 4/\log 3$, cohérent.

[Ensemble de Cantor (fr)](https://fr.wikipedia.org/wiki/Ensemble_de_Cantor) ·
[MathWorld — Cantor dust](https://mathworld.wolfram.com/CantorDust.html)

### 3.5 Pentaflake — $s = 1/\varphi^{2}$

$$
n = 5, \qquad
s = \frac{1}{\varphi^{2}} = \frac{3-\sqrt{5}}{2} \approx 0{,}381966,
\qquad \varphi = \frac{1+\sqrt{5}}{2}, \quad \varphi^{2} = \varphi + 1
$$

$$
5\,s^{D} = 1
\quad\Longrightarrow\quad
D = \frac{\log 5}{\log \varphi^{2}} = \frac{\log 5}{2\log \varphi}
\approx 1{,}6723
$$

Le rapport n'est pas arbitraire : $1/\varphi^{2}$ est exactement la valeur pour
laquelle les cinq pentagones fils se touchent sans se recouvrir — la condition
de l'ouvert est saturée, et la formule de Moran s'applique au cas limite. Le
nombre d'or sort de la géométrie du pentagone régulier (rapport
diagonale/côté $= \varphi$).

[N-flake (en)](https://en.wikipedia.org/wiki/N-flake#Pentaflake) ·
[MathWorld](https://mathworld.wolfram.com/Pentaflake.html)

### 3.6 Hexaflake — $s = 1/3$

$$
n = 6, \qquad s = \tfrac{1}{3}, \qquad
6\left(\tfrac{1}{3}\right)^{D} = 1
\quad\Longrightarrow\quad
D = \frac{\log 6}{\log 3} \approx 1{,}6309
$$

Les six copies se touchent exactement, sommet contre sommet : leurs centres
sont à distance $2/3$ et leur rayon circonscrit vaut $1/3$.

Nuance de vocabulaire : l'*hexaflake* de la littérature ajoute une septième
copie au centre, d'où $D = \log 7/\log 3 \approx 1{,}7712$. Ici il n'y a que
les six copies des sommets (parfois appelé hexagone de Sierpiński).

[N-flake (en)](https://en.wikipedia.org/wiki/N-flake)

### 3.7 Tapis de Sierpiński

Grille 3×3 privée de sa case centrale (`_grid_ifs`) :

$$
f_{i,j}(x,y) = \left(\frac{x+i}{3},\ \frac{y+j}{3}\right),
\qquad (i,j)\in\{0,1,2\}^{2}\setminus\{(1,1)\}
$$

$$
8\left(\tfrac{1}{3}\right)^{D} = 1
\quad\Longrightarrow\quad
D = \frac{\log 8}{\log 3} \approx 1{,}8928
$$

Toutes les cartes sont ici des homothéties sans rotation : c'est l'IFS le plus
simple à lire dans le code.

[Wikipédia (fr)](https://fr.wikipedia.org/wiki/Tapis_de_Sierpi%C5%84ski) ·
[MathWorld](https://mathworld.wolfram.com/SierpinskiCarpet.html)

### 3.8 Fractale de Vicsek

Même grille 3×3, mais on garde le centre et les quatre coins :

$$
(i,j)\in\bigl\{(1,1),\,(0,0),\,(2,0),\,(0,2),\,(2,2)\bigr\}
$$

$$
5\left(\tfrac{1}{3}\right)^{D} = 1
\quad\Longrightarrow\quad
D = \frac{\log 5}{\log 3} \approx 1{,}4650
$$

C'est la variante en X (saltire) ; la variante en croix, qui garde les quatre
milieux d'arêtes au lieu des coins, a exactement la même dimension — encore un
cas de deux formes distinctes de même dimension.

[Wikipédia (fr)](https://fr.wikipedia.org/wiki/Fractale_de_Vicsek) ·
[MathWorld — Box fractal](https://mathworld.wolfram.com/BoxFractal.html)

### 3.9 Courbe de Koch

Quatre similitudes de rapport $1/3$, décodées depuis `_koch()` :

$$
\begin{aligned}
f_1 &= \tfrac{1}{3}\,\mathrm{Id}, & t &= (0,\,0) \\
f_2 &= \tfrac{1}{3}\,R(+60^{\circ}), & t &= (1/3,\,0) \\
f_3 &= \tfrac{1}{3}\,R(-60^{\circ}), & t &= (1/2,\,\sqrt{3}/6) \\
f_4 &= \tfrac{1}{3}\,\mathrm{Id}, & t &= (2/3,\,0)
\end{aligned}
$$

$$
4\left(\tfrac{1}{3}\right)^{D} = 1
\quad\Longrightarrow\quad
D = \frac{\log 4}{\log 3} \approx 1{,}2619
$$

L'attracteur est la courbe de Koch joignant $(0,0)$ à $(1,0)$, de sommet
$(1/2,\ \sqrt{3}/6)$ — c'est le $h = \sqrt{3}/6 \approx 0{,}2887$ du code. Le
flocon complet, c'est trois de ces courbes sur les côtés d'un triangle
équilatéral.

Même dimension que la poussière de Cantor du §3.4, pour une raison exacte :
$\log 4/\log 3$ des deux côtés, 4 copies de rapport $1/3$ dans les deux cas.

[Wikipédia (fr)](https://fr.wikipedia.org/wiki/Flocon_de_Koch) ·
[MathWorld](https://mathworld.wolfram.com/KochSnowflake.html)

### 3.10 Dragon de Heighway

Deux similitudes de rapport $1/\sqrt{2}$ :

$$
f_1 = \tfrac{1}{\sqrt{2}}\,R(+45^{\circ}),\quad t = (0,\,0)
\qquad
f_2 = \tfrac{1}{\sqrt{2}}\,R(+135^{\circ}),\quad t = (1,\,0)
$$

ou, en écriture complexe, exactement le dragon classique :

$$
f_1(z) = \frac{1+i}{2}\,z
\qquad
f_2(z) = 1 - \frac{1-i}{2}\,z
$$

La formule de Moran donne $2 (1/\sqrt{2})^{D} = 1 \Longrightarrow D = 2$, et
c'est ici la vraie valeur : le dragon a un **intérieur non vide** (il pave le
plan par translations). L'objet fractal est son bord, de dimension

$$
\dim \partial = 2\log_{2}\lambda \approx 1{,}5236271,
\qquad \lambda^{3} = \lambda^{2} + 2
$$

$$
\lambda = \frac{1 + \sqrt[3]{28 - 3\sqrt{87}} + \sqrt[3]{28 + 3\sqrt{87}}}{3}
\approx 1{,}6956208
$$

[Wikipédia (fr)](https://fr.wikipedia.org/wiki/Courbe_du_dragon) ·
[MathWorld](https://mathworld.wolfram.com/DragonCurve.html)

### 3.11 Courbe C de Lévy

Deux similitudes de rapport $1/\sqrt{2}$, tournées en sens opposés :

$$
f_1 = \tfrac{1}{\sqrt{2}}\,R(-45^{\circ}),\quad t = (0,\,0)
\qquad
f_2 = \tfrac{1}{\sqrt{2}}\,R(+45^{\circ}),\quad t = (1/2,\,-1/2)
$$

$$
f_1(z) = \frac{1-i}{2}\,z
\qquad
f_2(z) = \frac{1-i}{2} + \frac{1+i}{2}\,z
$$

Les deux moitiés se raccordent au point de jonction
$f_1(1,0) = f_2(0,0) = (1/2, -1/2)$, d'où la courbe continue de $(0,0)$ à
$(1,0)$.

Dimension de similitude 2 également, mais cette fois les deux copies **se
recouvrent** : la condition de l'ouvert tombe. La dimension de Hausdorff vaut
tout de même 2 (la courbe contient des ouverts) et c'est son bord qui est
fractal, de dimension $\approx 1{,}9340$.

[Wikipédia (fr)](https://fr.wikipedia.org/wiki/Courbe_de_L%C3%A9vy) ·
[MathWorld](https://mathworld.wolfram.com/LevyFractal.html)

### 3.12 Fougère de Barnsley

Le seul exemple du catalogue qui ne soit pas fait de similitudes : les cartes
comportent du cisaillement, ce qui donne les courbures des frondes.

$$
\begin{aligned}
f_1 &:\ M = \begin{pmatrix} 0 & 0 \\ 0 & 0{,}16 \end{pmatrix},
     & t &= (0,\ 0) \\
f_2 &:\ M = \begin{pmatrix} 0{,}85 & 0{,}04 \\ -0{,}04 & 0{,}85 \end{pmatrix},
     & t &= (0,\ 1{,}6) \\
f_3 &:\ M = \begin{pmatrix} 0{,}2 & -0{,}26 \\ 0{,}23 & 0{,}22 \end{pmatrix},
     & t &= (0,\ 1{,}6) \\
f_4 &:\ M = \begin{pmatrix} -0{,}15 & 0{,}28 \\ 0{,}26 & 0{,}24 \end{pmatrix},
     & t &= (0,\ 0{,}44)
\end{aligned}
$$

| carte | $\det M$ | $p$ | rôle |
| --- | --- | --- | --- |
| $f_1$ | $0$ | $0{,}01$ | la tige |
| $f_2$ | $0{,}7241$ | $0{,}85$ | la fronde entière, décalée |
| $f_3$ | $0{,}1038$ | $0{,}07$ | foliole gauche |
| $f_4$ | $-0{,}1088$ | $0{,}07$ | foliole droite |

Deux particularités :

- $f_1$ est **dégénérée** ($\det = 0$, matrice de rang 1) : elle écrase le
  plan sur le segment vertical $x = 0$. C'est précisément pour elle qu'existe
  le plancher `floor` de `det_probs`.
- Les copies se recouvrent, la formule de Moran ne s'applique pas ; il n'y a
  pas d'expression fermée simple pour la dimension de cet attracteur.

Les probabilités non uniformes sont indispensables **au rendu** : avec
$p_i = 1/4$ partout, l'attracteur serait le même, mais un quart des points
irait dessiner la tige et l'image mettrait très longtemps à se former.
Amusant : l'heuristique automatique $p_i\propto\lvert\det M_i\rvert$ redonne
$(0{,}011 ;\ 0{,}765 ;\ 0{,}110 ;\ 0{,}115)$, très proche des valeurs
réglées à la main par Barnsley.

[Wikipédia (fr)](https://fr.wikipedia.org/wiki/Foug%C3%A8re_de_Barnsley) ·
[MathWorld](https://mathworld.wolfram.com/BarnsleysFern.html)

### 3.13 En trois dimensions — la pyramide de Sierpinski

Le jeu du chaos ne change pas d'un iota en passant dans l'espace : on tire un
sommet parmi les quatre du tétraèdre régulier et on va au milieu.

$$
f_k(P) = \tfrac{1}{2}\,(P + V_k), \qquad k = 0,\dots,3, \qquad P\in\mathbb{R}^{3}
$$

$$
V_0 = (0,\ 1,\ 0), \qquad
V_k = \left(r\cos\theta_k,\ -\tfrac{1}{3},\ r\sin\theta_k\right),
\quad r = \frac{\sqrt{8}}{3}, \quad
\theta_k = \frac{\pi}{2} + \frac{2\pi k}{3}
$$

Les quatre copies se touchent aux milieux des arêtes — condition de l'ouvert
saturée, exactement comme le triangle en dimension 2 — d'où

$$
4\left(\tfrac{1}{2}\right)^{D} = 1
\quad\Longrightarrow\quad
D = \frac{\log 4}{\log 2} = 2
$$

**exactement 2**, une dimension entière pour un objet pourtant fractal. Le
volume est nul, mais l'aire totale des faces ne décroît pas : chaque étape
remplace un tétraèdre par quatre tétraèdres d'arête moitié, donc d'aire
quatre fois moindre — le compte est juste. Vu de face, l'ombre de la pyramide
est un carré plein ; vu d'un sommet, un triangle.

`chaos_3d.py` sème les points un à un **pendant** que la pyramide tourne : la
forme apparaît sous les yeux, comme dans l'animation de référence, puis la
rotation continue sur le nuage complet. Les réglages par défaut sont
volontairement lents — 1500 points au maximum, semés à 20 points par seconde,
soit 75 s de remplissage et un peu plus de trois tours à 15 °/s. À cette
densité un pixel isolé serait invisible : chaque point est un carré de 4 px
de côté, la largeur étant précuite dans la table de nuances pour que le rendu
pose une ligne du carré en une seule affectation de tranche.

Une fois semé, chaque image ne fait plus que reprojeter : rotation d'azimut
autour de l'axe vertical, inclinaison de la caméra, projection orthographique
à échelle fixe — le nuage tenant dans la sphère unité, aucun recadrage n'est
nécessaire et l'objet ne respire pas pendant le tour. La profondeur,
quantifiée sur 256 niveaux, sert à la fois de tampon de profondeur (les points
proches masquent les lointains) et d'assombrissement des points lointains.

Deux quantités suivent le temps réel et non le compteur d'images : l'angle de
rotation et le semis, dont le reliquat fractionnaire est reporté d'une image à
l'autre. Les 20 points par seconde et les 15 degrés par seconde sont donc
tenus quelle que soit la cadence d'affichage.

[Triangle de Sierpiński, analogues en dimension supérieure](https://en.wikipedia.org/wiki/Sierpi%C5%84ski_triangle#Analogues_in_higher_dimensions) ·
[MathWorld — Tetrix](https://mathworld.wolfram.com/Tetrix.html) ·
[l'animation de référence](https://fr.wikipedia.org/wiki/Jeu_du_chaos)

---

## 4. Contrôle numérique des dimensions

Comptage de boîtes sur 400 000 points (pente entre les échelles 1/64 et
1/128 ; Koch mesuré sur des puissances de 3, de 1/729 à 1/2187, la courbe
étant trop fine aux échelles grossières) :

| exemple | attendu | mesuré |
| --- | --- | --- |
| Sierpiński triangle | 1,585 | 1,575 |
| Carré `s=1/2` | 2,000 | 1,962 |
| Carré, sans répétition | 1,585 | 1,555 |
| Carré, sans opposé | 1,585 | 1,569 |
| Carré `s=1/3` | 1,262 | 1,219 |
| Pentaflake | 1,672 | 1,660 |
| Hexaflake | 1,631 | 1,598 |
| Tapis de Sierpiński | 1,893 | 1,875 |
| Vicsek | 1,465 | 1,427 |
| Koch | 1,262 | 1,253 |

L'estimation est systématiquement un peu basse : à échantillonnage fini, les
boîtes les plus fines ne sont pas toutes atteintes. La convergence est lente
(l'erreur décroît comme $1/\log(1/\varepsilon)$), ce qui est le défaut connu
du comptage de boîtes — l'accord est néanmoins net.

---

## 5. Notes d'implémentation

- **Boîte englobante** (`bbox_of`) : un IFS quelconque n'a pas de boîte connue
  a priori, elle est estimée sur 20 000 points avant le tracé. `fit_transform`
  en déduit une transformation affine isotrope (aucune déformation) avec `y`
  inversé, écran oblige.
- **Rendu** : le buffer est stocké directement au format scanline PNG (octet
  de filtre en tête de chaque ligne), si bien que produire l'image se réduit à
  `zlib.compress` plus trois chunks. Pas de dépendance externe.
- **Animation** : le même raster est réutilisé d'une image à l'autre, seuls
  les nouveaux points y sont ajoutés. La mise à jour passe par `put -format
  png` (écriture en place) et non `configure(-data)`, qui vide l'image avant
  de la relire et faisait scintiller l'affichage. La cadence est bornée à
  ~60 images/s ; la vitesse se règle avec `pts/frame`.

---

## 6. Références

- Michael F. Barnsley, *Fractals Everywhere*, Academic Press, 1988 — le jeu du
  chaos, le théorème du collage, la fougère.
- John E. Hutchinson, « Fractals and self-similarity », *Indiana Univ. Math.
  J.* 30 (1981), 713–747 — l'opérateur $F$ et l'unicité de l'attracteur.
- John H. Elton, « An ergodic theorem for iterated maps », *Ergodic Theory
  Dynam. Systems* 7 (1987), 481–488 — pourquoi l'orbite aléatoire dessine
  l'attracteur.
- P. A. P. Moran, « Additive functions of intervals and Hausdorff measure »,
  *Proc. Cambridge Philos. Soc.* 42 (1946), 15–23 — l'équation
  $\sum_i s_i^{D} = 1$.

Articles généraux :
[jeu du chaos](https://fr.wikipedia.org/wiki/Jeu_du_chaos) ·
[systèmes de fonctions itérées](https://fr.wikipedia.org/wiki/Syst%C3%A8me_de_fonctions_it%C3%A9r%C3%A9es) ·
[dimension de Hausdorff](https://fr.wikipedia.org/wiki/Dimension_de_Hausdorff) ·
[condition de l'ouvert](https://en.wikipedia.org/wiki/Open_set_condition) ·
[théorème du collage](https://en.wikipedia.org/wiki/Collage_theorem) ·
[opérateur de Hutchinson](https://en.wikipedia.org/wiki/Hutchinson_operator) ·
[MathWorld — IFS](https://mathworld.wolfram.com/IteratedFunctionSystem.html) ·
[MathWorld — dimension de similitude](https://mathworld.wolfram.com/SimilarityDimension.html)

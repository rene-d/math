"""
Marsh Crossing

https://projecteuler.net/problem=607
"""

from scipy.optimize import minimize
from math import sqrt


v2 = sqrt(2)

# distance entre le point A ou B et le marais
d1 = 50 / v2 - 10 - 10 - 5

# coordonnées du point A dans un repère abscisses=(NW-SE) et ordonnées=(SW-NE)
xa = 0
ya = 0

# coordonnées du point B
xb = 100 / v2
yb = 100 / v2

# coordonnées des intersections des limites des 5 régions du marais
x0 = d1
x1 = x0 + 10
x2 = x1 + 10
x3 = x2 + 10
x4 = x3 + 10
x5 = x4 + 10


# fonction qui donne le temps de trajet en fonction des points (xi, yi) de passage
# aux limites des régions
def temps(v):
    y0, y1, y2, y3, y4, y5 = v
    t = sqrt(d1 * d1 + y0 ** 2) / 10            # temps de trajet de A au marais
    t += sqrt(10 * 10 + (y0 - y1) ** 2) / 9     # temps de passage dans la première zone
    t += sqrt(10 * 10 + (y1 - y2) ** 2) / 8
    t += sqrt(10 * 10 + (y2 - y3) ** 2) / 7
    t += sqrt(10 * 10 + (y3 - y4) ** 2) / 6
    t += sqrt(10 * 10 + (y4 - y5) ** 2) / 5
    t += sqrt(d1 * d1 + (y5 - yb) ** 2) / 10    # temps de trajet entre le marais et B
    return t


ligne_droite = [x0, x1, x2, x3, x4, x5]
res = minimize(temps, ligne_droite, tol=1e-10)

print(round(res.fun, 10))
print(round(temps(ligne_droite), 10))

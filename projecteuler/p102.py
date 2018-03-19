"""
Triangle containment

https://projecteuler.net/problem=102
"""


# https://openclassrooms.com/courses/theorie-des-collisions/formes-plus-complexes
def collision(poly, p):
    signe = 0
    for i, A in enumerate(poly):
        B = poly[(i + 1) % len(poly)]
        dx = B[0] - A[0]
        dy = B[1] - A[1]
        tx = p[0] - A[0]
        ty = p[1] - A[1]

        d = dx * ty - dy * tx
        if d * signe < 0:
            return False
        signe = d
    return True


def main():
    nb = 0
    for i, coords in enumerate(open("p102_triangles.txt")):
        poly = list(map(int, coords.split(",")))
        poly = list(zip(poly[::2], poly[1::2]))
        r = collision(poly, (0, 0))
        if r:
            nb += 1
    print(nb)


if __name__ == '__main__':
    main()

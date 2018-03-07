"""
Su Doku

https://projecteuler.net/problem=96
"""


def solve(grid):
    for i, n in enumerate(grid):
        if n == "0":
            # case vide

            # cherche les nombres manquants dans la ligne, la colonne et le carré 3x3
            y, x = divmod(i, 9)
            cx = (x // 3) * 3
            cy = (y // 3) * 3

            """
            def v(x, y):
                return grid[x + y * 9]

            found = set()
            for k in range(9):
                found.add(v(k, y))
                found.add(v(x, k))
                found.add(v(cx + k % 3, cy + k // 3))
            """

            # code similaire à ci-dessus... en bien plus optimisé
            k = cx + cy * 9
            found = set(grid[y * 9:y * 9 + 9]
                      + grid[x::9]
                      + grid[k:k + 3] + grid[k + 9:k + 12] + grid[k + 18:k + 21])

            missing = set("123456789") - found

            # essaie tous les manquants, récursivement
            for k in missing:
                h = grid[0:i] + k + grid[i + 1:]
                r = solve(h)
                if r is not None:
                    # on a trouvé une solution
                    return r

            # pas de solution :
            #  - cas missing=∅  (fin de la récursion)
            #  - aucune solution récursive satisfaisante
            return None

    # retourne le résultat
    return grid


result = 0
with open("p096_sudoku.txt") as f:
    for i in f:
        if i.startswith("Grid "):
            grid = ''.join([next(f).strip() for _ in range(9)])
            assert len(grid) == 81
            solution = solve(grid)
            # print(solution)
            result += int(solution[0:3])
print(result)

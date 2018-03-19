// Counting rectangles
//
// https://projecteuler.net/problem=85
// https://www.hackerrank.com/contests/projecteuler/challenges/euler085/problem

#include <stdio.h>
#include <math.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>


int64_t R(int64_t x, int64_t y)
{
    return x * (x + 1) * y * (y + 1) / 4;
}

int invT(int a)
{
    return (int)((sqrt(8 * a + 1) - 1) / 2);
}

int vmax(int a, int b)
{
    return a > b ? a : b;
}

void solve(int n)
{
    int x_max = invT(n) + 2;
    int64_t nb_min = 100000;
    int resultat = 0;

    for (int x = 1; x <= x_max; ++x)
    {
        for (int y = x; y <= x_max; ++y)
        {
            int64_t nb = R(x, y) - n;
            if (nb > nb_min) break;

            if (nb < 0) nb = -nb;
            if (nb < nb_min)
            {
                nb_min = nb;
                resultat = x * y;
            }
            else if (nb == nb_min)
            {
                resultat = vmax(resultat, x * y);
            }
        }
    }
    printf("%d\n", resultat);
}


int main(int argc, char *argv[])
{
    if (getenv("OUTPUT_PATH") != NULL || (argc >= 2 && !strcmp(argv[1], "hr")))
    {
        // HackerRank
        int T, n;
        scanf("%d", &T);
        while (T--)
        {
            scanf("%d", &n);
            solve(n);
        }
    }
    else
    {
        // Project Euler
        solve(2000000);
    }

    return 0;
}

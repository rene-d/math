/*
Right triangles with integer coordinates

https://projecteuler.net/problem=91
*/

#include <stdio.h>

static inline int sqr(int x)
{
    return x * x;
}

int main()
{
    const int N = 50;
    int nb = 0;

    // probablement optimisable...
    for (int x1 = 0; x1 <= N; ++x1)
    {
        for (int y1 = 0; y1 <= N; ++y1)
        {
            if (x1 == 0 && y1 == 0) continue;
            for (int x2 = 0; x2 <= N; ++x2)
            {
                for (int y2 = 0; y2 <= N; ++y2)
                {
                    if (x2 == 0 && y2 == 0) continue;
                    if (x1 == x2 && y1 == y2) continue;

                    int OA = sqr(x1) + sqr(y1);
                    int OB = sqr(x2) + sqr(y2);
                    int AB = sqr(x1 - x2) + sqr(y1 - y2);

                    if (OA + OB == AB || OA + AB == OB || OB + AB == OA)
                        nb++;
                }
            }
        }
    }
    printf("%d\n", nb / 2);
    return 0;
}

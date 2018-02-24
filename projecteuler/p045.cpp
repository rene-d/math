/*
Triangular, pentagonal, and hexagonal

https://projecteuler.net/problem=45
*/

/* https://en.wikipedia.org/wiki/Polygonal_number */

#include <stdio.h>


// Triangle
inline size_t Tn(size_t n)
{
    return n * (n + 1) / 2;
}

// Pentagonal
inline size_t Pn(size_t n)
{
    return n * (3 * n - 1) / 2;
}

// Hexagonal
inline size_t Hn(size_t n)
{
    return n * (2 * n - 1);
}


int main()
{
    size_t i = 285 + 1;
    size_t j = 165 + 1;
    size_t k = 143 + 1;

    size_t t, p, h;

    while (true)
    {
        t = Tn(i);
        p = Pn(j);
        h = Hn(k);

        if (t == p && p == h)
        {
            printf("%zu\n", t);
            //printf("%zu %zu %zu => %zu\n", i, j, k, t);
            break;
        }

        if (t <= p && t <= h) i++;
        if (p <= h && p <= t) j++;
        if (h <= t && h <= p) k++;
    }

    return 0;
}
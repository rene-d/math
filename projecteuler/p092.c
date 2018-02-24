/*
Square digit chains

https://projecteuler.net/problem=92
*/

#include <stdio.h>


int maillon(int n)
{
    int s = 0;
    while (n > 0)
    {
        int r = n % 10;
        s += r * r;
        n = n / 10;
    }
    return s;
}

int main()
{
    int i;
    int s = 0;
    for (i = 1; i < 10000000; ++i)
    {
        int e = i;
        for (e = i; e != 1 && e != 89; e = maillon(e))
        {
           // printf("%d %d\n", i, e);
        }
        if (e == 89) s += 1;
    }
    printf("%d\n", s);
}

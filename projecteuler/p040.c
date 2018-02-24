// Champernowne's constant
//
// https://projecteuler.net/problem=40

#include <stdio.h>
#include <stdlib.h>

const int L = 1000000;

int main()
{
    char *d = (char *) malloc(L + 16);
    int len = 0;
    int i = 0;

    while (len <= L)
    {
        int n, k;

        k = i;
        while (k > 0) { k /= 10; ++len; }

        n = len;
        k = i;
        while (k > 0) { d[n--] = k % 10; k /= 10; }

        ++i;
    }

    printf("%d\n", d[1] * d[10] * d[100] * d[1000] * d[10000] * d[100000] * d[1000000]);
    //printf("%d %d %d %d %d %d %d\n", d[1], d[10], d[100], d[1000], d[10000], d[100000], d[1000000]);

    free(d);

    return 0;
}
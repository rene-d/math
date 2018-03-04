/*
Prime digit replacements

https://projecteuler.net/problem=51
*/

#include <stdio.h>
#include <string.h>
#include <stdbool.h>
#include <assert.h>

/*
   constat amusant
    série de nombres premiers: 000857 111857 222857 333857 555857 666857 777857
*/

const int famille = 8;


bool est_premier(int n)
{
    if (n == 2) return true;
    if (n % 2 == 0 || n < 2) return false;
    int i = 3;
    while (i * i <= n)
    {
        if (n % i == 0) return false;
        i += 2;
    }
    return true;
}


int remplace(int n, int a, int b)
{
    int p = 1;
    int m = 0;
    int c = 0;
    while (n != 0)
    {
        c = n % 10;
        if (c == a) c = b;
        m += (c * p);
        p *= 10;
        n /= 10;
    }
    // cas de chiffre du début remplacé par 0
    if (c == 0) return n;
    return m;
}


int main()
{
    int    n = 56003;
    int    nb_digits[10];
    int    prem = 0;

    assert(est_premier(56003));

    while (prem < famille && n < 10000000)
    {
        ++n;

        if (! est_premier(n)) continue;

        memset(nb_digits, 0, sizeof(nb_digits));
        for (int k = n; k != 0; k /= 10)
        {
            ++nb_digits[k % 10];
        }

        for (int d = 0; d < 10; ++d)
        {
            if (nb_digits[d] < 2) continue;

            prem = 1;
            for (int e = 0; e < 10; ++e)
            {
                if (e == d) continue;
                int m = remplace(n, d, e);
                if (m != n && est_premier(m)) ++prem;
            }

            if (prem >= famille)
            {
                printf("%d\n", n);

                printf("\n");
                for (int e = 0; e < 10; ++e)
                {
                    if (e == d) continue;
                    int m = remplace(n, d, e);
                    if (m == n || ! est_premier(m)) continue;
                    printf("%d -> %d premier (%d -> %d)\n", n, m, d, e);
                }

                break;
            }
        }
    }

    return 0;
}
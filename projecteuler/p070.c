#include <stdio.h>
#include <stdbool.h>


// calcul de l'Indicatrice d'Euler φ(n) ou totient(n)
int EulerPhi(int n)
{
    int phi = n;
    int i = 2;
    while (i * i <= n)
    {
        if (n % i == 0)
            phi -= phi / i;
        while (n % i == 0)
            n = n / i;
        i += (i != 2) ? 2 : 1;
    }
    if (n > 1)
        phi -= phi / n;
    return phi;
}


// détermine si deux nombres ont les mêmes chiffres
bool est_permutation(int a, int b)
{
    char    chiffres[10] = { 0 };

    while (a != 0)
    {
        ++chiffres[a % 10];
        a /= 10;
    }
    while (b != 0)
    {
        --chiffres[b % 10];
        b /= 10;
    }

    for (int i = 0; i < 10; ++i)
        if (chiffres[i] != 0)
            return false;

    return true;
}



int main()
{
    float rmin = 10;
    int nmin = 0;

    for (int n = 2; n < 10000000; ++n)
    {
        int p = EulerPhi(n);
        float r = (float)n / (float)p;

        if (r < rmin && est_permutation(p, n))
        {
            rmin = r;
            nmin = n;
        }
    }

    printf("%d\n", nmin);
    return 0;
}

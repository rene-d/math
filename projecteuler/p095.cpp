/*"
Amicable chains

https://projecteuler.net/problem=95
*/

#include <cstdio>
#include <vector>
#include <algorithm>


const unsigned N = 1000000;


int main()
{
    std::vector<unsigned>    sum_of_div(N);
    std::vector<bool>   utilises(N);
    unsigned nmax = 0;
    unsigned xmin = N;

    // Sum of Divisors Sieve O(n log n)
    // http://codeforces.com/blog/entry/8989
    // For every number i, You know that j=2*i,3*i,4*i upto k*i such that k*i<N, will have
    // i as one of it's divisors, so add i that to divisorSum[j]
    for (unsigned i = 1; i < N; ++i)
    {
        for (unsigned j = 2 * i; j < N; j += i)
            sum_of_div[j] += i;
    }

    for (unsigned i = 1; i < N; ++i)
    {
        std::fill(utilises.begin(), utilises.end(), false);

        unsigned a = i;
        unsigned n = 0;
        while (n++ < 1000)
        {
            if (utilises[a]) break;
            utilises[a] = true;

            a = sum_of_div[a];
            if (a >= N) break;  // évite que la chaîne déborde
        }

        if (a == i)
        {
            if (nmax < n) { nmax = n; xmin = N; }
            //printf("[%d] chaine %2d :", i, n);
            unsigned k = n;
            while (--k > 0)
            {
                if (nmax == n && xmin > a) xmin = a;
                a = sum_of_div[a];
                //printf(" %d", a);
            }
            //printf("\n");
        }
    }

    printf("%d\n", xmin);

    return 0;
}
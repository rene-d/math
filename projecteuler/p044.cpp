/*
Pentagon numbers

https://projecteuler.net/problem=44
*/

#include <iostream>
#include <vector>

const size_t L = 3000;

inline size_t Pn(size_t n)
{
    return n * (3 * n - 1) / 2;
}

int main()
{
    std::vector<bool> is_pentagonal(Pn(2 * L) + 1);

    for (size_t n = 1; n < 2 * L; ++n)
    {
        is_pentagonal[Pn(n)] = true;
    }

    for (size_t j = 1; j < L; ++j)
    {
       size_t Pj = Pn(j);

        for (size_t k = j + 1; k < L; ++k)
        {
            size_t Pk = Pn(k);

            size_t diff = Pk - Pj;
            size_t sum = Pk + Pj;

            if (is_pentagonal[diff] && is_pentagonal[sum])
            {
                printf("%zd\n", diff);
                //printf("%zd %zd D=%zd\n", j, k, d);
            }
        }
    }

    return 0;
}
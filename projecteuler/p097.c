// Large non-Mersenne prime
//
// https://projecteuler.net/problem=97

#include <stdio.h>
#include <stdint.h>
#include <inttypes.h>

int main()
{
    uint64_t    m = 28433;

    for (unsigned i = 0; i < 7830457; ++i)
    {
        m = m * 2;
        m = m % 10000000000;
    }
    m = m + 1;

    printf("%" PRIu64 "\n", m);

    return 0;
}

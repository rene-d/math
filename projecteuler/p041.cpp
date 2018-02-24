// Pandigital prime
//
// https://projecteuler.net/problem=41

#include <iostream>
#include <algorithm>
#include <cstdint>
#include <cmath>
#include <cinttypes>
#include <cstdlib>


bool is_prime(uint32_t i)
{
    if (i == 2) return true;
    if (i % 2 == 0) return false;
    uint32_t n = (uint32_t) sqrt(i);
    for (uint32_t j = 3; j <= n; j += 2)
    {
        if (i % j == 0) return false;
    }
    return true;
}


uint32_t check(char *chiffres, size_t nb)
{
    do {
        uint32_t n = (uint32_t) strtoul(chiffres, NULL, 10);
        if (is_prime(n))
            return n;
    } while (std::prev_permutation(chiffres, chiffres + nb));
    return 0;
}


int main()
{
    const char chiffres[] = "987654321";

    for (size_t n = 0; n < 9; ++n)
    {
        char    work[16];

        // supprime les n premiers chiffres et le \0 final (pour strtoul)
        memmove(work, chiffres + n, (9 - n) + 1);

        uint32_t m = check(work, 9 - n);
        if (m != 0)
        {
            std::cout << m << std::endl;
            break;
        }
    }

    return 0;
}
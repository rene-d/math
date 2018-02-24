// Sub-string divisibility
//
// https://projecteuler.net/problem=43

#include <iostream>
#include <algorithm>
#include <cstdint>
#include <cmath>
#include <cinttypes>


int d(const char *chiffres, int p)
{
    return (chiffres[p - 1] - '0') * 100 + (chiffres[p] - '0') * 10 + (chiffres[p + 1] - '0');
}

int main()
{
    char chiffres[] = "9876543210";
    uint64_t somme = 0;

    do {
        if (d(chiffres, 2) % 2 != 0) continue;
        if (d(chiffres, 3) % 3 != 0) continue;
        if (d(chiffres, 4) % 5 != 0) continue;
        if (d(chiffres, 5) % 7 != 0) continue;
        if (d(chiffres, 6) % 11 != 0) continue;
        if (d(chiffres, 7) % 13 != 0) continue;
        if (d(chiffres, 8) % 17 != 0) continue;

        somme += strtoul(chiffres, NULL, 0);
    } while (std::prev_permutation(chiffres, chiffres + 10));

    std::cout << somme << std::endl;

    return 0;
}
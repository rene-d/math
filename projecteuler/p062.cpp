/*
Cubic permutations

https://projecteuler.net/problem=62
*/

#include <cstdint>
#include <map>
#include <iostream>

struct cube
{
    uint64_t    n3;
    unsigned    perm;
};


// index qui ne dépend que du nombre de chiffres 0 à 9
// ainsi, toutes les permutations des chiffres de n produiront le même index
uint64_t index(uint64_t n)
{
    uint64_t i = 0;
    while (n != 0)
    {
        uint64_t c = n % 10;
        i += 1ul << (c * 4);        // stocke le nombre de chiffre c dans le c-ième quartet
        n = n / 10;
    }
    return i;
}


int main()
{
    uint64_t        n3, i;
    uint64_t        n;
    std::map<uint64_t, cube>   cubes;

    for (n = 225; n < 100000; ++n)
    {
        n3 = n * n * n;

        i = index(n3);

        auto it = cubes.find(i);
        if (it == cubes.end())
        {
            cubes[i] = { n3, 1 };
        }
        else
        {
            unsigned perm = ++(it->second.perm);
            if (perm == 5)
            {
                std::cout << it->second.n3 << std::endl;
                break;
            }
        }
    }

    return 0;
}

/*
Concealed Square

https://projecteuler.net/problem=206
*/

#include <stdio.h>
#include <math.h>
#include <stdint.h>
#include <inttypes.h>


void bruteforce1()
{
    uint64_t    n, r;
                         //  1_2_3_4_5_6_7_8_9_0      1_2_3_4_5_6_7_8_9_0
    for (uint64_t a = 0; a <=                 90; a += 10)
    for (uint64_t b = 0; b <=               9000; b += 1000)
    for (uint64_t c = 0; c <=             900000; c += 100000)
    for (uint64_t d = 0; d <=           90000000; d += 10000000)
    for (uint64_t e = 0; e <=         9000000000; e += 1000000000)
    for (uint64_t f = 0; f <=       900000000000; f += 100000000000)
    for (uint64_t g = 0; g <=     90000000000000; g += 10000000000000)
    for (uint64_t h = 0; h <=   9000000000000000; h += 1000000000000000)
    for (uint64_t i = 0; i <= 900000000000000000; i += 100000000000000000)
    {                    //  1_2_3_4_5_6_7_8_9_0      1_2_3_4_5_6_7_8_9_0
        //  1_2_3_4_5_6_7_8_9_0
        n = 1020304050607080900 + a + b + c + d + e + f + g + h + i;

        r = sqrt(n);
        if (r * r == n)
        {
            printf("%" PRIu64 "\n", r);
            return; // solution unique
        }
    }
}


void bruteforce2()
{
    uint64_t    n, r;
    uint64_t    a = sqrt(1020304050607080900);
    uint64_t    b = sqrt(1929394959697989990);
    int         i;

    for (r = b; r >= a; r--)
    {
        n = r * r;

        static const int digits[] = { 0, 9, 8, 7, 6, 5, 4, 3, 2, 1 };

        // 1_2_3_4_5_6_7_8_9_0
        for (i = 0; i < 10; ++i)
        {
            if (n % 10 != digits[i]) break;
            n /= 100;
        }
        if (i == 10)
        {
            printf("%" PRIu64 "\n", r);
            break;  // solution unique
        }
    }
}


int main()
{
    // la bruteforce2 est plus rapide si on teste de b -> a
    // et plus lente si on fait l'inverse...
    // j' "optimise" ;-)
    bruteforce2();
    return 0;
}


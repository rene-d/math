/*
Crack-free Walls

https://projecteuler.net/problem=215
*/

#include <vector>
#include <iostream>
#include <cstdint>
#include <algorithm>
#include <functional>
#include <numeric>

using namespace std;


int width = 32;
int height = 10;


// find (recursively) all brick configurations that can fill one row
void find_rows(vector<uint64_t>& rows, uint64_t row, int x)
{
    if (x < width)
    {
        for (int brick = 2; brick <= 3; ++brick)
        {
            if (x + brick == width)
            {
                rows.push_back(row);
                break;
            }
            else if (x + brick < width)
            {
                row |= 1 << (x + brick);
                find_rows(rows, row, x + brick);
                row &= ~(1 << (x + brick));
            }
        }
    }
}


int main()
{
    // get all brick arrangements
    vector<uint64_t> rows;

    find_rows(rows, 0, 0);

    // for each brick arrangement, find the rows that can stack (i.e. no crack at same position)
    vector<vector<size_t>> stackable_rows(rows.size());

    for (size_t i = 0; i < rows.size(); ++i)
    {
        for (size_t j = 0; j < rows.size(); ++j)
        {
            if ((rows[i] & rows[j]) == 0)
                stackable_rows[i].push_back(j);
        }
    }

    // stack up to 'height' rows
    vector<uint64_t> walls(rows.size(), 1ull);
    vector<uint64_t> walls2(rows.size(), 0ull);

    while (--height)        // loop height-1 times
    {
        size_t i = 0;
        for (const auto& row : stackable_rows)
        {
             walls2[i++] = accumulate(row.begin(), row.end(),
                                      0ull,
                                      [walls](uint64_t a, size_t b) { return a + walls[b]; });
        }
        swap(walls, walls2);
    }

    // count solutions and print the answer
    cout << accumulate(walls.begin(), walls.end(), 0ull) << endl;

    return 0;
}

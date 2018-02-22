"""
Counting Sundays

"""

import datetime

resultat = 0
for y in range(1901, 2001):
    for m in range(1, 13):
        if datetime.datetime(y, m, 1).weekday() == 6:
            resultat += 1
print(resultat)

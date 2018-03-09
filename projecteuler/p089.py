"""
Roman numerals

https://projecteuler.net/problem=89
"""
numeral_map = tuple(zip(
    (1000, 900, 500, 400, 100, 90, 50, 40, 10, 9, 5, 4, 1),
    ('M', 'CM', 'D', 'CD', 'C', 'XC', 'L', 'XL', 'X', 'IX', 'V', 'IV', 'I')
))


def int_to_roman(i):
    result = []
    for integer, numeral in numeral_map:
        count = i // integer
        result.append(numeral * count)
        i -= integer * count
    return ''.join(result)


def roman_to_int(n):
    i = result = 0
    for integer, numeral in numeral_map:
        while n[i:i + len(numeral)] == numeral:
            result += integer
            i += len(numeral)
    return result


resultat = 0
for num in open("p089_roman.txt"):
    num = num.strip()
    resultat += len(num)
    i = roman_to_int(num)
    r = int_to_roman(i)
    resultat -= len(r)
    # print("{:<15} {:<5} {:<15}".format(num, i, r))
print(resultat)

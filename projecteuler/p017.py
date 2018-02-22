"""
https://projecteuler.net/problem=17
"""

units = ['zero', 'one', 'two', 'three', 'four',
         'five', 'six', 'seven', 'eight', 'nine',
         'ten', 'eleven', 'twelve', 'thirteen', 'fourteen',
         'fifteen', 'sixteen', 'seventeen', 'eighteen', 'nineteen']
teens = ['twenty', 'thirty', 'forty', 'fifty', 'sixty', 'seventy', 'eighty', 'ninety']


def int2words(n):
    """
    https://en.wikipedia.org/wiki/English_numerals
    http://www.lexisrex.com/English-Numbers/
    """
    assert n >= 0

    if n < 20:
        return units[n]

    if n < 100:
        w = teens[n // 10 - 2]
        if n % 10 != 0:
            w += "-" + units[n % 10]
        return w

    if n < 1000:
        w = units[n // 100] + " hundred"
        if n % 100 != 0:
            w += " and " + int2words(n % 100)
        return w

    if n < 1000000:
        w = int2words(n // 1000) + " thousand"
        if n % 1000 != 0:
            w2 = int2words(n % 1000)
            if w2.find(" and ") == -1:
                w += " and " + w2
            else:
                w += " " + w2
        return w

    assert w >= 1000000


resultat = 0
for i in range(1, 1001):
    w = int2words(i)
    w = w.replace(" ", "")
    w = w.replace("-", "")
    resultat += len(w)
print(resultat)

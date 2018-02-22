"""
XOR decryption

https://projecteuler.net/problem=59
"""


def is_letter(c):
    """ vérifie si c est une lettre majuscule ou minuscule """
    return (65 <= c <= 90) or (97 <= c <= 122)


def decrypt(encoded, key):
    decoded = []
    len_key = len(key)
    len_enc = len(encoded)

    nb_others = 0
    nb_chars = 0
    nb_err = 0

    for i, c in enumerate(encoded):
        c = c ^ key[i % len_key]

        if 65 <= c <= 90 or 97 <= c <= 122:
            nb_chars += 1
        else:
            nb_others += 1

        decoded.append(c)

    n = 0
    for i in decoded:
        if is_letter(i):
            n += 1
        else:
            if n > 0:
                if chr(i) not in [' ', ',', '.', ':', '!', '\n', "'"]:
                    nb_err += 1
            n = 0

    if nb_err > 5:
        return None

    if nb_chars < len_enc * 0.7 or nb_others > len_enc * 0.3:
        return None

    print(''.join([chr(i) for i in decoded]))
    print('key:', [chr(i) for i in key])
    print('stats:', nb_chars, nb_others, nb_err, len_enc)
    print('solution:', sum(decoded))


with open("p059_cipher.txt") as f:
    cipher = [int(i) for i in f.read().strip().split(",")]

for a in range(97, 123):
    for b in range(97, 123):
        for c in range(97, 123):
            decrypt(cipher, [a, b, c])

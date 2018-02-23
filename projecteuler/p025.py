"""
1000-digit Fibonacci number

https://projecteuler.net/problem=25
"""

a, b = 1, 1
i = 1
while True:
    i += 1
    a, b = b, a + b

    if len(str(a)) >= 1000:
        print(i)
        break

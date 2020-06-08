class Fraction:
    """
    calculs sur ℚ (ensemble des entiers rationnels)
    """

    def __init__(self, num, den=1):
        assert den != 0
        self.num = num
        self.den = den
        self.simplifie()

    def __str__(self):
        if self.den == 1:
            return str(self.num)
        else:
            return "{}/{}".format(self.num, self.den)

    def simplifie(self):
        d = pgcd(self.num, self.den)
        if d != 1:
            self.num = self.num // d
            self.den = self.den // d

    def __add__(self, r):
        if isinstance(r, Fraction):
            n = Fraction(self.num * r.den + self.den * r.num, self.den * r.den)
        elif isinstance(r, int):
            n = Fraction(self.num + self.den * r, self.den)
        else:
            raise TypeError
        n.simplifie()
        return n

    def __sub__(self, r):
        if isinstance(r, Fraction):
            n = Fraction(self.num * r.den - self.den * r.num, self.den * r.den)
        elif isinstance(r, int):
            n = Fraction(self.num - self.den * r, self.den)
        else:
            raise TypeError
        n.simplifie()
        return n

    def __mul__(self, other):
        if isinstance(other, Fraction):
            n = Fraction(self.num * other.num, self.den * other.den)
        elif isinstance(other, int):
            n = Fraction(self.num * other, self.den)
        else:
            raise TypeError
        n.simplifie()
        return n

    def __truediv__(self, other):
        """ f / g ou f / 1 """
        if isinstance(other, Fraction):
            n = Fraction(self.num * other.den, self.den * other.num)
        elif isinstance(other, int):
            n = Fraction(self.num, self.den * other)
        else:
            raise TypeError
        n.simplifie()
        return n

    def __radd__(self, other):
        """ cas de 1 + f """
        return self.__add__(other)

    def __rsub__(self, other):
        """ cas de 1 - f """
        new = self.__sub__(other)
        new.num = -new.num
        return new

    def __rtruediv__(self, other):
        """ 1 / f """
        if isinstance(other, int):
            new = Fraction(self.den * other, self.num)
        else:
            raise TypeError
        new.simplifie()
        return new

    def __neg__(self):
        return Fraction(-self.num, self.den)

    def __ge__(self, other):
        if isinstance(other, Fraction):
            return self.num * other.den >= self.den * other.num
        elif isinstance(other, int):
            return self.num >= self.den * other.num
        else:
            raise TypeError

    def __lt__(self, other):
        return not self.__ge__(other)

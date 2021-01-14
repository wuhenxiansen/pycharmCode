#Implements rational number arithmetic.

import math

#Determine multiplicative inverse of n1 mod n2 (both integers) via extended Euclidean algorithm.
def inverse(n1, n2):
    n1 = n1 % n2
    if n1 == 1: 
        return n1
    q = n2 // n1
    r = n2 % n1
    a = (0, 1) #a and b keep values of successive remainders as linear combinations of n1 and n2. This removes the need to backtrack
    b = (1,-q) #Initially, a is (n2 = 0 * n1 + 1 * n2) and b is (r = 1 * n1 - q * n2)
    while r > 1:
        x = (a[0] * n2 + a[1] * n1)
        y = (b[0] * n2 + b[1] * n1)
        q = x // y
        r = x % y
        a, b = b, (a[0] - q * b[0], a[1] - q * b[1])
    if r > 0:
        return b[1]
    raise ValueError("{} is not invertible mod {}".format(n1, n2))

#The main issue with this class is that it only permits arithmetic between Fraction instances (e.g. you can't add int to frac).
#Luckily, for our purposes this is all we need.
class Fraction():
    def __init__(self, num, denom):
        self.num = num // math.gcd(num, denom) #Simplify
        self.denom = denom // math.gcd(num, denom)
        if self.denom < 0: #Put negatives in numerator
            self.denom = -self.denom
            self.num = -self.num

    def __add__(self, other): 
        if type(other) == Fraction:
            return Fraction(self.num * other.denom + self.denom * other.num, self.denom * other.denom)
        raise NotImplementedError

    def __mul__(self, other):
        if type(other) == Fraction:
            return Fraction(self.num * other.num, self.denom * other.denom)
        raise NotImplementedError

    def __neg__(self):
        return Fraction(-self.num,self.denom)

    def __sub__(self, other):
        if type(other) == Fraction:
            return self + -other
        raise NotImplementedError

    def __truediv__(self, other):
        if type(other) == Fraction:
            return Fraction(self.num * other.denom, self.denom * other.num)
        raise NotImplementedError

    #Equality testing and order is possible between Fraction and non-fraction types.

    def __eq__(self, other):
        if  type(other) != Fraction:
            return self.num / self.denom == other
        else:
            return self.num / self.denom == other.num / other.denom

    def __lt__(self, other):
        if  type(other) != Fraction:
            return self.num / self.denom < other
        else:
            return self.num / self.denom < other.num / other.denom

    def __le__(self, other):
        return self < other or self == other

    def __gt__(self, other):
        return not self <= other

    def __ge__(self, other):
        return not self < other

    #Makes output easy to read -- Fraction(a,b) is printed as "a/b"
    def __repr__(self):
        if self.denom == 1: #Special case if the denominator is 1
            return str(self.num)
        return str(self.num) + '/' + str(self.denom)

    def __abs__(self):
        return Fraction(abs(self.num),abs(self.denom))

    #The expression (a/b)%c returns ab^(-1) where b^(-1) is the inverse of b mod c.
    #C must a fraction with denominator 1.
    def __mod__(self, other): 
        if other.denom != 1:
            raise NotImplementedError
        return Fraction((self.num * inverse(self.denom, other.num)) % other.num, 1)

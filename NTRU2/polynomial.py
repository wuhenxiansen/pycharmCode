from fraction import Fraction
import copy

#Implements polynomial arithmetic in Q[x].

class Polynomial():

    #Polynomials are represented as lists of coefficients, where L[i] is the coefficient of x^i.
    def __init__(self,coefficents): 
        self.coefs = coefficents
        
        #Get rid of trailing zeroes
        while self.coefs[-1] == 0:
            self.coefs = self.coefs[:-1]
            if len(self.coefs) == 0:
                self.coefs = [0]
                break
            
        self.degree = len(self.coefs) - 1

        #Make all coefficients fractions
        for c in range(len(self.coefs)): 
            if type(self.coefs[c]) == int:
                self.coefs[c] = Fraction(self.coefs[c],1)

    #Arithmetic operations
    def __add__(self, other): 
        n = max(self.degree, other.degree) + 1
        res = [Fraction(0,1) for i in range(n)]
        for i in range(n):
            if self.degree >= i: 
                res[i] += self.coefs[i]
            if other.degree >= i:
                res[i] += other.coefs[i]
        return Polynomial(res)

    def __neg__(self):
        return Polynomial([-i for i in self.coefs])

    def __sub__(self, other):
        return self + (-other)

    def __mul__(self, other):
        deg = self.degree + other.degree + 1
        res = [Fraction(0,1) for i in range(deg)]
        for i in range(deg):
            for j in range(i+1):
                if j <= self.degree and i - j <= other.degree:
                    res[i] += self.coefs[j] * other.coefs[i - j]
        return Polynomial(res)

    #Determines remainder via polynomial long division.
    def __mod__(self, other): 
        if type(other) == int:
            other = Polynomial([other])
        #If other is an integer, just take all the coefficients modulo it.  This is equivalent to putting the polynomial in Z_n[x]
        if other.degree == 0: 
            return Polynomial([i % other.coefs[0] for i in self.coefs])
        else:
            self2 = copy.deepcopy(self)
            while self2.degree >= other.degree:
                factor = Polynomial([0 for _ in range(self2.degree - other.degree)] + [self2.coefs[-1] / other.coefs[-1]])
                self2 -= factor * other
            return self2
        
    #Determines quotient via polynomial long division. 
    def __floordiv__(self, other):
        if type(other) == int:
            other = Polynomial([other])
        #If other is an integer, just treat it like a normal division.
        if other.degree == 0: 
            return Polynomial([i / other.coefs[0] for i in self.coefs])
        else:
            if self.degree < other.degree:
                return Polynomial([0])
            factor = Polynomial([0 for _ in range(self.degree - other.degree)] + [self.coefs[-1] / other.coefs[-1]])
            return (factor + (self - factor * other).__floordiv__(other))

    #Uses extended Euclidean algorithm to compute inverses in Q[x].
    #To get inverses in Z_n[x], do f.inverse(g) % n.
    def inverse(self, other): 
        try:                  
            self2 = self % other
            q = other // self2
            r = other % self2
            a = (Polynomial([0]), Polynomial([1]))
            b = (Polynomial([1]), -q)
            while r.degree > 0:
                x = (a[0] * other + a[1] * self2)
                y = (b[0] * other + b[1] * self2)
                q = x // y
                r = x % y
                a, b = b, (a[0] - q * b[0], a[1] - q * b[1])
            return (b[1] // r)
        except ValueError:
            raise ValueError("{} is not invertible mod {}".format(self, other))

    #Put coefficients between -n and n.
    def centeredLift(self, n):
        lift = self % n
        for c in range(len(lift.coefs)):
            if lift.coefs[c] > Fraction(n // 2,1):
                lift.coefs[c] -= Fraction(n,1)
        return lift

    #Pretty-print polynomials.
    def __repr__(self):
        st = ''
        if self.coefs[0] != 0 or len(self.coefs) == 1:
            st = str(self.coefs[0])
        for i in range(1, len(self.coefs)):
            sign = ''
            c = ''
            exp = ''
            if self.coefs[i] == Fraction(0,1):
                continue
            if self.coefs[i] < Fraction(0,1):
                sign = '-'
            if self.coefs[i] > Fraction(0,1):
                sign = '+'
            if abs(self.coefs[i]) != 1:
                c = str(abs(self.coefs[i]))
            if i > 1:
                exp = "^" + str(i)

            st += " {} {}x{}".format(sign, c, exp)
        if len(st) > 1 and st[1] == "+":
            st = st[3:]
        return st

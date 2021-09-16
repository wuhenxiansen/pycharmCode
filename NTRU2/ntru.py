import random
from fraction import Fraction
from polynomial import Polynomial

#===================================
#Parameters
# n = 43
# p = 3
# q = 32
# df = 4
# dg = 2
# d = 3

n = 97
p = 3
q = 48
df = 3
dg = 2
d = 2
#poly = x^N -1
poly = Polynomial([-1] + [0] * (n-1) + [1]) 

#===================================

#Get a random polynomial in L(d1,d2)
def randpoly(d1, d2, n=n):

    def shuffle(lst):
        random.shuffle(lst)
        return lst

    coefs = shuffle(list(range(n)))[:d1 + d2]
    pos = shuffle(coefs)[:d1]
    poly = [0 for i in range(n)]
    
    for i in coefs:
        if i in pos:
            poly[i] = 1
        else:
            poly[i] = -1
    return Polynomial(poly)
    
#Gets a random (invertible) polynomial in L(d1,d2)
def randInvertPoly(d1, d2, n=n): 
    while True:
        try:
            f = randpoly(d1,d2,n=n)
            print('f(x)={}'.format(f))
            inv = f.inverse(poly)
            fp = inv % p
            fq = inv % q
            print('fp(x)={}'.format(fp))
            print('fq(x)={}'.format(fq))
            return f, fp, fq
        except ValueError:
            continue

#===================================

#Private key
f, fp, fq = randInvertPoly(df,df-1)
print('私钥：由f和fp构成')
g = randpoly(dg,dg)
print('g(x)={}'.format(g))
#Public key
h = (fq * g) % poly % q 
print('公钥：{}'.format(h))
#Encryption
#Encrypted message E = p * phi * h + M mod q
def encrypt(message):#message是一个关于明文的多项式
    phi = randpoly(d,d)
    print("加密公式：c(x)=p(x)*多项式phi*h+m(x)")
    return (Polynomial([p]) * phi * h + message) % poly % q

#Decryption
#a = centered lift of f * E mod q, M = centered lift of Fp * a mod p
def decrypt(message):#解密多项式
    a = ((f * message) % poly % q).centeredLift(q)
    print("解密公式：m(x)=fp*a=fp*f*c=sk*c")
    return ((fp * a) % poly % p).centeredLift(p)
def CiphertextoPoly(Ciphertext):
    return (Ciphertext % poly).centeredLift(2)
#===============================

#Utility functions

#Convert an ASCII message to binary, then interpret the binary as a polynomial that can be encrypted.
def textToPoly(text):#将明文转换为多项式
    binary = ''
    for c in text:
        binary += format(ord(c),'08b')
    poly = [0 for i in range(len(binary))]
    for b in range(len(binary)):
        poly[b] = int(binary[b])
    print(poly)
    print('明文{}对应的多项式是：{}'.format(text,Polynomial(poly)))
    return Polynomial(poly)

#Interpret a 0,1 polynomial as binary, then convert to ASCII text.
def polyToText(poly): #传入一个多项式系数数组得到对应数据
    message = ''
    binary = 0b0
    for i in range(len(poly.coefs) + 1):
        if i > 0 and i % 8 == 0:
            message += chr(binary)
            binary = 0
        if i < len(poly.coefs):
            binary <<= 1
            binary += poly.coefs[i].num
    return message
def polyToBinarText(poly): #返回对应的
    message = ''
    binary = 0b0
    for i in range(len(poly.coefs) + 1):
        if i > 0 and i % 8 == 0:
            message += chr(binary)
            binary = 0
        if i < len(poly.coefs):
            binary <<= 1
            binary += poly.coefs[i].num
    return message

def encryptText(text):
    return encrypt(textToPoly(text))

def decryptText(message):
    return polyToText(decrypt(message))
# c=encryptText('1')
c2=encryptText('1234567898515')
# print('密文多项式:{}'.format(c))
print('密文多项式:{}'.format(c2))
#print('密文:{}'.format(polyToBinarText(CiphertextoPoly(c))))
# print(decryptText(c))
print(decryptText(c2))

    
    
    
                



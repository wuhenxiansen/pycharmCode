from poly import poly
from poly import can_not_div_Error
from poly import egcd
import random
class ntru:
	def __init__(self,N,p,q,Fp = None,Fq = None,g = None,private_key = None,public_key = None):
		self.N = N
		self.p = p
		self.q = q
		self.private_key = private_key
		self.public_key = public_key 
		self.Fp = Fp
		self.Fq = Fq
		self.g = g
		P = [0] * (N + 1) 
		P[0] = -1
		P[N] = 1
		self.P = poly(P) 

	def _randpoly(self,one = None,_one = None):
		if one == None and _one == None:
			tot = random.randint(2,self.N - 1)
			one = random.randint(0,tot)
			_one = tot - one
		r =[0] * self.N
		while one != 0 or _one != 0:
			pos = random.randint(0,self.N - 1)
			if r[pos] is 0:
				if one > 0:
					r[pos] = 1
					one -= 1
				elif _one > 0:
					r[pos] = -1
					_one -= 1
		return poly(r)

	def randpoly_private(self):
		if self.N == 107:
			return self._randpoly(15, 14)
		if self.N == 167:
			return self._randpoly(61, 60)
		elif self.N == 503:
			return self._randpoly(216, 215)
		else:
			return self._randpoly()

	def randpoly_g(self):
		if self.N == 107:
			return self._randpoly(12, 12)
		elif self.N == 167:
			return self._randpoly(20, 20)
		elif self.N == 503:
			return self._randpoly(72, 72)
		else:
			return self._randpoly()

	def randpoly_phi(self):
		if self.N == 107:
			return self._randpoly(5, 5)
		if self.N == 167:
			return self._randpoly(18, 18)
		elif self.N == 503:
			return self._randpoly(55, 55)
		else:
			return self._randpoly()		
	def get_public(self):
		#self.public_key = 
		pass
	def createKey_pair(self):
		N = self.N
		q = self.q
		p = self.p
		self.private_key = self.randpoly_private()
		self.g = self.randpoly_g()
		while self.g.is_z():
			self.g = self.randpoly_g()
		tmp = q
		k = 0
		while tmp != 0:
			tmp = tmp // 2
			k += 1
		k -= 1
		while True:
			try:
				self.Fq = self.private_key.inv(N,2,k)
				self.Fp = self.private_key.inv(N,p,1)
				if (self.Fq is not False) and (self.Fp is not False):
					break
				self.private_key = self.randpoly_private()
			except can_not_div_Error:
				self.private_key = self.randpoly_private()	

		h = self.Fq.StarMult(self.g,N,q)
		self.public_key = h
		return (h,self.private_key)
	def encrypto(self,m):
		phi = self.randpoly_phi()

		#phi = poly([-1,1,0,0,1,-1,1])
		c = phi.StarMult(self.public_key,self.N,self.q)
		c2 = phi.StarMult(self.public_key,self.N,self.q)
		#print('公钥是：{}'.format(self.public_key.coe))
		c.expend(self.N)
		c2.expend(self.N)
		m.expend(self.N)
		for i in range(0,self.N):
			c.coe[i] = self.p * c.coe[i] + m.coe[i]
			c.coe[i] %= self.q
			# c2.coe[i] = self.p * c2.coe[i] + m.coe[i]
			# if c2.coe[i]+self.p*3<256:
			# 	c2.coe[i]+=self.p*3
			# elif c2.coe[i]-self.p*3<256:
			# 	c2.coe[i]-=self.p*3
			# c2.coe[i] %= self.q
		return c
	def decrypto(self,m):
		a = self.private_key.StarMult(m,self.N,self.q)
		#print('私钥是：{}'.format(self.private_key.coe))
		for i in range(0,len(a.coe)):
			if a.coe[i] < 0:
				a.coe[i] += self.q
			if a.coe[i] > self.q / 2:
				a.coe[i] = a.coe[i] - self.q
		M = a.StarMult(self.Fp,self.N,self.p).polydiv(self.P,self.p)[1]
		return M
"""
TEST
"""

NTRU = ntru(503,3,256,Fp=poly([-1,0,1,1]),public_key=poly([1,2,0,-2,-1]),private_key=poly([-1,1,0,0,1]))
NTRU.createKey_pair()
#print('私钥：{}'.format(NTRU.private_key.coe))
#print('公钥：{}'.format(NTRU.public_key.coe))
message1=list()
for i in range(10):
	n=random.randint(30,50)
	t=[]
	for j in range(n):
		t.append(random.randint(0,1))
	message1.append(t)
for me in message1:
	print(me)
	c=NTRU.encrypto(poly(me))
	m=NTRU.decrypto(c)
	m.expend(len(me))
	if me==m.coe:
		print("True,{}".format(m.coe))
# message=[[1,1,1,1,1,1,1,1,1,0,0],[1,0,0,0,1,0,0,0,0,0,0,1,1,0,1,1]]#,[1,1,0,0,1,1,1,1],[1,1,0,0,0,0,1,1],[1,1,0,1,0,1,0,1],[0,1,0,0,1,1,1,1],[0],[0,1,1,0,0,0,1,1,1]
# c1 = NTRU.encrypto(poly(message[0])) #
# c2 = NTRU.encrypto(poly(message[1])) #
# print('密文1：{}'.format(c1.coe))
# print('密文2：{}'.format(c2.coe))
#
# M1= NTRU.decrypto(c1)
# print('携带嵌入数据的明文：{}'.format(M1.coe))
# M2 = NTRU.decrypto(c2)
# print('携带嵌入数据的明文：{}'.format(M2.coe))

# c3 = c1.polyadd(c2,NTRU.q)
# M3=NTRU.decrypto(c3)
# print('携带嵌入数据的明文：{}'.format(M3.coe))
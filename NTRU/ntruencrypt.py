from poly import poly
from poly import can_not_div_Error
from poly import egcd
import random
def encode(Target_string):
	return ''.join([bin(ord(c)).replace('0b', '') for c in Target_string])
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
			return self._randpoly(15,14)
		elif self.N == 503:
			return self._randpoly(216,215)
		else :
			return self._randpoly()

	def randpoly_g(self):
		if self.N == 107:
			return self._randpoly(12,12)
		elif self.N == 503:
			return self._randpoly(72,72)
		else:
			return self._randpoly()

	def randpoly_phi(self):
		if self.N == 107:
			return self._randpoly(5,5)
		elif self.N == 503:
			return self._randpoly(5,5)
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
<<<<<<< Updated upstream
	def encrypto(self,m,flag):
		# phi = self.randpoly_phi()
		# phi2=self.randpoly_phi()
		# #phi = poly([-1,1,0,0,1,-1,1])
		# c = phi.StarMult(self.public_key,self.N,self.q)
		# c2 = phi2.StarMult(self.public_key,self.N,self.q)
		# #print('公钥是：{}'.format(self.public_key.coe))
		# c.expend(self.N)
		# c2.expend(self.N)
		# m.expend(self.N)
		# for i in range(0,self.N):
		# 	c.coe[i] = self.p * c.coe[i] + m.coe[i]
		# 	c.coe[i] %= self.q
		# 	c2.coe[i] = self.p * c.coe[i] + m.coe[i]
		# 	c2.coe[i] %= self.q
		# return c,c2
		phi = self.randpoly_phi()
		phi2 = self.randpoly_phi()
		# phi = poly([-1,1,0,0,1,-1,1])
		c = phi.StarMult(self.public_key, self.N, self.q)
		c2 = phi2.StarMult(self.public_key, self.N, self.q)
		total=0
=======
	def encrypto(self,m,phi,phi2):

		#phi = poly([-1,1,0,0,1,-1,1])
		c = phi.StarMult(self.public_key,self.N,self.q)
		c2 = phi2.StarMult(self.public_key,self.N,self.q)
		#print('公钥是：{}'.format(self.public_key.coe))
>>>>>>> Stashed changes
		c.expend(self.N)
		c2.expend(self.N)
		m.expend(self.N)
		for i in range(0, self.N):
			c.coe[i] = self.p * c.coe[i] + m.coe[i]
			c.coe[i] %= self.q
			c2.coe[i] = self.p * c.coe[i] + m.coe[i]
			c2.coe[i] %= self.q
		for index in c.coe:
			total+=index
		while (total%2)!=flag:
			phi = self.randpoly_phi()
			phi2 = self.randpoly_phi()
			# phi = poly([-1,1,0,0,1,-1,1])
			c = phi.StarMult(self.public_key, self.N, self.q)
			c2 = phi2.StarMult(self.public_key, self.N, self.q)
			total = 0

		# print('公钥是：{}'.format(self.public_key.coe))
			c.expend(self.N)
			c2.expend(self.N)
			m.expend(self.N)
			for i in range(0, self.N):
				c.coe[i] = self.p * c.coe[i] + m.coe[i]
				c.coe[i] %= self.q
				c2.coe[i] = self.p * c.coe[i] + m.coe[i]
				c2.coe[i] %= self.q
			for index in c.coe:
				total += index
		# print('total={}'.format(total))
		return c, c2
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

<<<<<<< Updated upstream
NTRU = ntru(41,2,13,Fp=poly([-1,0,1,1]),public_key=poly([1,2,0,-2,-1]),private_key=poly([-1,1,0,0,1]))
=======
NTRU = ntru(37,2,256,Fp=poly([-1,0,1,1]),public_key=poly([1,2,0,-2,-1]),private_key=poly([-1,1,0,0,1]))
>>>>>>> Stashed changes
NTRU.createKey_pair()
phi =NTRU.randpoly_phi()
phi2=NTRU.randpoly_phi()
print('私钥：{}'.format(NTRU.private_key.coe))
print('公钥：{}'.format(NTRU.public_key.coe))
<<<<<<< Updated upstream
#message=[[0,0,0,0,1,1,1,1],[1,1,0,0,1,1,1,1],[1,1,0,0,0,0,1,1],[1,1,0,1,0,1,0,1],[0,1,0,0,1,1,1,1],[1,1,0,1,1,0,1,1],[1,1,0,0,0,1,0,1],[1,1,0,0,1,1,1,1]]
#message=[[0],[0],[0],[0],[1],[1],[1],[1]]#明文使用1bit也行
message=input('Enter PlainText:')
message=encode(message)#转换为二进制
print(message)
print(type(message))
for i in message:
	i=int(i)
print(message)
flag=0
addtionData = input("Enter Message: ")
data=encode(addtionData)
print(data)
len=min(len(message),len(data))
index=0
I=list()
while index<len:

	#binary=bin(int(ord(j),10))
	#print(binary)
	flag=int(data[index])
	print(flag)
	c,c2 = NTRU.encrypto(poly(message[index]),flag) #
	print('密文{}：{}'.format(index+1,c.coe))
	# print('密文2：{}'.format(c2.coe))

	# c.coe[1] += 1
	# c.coe[0] += 1
	# c.coe[2]+=1
=======
message=[[0,0,0,0,0,1,1,1],[0,0,0,0,0,1,0,0],[0,0,0,0,0,1,0,1]]
for i in message:
	c,c2 = NTRU.encrypto(poly(i),phi,phi2) #

	print('密文1：{}'.format(c.coe))
	# print('密文2：{}'.format(c2.coe))
	#
	# c.coe[1] += 1
	# c.coe[0] += 1
>>>>>>> Stashed changes
	# c3 = c2.polysub(c)
	#
	# print('嵌入数据后的密文：{}'.format(c.coe))
	# print('密文差值：{}'.format(c3.coe))
<<<<<<< Updated upstream
	# M = NTRU.decrypto(c)
	# M2 = NTRU.decrypto(c2)
	# M3=NTRU.decrypto(c3)
	# M3.expend(8)
	# print('携带嵌入数据的明文：{}'.format(M.coe))
	# print('明文：{}'.format(M2.coe))
	# print('差值对应的明文：{}'.format(M3.coe))
	#print('密文1对应的明文：{}'.format(M.coe))
	total=0
	for index1 in c.coe:
		total+=index1
	if total%2==0:
		print('携带的数据为0')
		I.append('0')
	else:
		print('携带的数据为1')
		I.append('1')
	index+=1
	# print('密文2对应的明文：{}'.format(M2.coe))
str1="".join(I)
print(str1)
=======
	M = NTRU.decrypto(c)

	while len(M.coe)<8:
		M.coe.append(0)
	# M.expend(len(i))
	# M2=NTRU.decrypto(c2)
	# M3=NTRU.decrypto(c3)
	# M3.expend(len(i))
	print('明文：{}'.format(M.coe))
	# print('携带嵌入数据的明文：{}'.format(M.coe))
	# print('明文：{}'.format(M2.coe))
	# print('差值对应的明文：{}'.format(M3.coe))
>>>>>>> Stashed changes

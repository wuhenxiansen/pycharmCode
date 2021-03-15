from poly import poly
from poly import can_not_div_Error
from poly import egcd
import re
import random
def encode(Target_string):
	str=''
	for c in Target_string:
		str1=bin(ord(c)).replace('0b', '')
		if len(str1)<7:
			str1='0'+str1
		str+=str1
	#return ''.join([bin(ord(c)).replace('0b', '') for c in Target_string])
	return str
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
		cnt=1
		phi = self.randpoly_phi()
		#phi2 = self.randpoly_phi()
		# phi = poly([-1,1,0,0,1,-1,1])
		c = phi.StarMult(self.public_key, self.N, self.q)
		#c2 = phi2.StarMult(self.public_key, self.N, self.q)
		total=0
		c.expend(self.N)
		#c2.expend(self.N)
		m.expend(self.N)
		for i in range(0, self.N):
			c.coe[i] = self.p * c.coe[i] + m.coe[i]
			c.coe[i] %= self.q
			# c2.coe[i] = self.p * c.coe[i] + m.coe[i]
			# c2.coe[i] %= self.q
		for index in c.coe:
			total+=index
		#print('运行第{}次'.format(cnt))
		while (total%2)!=flag:
			phi = self.randpoly_phi()
			#phi2 = self.randpoly_phi()
			# phi = poly([-1,1,0,0,1,-1,1])
			c = phi.StarMult(self.public_key, self.N, self.q)
			# c2 = phi2.StarMult(self.public_key, self.N, self.q)
			total = 0
			cnt+=1
			#print('运行第{}次'.format(cnt))
		# print('公钥是：{}'.format(self.public_key.coe))
			c.expend(self.N)
			# c2.expend(self.N)
			m.expend(self.N)
			for i in range(0, self.N):
				c.coe[i] = self.p * c.coe[i] + m.coe[i]
				c.coe[i] %= self.q
				# c2.coe[i] = self.p * c.coe[i] + m.coe[i]
				# c2.coe[i] %= self.q
			for index in c.coe:
				total += index
		# print('total={}'.format(total))
		#return c, c2
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
NTRU = ntru(17, 3, 512, Fp=poly([-1, 0, 1, 1]), public_key=poly([1, 2, 0, -2, -1]),private_key=poly([-1, 1, 0, 0, 1]))
NTRU.createKey_pair()
def Owner(data):

	print('Public Key：{}'.format(NTRU.private_key.coe))
	print('Private Key：{}'.format(NTRU.public_key.coe))
	# message=[[0,0,0,0,1,1,1,1],[1,1,0,0,1,1,1,1],[1,1,0,0,0,0,1,1],[1,1,0,1,0,1,0,1],[0,1,0,0,1,1,1,1],[1,1,0,1,1,0,1,1],[1,1,0,0,0,1,0,1],[1,1,0,0,1,1,1,1]]
	# message=[[0],[0],[0],[0],[1],[1],[1],[1]]#明文使用1bit也行
	message = input('Enter PlainText:')
	message = encode(message)  # 转换为二进制
	print('It\'s Binary code:'+message)
	plainText = list()
	for i in message:
		i = int(i)
		temp = list()
		temp.append(i)
		plainText.append(temp)
	#print(plainText)
	length = len(message)
	index = 0
	C = list()
	while index<length:
		#binary=bin(int(ord(j),10))
		#print(binary)
		if index<len(data):
			flag=int(data[index])
		else:
			flag=random.randint(0,1)
		#print('flag is {}'.format(flag))
		c= NTRU.encrypto(poly(plainText[index]),flag) #得到密文
		C.append(c)
		index+=1
	return C
def Receiver(C,length):
	P=list()
	I=list()
	index=0
	print('Have the private key?')
	choice = input('Input \'Y\' or \'N\':')
	if (choice == 'Y'):
		for c in C:
			M = NTRU.decrypto(c)
			P.append(str(M.coe[0]))
			if index < length:
				total = 0
				for index1 in c.coe:
					total += index1
				if total % 2 == 0:
					I.append('0')
				else:
					I.append('1')
			index+=1
		str1 = "".join(I)
		print('	Additional data\'s Binary code:{}'.format(str1))
		bb = re.findall(r'.{7}', str1)
		str2 = ""
		for b in bb:
			str2 += chr(int(b, 2))
		print('	The secret additonal data:{}'.format(str2))

		print('----------------------')
		str3 = "".join(P)
		print('	Plaintext\'s Binary code:{}'.format(str3))
		cc = re.findall(r'.{7}', str3)
		str4 = ""
		for b in cc:
			str4 += chr(int(b, 2))
		print('	PlainText:{}'.format(str4))
	else:
		for c in C:
			if index < length:
				total = 0
				for index1 in c.coe:
					total += index1
				if total % 2 == 0:
					I.append('0')
				else:
					I.append('1')
				index+=1
		str1 = "".join(I)
		print(' Additional data\'s Binary code:{}'.format(str1))
		bb = re.findall(r'.{7}', str1)
		str2 = ""
		for b in bb:
			str2 += chr(int(b, 2))
		print('The secret additonal data:{}'.format(str2))
def main():
	#NTRU = ntru(17,2,256,Fp=poly([-1,0,1,1]),public_key=poly([1,2,0,-2,-1]),private_key=poly([-1,1,0,0,1]))
	flag=0
	addtionData = input("Enter AdditionalData: ")
	data = encode(addtionData)
	print('It\'s Binary code:'+data)
	length=len(data)
	C=Owner(data)
	Receiver(C,length)

if __name__ == '__main__':
    main()
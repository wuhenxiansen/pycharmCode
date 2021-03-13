from poly import poly
from poly import can_not_div_Error
from poly import egcd
import re
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
	def encrypto(self,m):
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
NTRU = ntru(91, 3, 256, Fp=poly([-1, 0, 1, 1]), public_key=poly([1, 2, 0, -2, -1]),private_key=poly([-1, 1, 0, 0, 1]))
NTRU.createKey_pair()
def Owner():

	print('Public Key：{}'.format(NTRU.private_key.coe))
	print('Private Key：{}'.format(NTRU.public_key.coe))
	# message=[[0,0,0,0,1,1,1,1],[1,1,0,0,1,1,1,1],[1,1,0,0,0,0,1,1],[1,1,0,1,0,1,0,1],[0,1,0,0,1,1,1,1],[1,1,0,1,1,0,1,1],[1,1,0,0,0,1,0,1],[1,1,0,0,1,1,1,1]]
	# message=[[0],[0],[0],[0],[1],[1],[1],[1]]#明文使用1bit也行
	print('\tOwner Process:')
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
		c= NTRU.encrypto(poly(plainText[index])) #得到密文
		C.append(c)
		index+=1
	return C
def DataHider(C):
	print('\tDataHider Process:')
	addtionData = input("Enter the data to be embedded: ")
	data = encode(addtionData)
	print(data)
	I = list()
	P = list()
	index=0
	length=len(C)#密文长度
	length2=len(data)#隐藏字符长度
	#设置前16比特用于表示嵌入数据长度
	Binlen2=encode(chr(length2))
	while len(Binlen2)<16:
		Binlen2='0'+Binlen2
	data=Binlen2+data
	while index < length:
		#c = NTRU.encrypto(poly(plainText[index]))  #
		#M = NTRU.decrypto(C[index])
		# print('密文对应的明文：{}'.format(M.coe))
		M=NTRU.decrypto(C[index])
		O=M
		if index < len(data):
			total = 0
			for index1 in C[index].coe:
				total += index1
			while total % 2 != int(data[index]):
				# print(c.coe)
				# 数据隐藏者对密文进行处理转换密文，使密文符合条件以表示某数据
				# 密文  e(x)=p*h(x)*r(x)+m(x)   对于密文再加上p*一个多项式，最后mod p 结果仍然不变
				phi = NTRU.randpoly_phi()
				phi.expend(NTRU.N)
				# r = phi.StarMult(NTRU.public_key, NTRU.N, NTRU.q)
				# r.expend(NTRU.N)
				# c2.expend(self.N)
				for i in range(0, NTRU.N):
					#print('index={},i={}'.format(index,i))
					C[index].coe[i] += NTRU.p * phi.coe[i]
					C[index].coe[i] %= NTRU.q
				M = NTRU.decrypto(C[index])
				#print('密文1对应的明文：{}'.format(M.coe))
				total = 0
				for index1 in C[index].coe:
					total += index1
		index += 1
	print('Data embedding completed!')
	return C
def Receiver(C):
	print('\tDataHider Process:')
	cnt=0
	P=list()
	A=list()

	choice=input('Input \'Y\' or \'N\':')
	Binary = 0
	index = 0
	for c in C:
		#print(c.coe)
		cnt += 1
		total = 0


		for index1 in c.coe:
			total += index1
		if cnt<=16:
			Binary=Binary*2+(total%2)
		else :
			if index<Binary:
				A.append(str(total%2))
				index+=1
		if choice=='Y':
			m=NTRU.decrypto(c)
			P.append(str(m.coe[0]))
	# print('adddata:{}'.format(A))
	# print('data:{}'.format(P))
	str1=''.join(A)
	bb = re.findall(r'.{7}', str1)
	secretData = ""
	for b in bb:
		secretData += chr(int(b, 2))
	print('Extract the data')
	if choice=='Y':
		str2 = ''.join(P)
		bb = re.findall(r'.{7}', str2)
		PlainText = ""
		for b in bb:
			PlainText += chr(int(b, 2))
		print('The PlainText:{}'.format(PlainText))
		print('The secret additonal data:{}'.format(secretData))
	else:
		print('The secret additonal data:{}'.format(secretData))

def main():
	C=Owner()
	C=DataHider(C)
	Receiver(C)
if __name__ == '__main__':
    main()
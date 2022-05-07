from poly import poly
from poly import can_not_div_Error
from poly import egcd
import re
import time
import random
import sys
def encode(Target_string):
	str=''
	for c in Target_string:
		str1=bin(ord(c)).replace('0b', '')
		while len(str1)<7:
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
			pos = random.randint(0,self.N - 1)#随机生成1 -1
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
		if self.N == 167:
			return self._randpoly(61,60)
		elif self.N == 503:
			return self._randpoly(216,215)
		else :
			return self._randpoly()
	def randpoly_g(self):
		if self.N == 107:
			return self._randpoly(12,12)
		elif self.N == 167:
			return self._randpoly(20,20)
		elif self.N == 503:
			return self._randpoly(72,72)
		else:
			return self._randpoly()
	def randpoly_phi(self):
		if self.N == 107:
			return self._randpoly(5,5)
		if self.N == 167:
			return self._randpoly(18,18)
		elif self.N == 503:
			return self._randpoly(55,55)
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
NTRU = ntru(167, 3, 256, Fp=poly([-1, 0, 1, 1]), public_key=poly([1, 2, 0, -2, -1]),private_key=poly([-1, 1, 0, 0, 1]))
NTRU.createKey_pair()
def Owner():

	#print('Public Key：{}'.format(NTRU.private_key.coe))
	#print('Private Key：{}'.format(NTRU.public_key.coe))
	print('\t数据拥有者加密过程:\n')
	print('\t读取明文文本:\n')
	message=''
	with open(file='plainText.txt',mode='r') as f:
		datas=f.readlines()
	for d in datas:
		message+=d
	print(message)
	plainText = list()
	for m in message:
		m=encode(m)
		temp = list()
		for bi in m:
			bi=int(bi)
			temp.append(bi)
		plainText.append(temp)
	print(plainText)
	length = len(message)
	index = 0
	C = list()
	encryptData=''#密文串
	while index<length:
		c= NTRU.encrypto(poly(plainText[index])) #得到密文
		C.append(c)
		for ch in c.coe:
			encryptData+=chr(ch)
		index+=1
	#print(encryptData)
	out=sys.stdout
	sys.stdout=open('ciphertext.txt','w',encoding='utf-8')
	print(encryptData)
	sys.stdout.close()
	sys.stdout=out
	return C
def DataHider(C):
	# t=input('输入t:')
	# s=input('输入s:')
	# t=int(t)
	# s=int(s)
	t=60
	s=60

	print('\t数据隐藏者嵌入数据过程:\n')

	# AdL1=input("输入待嵌入的数据1长度: ")
	# addtionData1=''
	# for i in range(0,int(AdL1)):
	# 	addtionData1 += random.choice('0123456789abcdefghijklmnopqrstuvwxyz!@#$%^&*()')
	with open(file='data1.txt',mode='r') as f:
		addtionData1=f.read()
	print('隐藏数据1：{}'.format(addtionData1))
	data1 = encode(addtionData1)

	#print('It\'s Binary code:{}'.format(data1))
	#处理二进制串
	# AdL2 = input("输入待嵌入的数据2长度: ")
	# addtionData2 = ''
	# for i in range(0, int(AdL2)):
	# 	addtionData2 += random.choice('0123456789abcdefghijklmnopqrstuvwxyz!@#$%^&*()')
	with open(file='data2.txt',mode='r') as f:
		addtionData2=f.read()
	print('隐藏数据2：{}'.format(addtionData2))

	data2 = encode(addtionData2)
	start = time.process_time()
	length=len(C)#密文长度
	length1=len(data1)#第一阶段总隐藏字符长度
	Binlen1 = bin(length1).replace('0b','')
	while len(Binlen1) < 24:
		Binlen1 = '0' + Binlen1
	cnt = 0
	index = 0
	#隐藏第一阶段数据
	while index<length:
		if cnt>=length1:
			break
		index1=0
		while index1<t:
			if cnt >= length1:
				break
			if cnt < length1:
				C[index].coe[index1+7]+=int(data1[cnt])
				C[index].coe[index1+7] %= NTRU.q
				cnt+=1
			index1+=1
		index+=1
	print('\t第一阶段数据嵌入完毕!\n')

	length2 = len(data2)  # 第二阶段总隐藏字符长度
	Binlen2 = bin(length2).replace('0b','')
	while len(Binlen2) < 24:
		Binlen2 = '0' + Binlen2
	# 隐藏第二阶段数据
	cnt=0
	index=0
	while index < length:
		if cnt >= length2:
			break
		index1 = 0
		while index1 < s:
			if cnt >= length2:
				break
			if cnt < length2:
				if C[index].coe[index1 + t+7]%2!=int(data2[cnt]):
					C[index].coe[index1 + t+7] +=1
					C[index].coe[index1 + t+7] %= NTRU.q
				cnt += 1
			index1 += 1
		index += 1
	#在最后一个像素点中隐藏数据表示嵌入数据的长度
	index1 = 0
	for i in range(0,24):
		if C[length - 1].coe[i + 7] % 2 != int(Binlen1[i]):
			C[length - 1].coe[i + 7] += 1
			C[length - 1].coe[i + 7] %= NTRU.q
		if C[length - 1].coe[i + 7+24]%2!=int(Binlen2[i]):
			C[length - 1].coe[i + 7+24] +=1
			C[length - 1].coe[i + 7+24] %= NTRU.q

	print('\t第二阶段数据嵌入完毕!\n')
	end=time.process_time()
	print('两个阶段总嵌入时间为{}'.format(end-start))

	return C,t,s
def Receiver(C,t,s):


	print('\t数据提取者提取数据过程:\n')

	message1=list()
	P = list()
	A = list()
	A2 = list()
	#第二阶段嵌入数据提取
	#先提取隐藏数据长度的信息
	L2 = ''
	L1 = ''
	for i in range(0,24):
		L2 += str(C[len(C)-1].coe[i + 7+24]%2)
		L1 += str(C[len(C)-1].coe[i + 7]%2)
	ad1Len = int(L1, 2)
	ad2Len = int(L2, 2)
	for c in C:
		for i in range(0,s):
			if ad2Len > 0:
				A2.append(str(c.coe[i+t+7]%2))
				ad2Len-=1
	for c in C:
		m1=NTRU.decrypto(c)
		m1.expend(NTRU.N)
		message1.append(m1.coe)

	for me in message1:
		for j in range(0,7):
			P.append(str(me[j]))
		for i in range(0,s):
			if ad1Len >0:
				A.append(str(me[7+i]))
				ad1Len-=1;

	str1=''.join(P)
	bb1=re.findall(r'.{7}', str1)
	PlainText = ""
	print(bb1)
	for b1 in bb1:
		PlainText+=chr(int(b1,2))
	print('原始载体数据:')
	print(PlainText)
	out = sys.stdout
	sys.stdout = open('recoverPlaintext.txt', 'w')
	print(PlainText)
	sys.stdout.close()
	sys.stdout = out
	str2 = ''.join(A)
	bb = re.findall(r'.{7}', str2)
	secretData1 = ""
	for b in bb:
		secretData1 += chr(int(b, 2))
	print('第一阶段隐藏数据:')
	print(secretData1)
	out = sys.stdout
	sys.stdout = open('recoverData1.txt', 'w')
	print(secretData1)
	sys.stdout.close()
	sys.stdout = out
	str3 = ''.join(A2)
	bb = re.findall(r'.{7}', str3)
	secretData2 = ""
	for b in bb:
		secretData2 += chr(int(b, 2))
	out = sys.stdout
	sys.stdout = open('recoverData2.txt', 'w')
	print(secretData2)
	sys.stdout.close()
	sys.stdout = out
	print('第二阶段隐藏数据:')
	print(secretData2)


def main():
	encryptData=Owner()
	# print('加密载体数据：')
	# print(encryptData)
	encryptData2,t,s=DataHider(encryptData)
	# print('携带隐藏数据的加密载体数据：')
	# print(encryptData2)
	Receiver(encryptData2,t,s)
if __name__ == '__main__':
    main()
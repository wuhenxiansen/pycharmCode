from poly import poly
from poly import can_not_div_Error
from poly import egcd
import re
import time
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
			return self._randpoly(9, 8)
		elif self.N == 167:
			return self._randpoly(11, 10)
		elif self.N == 503:
			return self._randpoly(11, 10)
		else:
			return self._randpoly()

	def randpoly_g(self):
		if self.N == 107:
			return self._randpoly(8, 8)
		elif self.N == 167:
			return self._randpoly(10, 10)
		elif self.N == 503:
			return self._randpoly(10, 10)
		else:
			return self._randpoly()

	def randpoly_phi(self):
		if self.N == 107:
			return self._randpoly(5, 5)
		elif self.N == 167:
			return self._randpoly(11, 11)
		elif self.N == 503:
			return self._randpoly(11, 11)
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
		print('公钥：{}'.format(h.coe))
		print('私钥：{}'.format(self.private_key.coe))
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
		#print('密文：{}'.format(c.coe))
		return c
	def decrypto(self,m):
		a = self.private_key.StarMult(m,self.N,self.q)
		#print('a.coe:{}'.format(a.coe))
		#print('私钥是：{}'.format(self.private_key.coe))
		for i in range(0,len(a.coe)):
			if a.coe[i] < 0:
				a.coe[i] += self.q
			if a.coe[i] > self.q / 2:
				a.coe[i] = a.coe[i] - self.q
		#print('a.coe:{}'.format(a.coe))
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
	LS = input('输入原始载体字符串长度:')
	# message=''
	# for i in range(0,int(LS)):
	# 	message += random.choice('0123456789abcdefghijklmnopqrstuvwxyzQWERTYUIOPASDFGHJKLZXCVBNM!@#$%^&*()')
	#print(message)
	message=[]
	for i in range(0, int(LS)):
		message.append(random.randint(0,255))
	print(message)
	plainText = list()
	for m in message:
		#m=encode(m)
		m=bin(m).replace('0b', '')
		temp = list()
		for bi in m:
			bi=int(bi)
			temp.append(bi)
		plainText.append(temp)
	#print(plainText)
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
	return encryptData
def DataHider(encryptdata,lenB):
	t=input('输入t:')
	#s=input('输入s:')
	t=int(t)
	#s=int(s)
	C=list()
	count=1
	c=list()
	for ch in encryptdata:
		c.append(ord(ch))
		if(count%NTRU.N==0):
			C.append(poly(c))
			c=list()
		count+=1
	print('\t数据隐藏者嵌入数据过程:\n')
	AdL1=input("输入待嵌入的数据1长度: ")
	addtionData1=''
	for i in range(0,int(AdL1)):
		addtionData1 += random.choice('0123456789abcdefghijklmnopqrstuvwxyzQWERTYUIOPSDFGHJKLXCVBNM!@#$%^&*()')
	print('隐藏数据1：{}'.format(addtionData1))
	data1 = encode(addtionData1)

	#print('It\'s Binary code:{}'.format(data1))
	#处理二进制串
	newdata = list()
	AdL2 = input("输入待嵌入的数据2长度: ")
	addtionData2 = ''
	for i in range(0, int(AdL2)):
		addtionData2 += random.choice('0123456789abcdefghijklmnopqrstuvwxyzQWERTYUIOPASDFGHJKLXCVBNM!@#$%^&*()')
	print('隐藏数据2：{}'.format(addtionData2))

	data2 = encode(addtionData2)
	#print(data2)
	start = time.process_time()
	length=len(C)#密文长度
	length1=len(data1)#第一阶段总隐藏字符长度
	Binlen1 = bin(length1).replace('0b','')
	while len(Binlen1) < 24:
		Binlen1 = '0' + Binlen1
	#将隐藏数据的二进制流分为2^lenB为一组
	tmp = ''
	for i in range(0, len(data2)):

		if i>=lenB and i % lenB == 0:
			newdata.append(tmp)
			tmp = ''
		tmp += data2[i]
	if tmp != '':
		newdata.append(tmp)
	#print(newdata)
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

	length2 = len(newdata)  # 第二阶段总隐藏字符长度
	length22=len(data2)
	Binlen2 = bin(length22).replace('0b','')
	while len(Binlen2) < 24:
		Binlen2 = '0' + Binlen2
	# 隐藏第二阶段数据
	#嵌入nbit数据
	cnt=0
	index=0
	while index < length:#length 密文c长度
		#print('嵌入前：',C[index].coe)
		if cnt >= length2:
			break
		index1 = 0
		while index1 < NTRU.N:
			if cnt >= length2:
				break
			if cnt < length2:
				sum=0
				for i in newdata[cnt]:
					sum=sum*2+int(i)
				if C[index].coe[index1]%int(pow(2,lenB))!=sum:
					i=0
					while C[index].coe[index1]+NTRU.p*i<256:
						if (C[index].coe[index1]+NTRU.p*i)%int(pow(2,lenB))==sum:
							C[index].coe[index1] += NTRU.p*i
							break
						i+=1
				if C[index].coe[index1]%int(pow(2,lenB))!=sum:
					i=0
					while C[index].coe[index1]-NTRU.p*i>=0:
						if (C[index].coe[index1]-NTRU.p*i)%int(pow(2,lenB))==sum:
							C[index].coe[index1] -= NTRU.p*i
							break
						i+=1
				cnt += 1
			index1 += 1
		#print('嵌入后：',C[index].coe)
		index += 1
	#在最后一个像素点中隐藏数据表示嵌入数据的长度
	index1 = 0
	for i in range(0,24):
		if C[length - 1].coe[i ] % 2 != int(Binlen1[i]):
			C[length - 1].coe[i ] += NTRU.p
			C[length - 1].coe[i ] %= NTRU.q
		if C[length - 1].coe[i +24]%2!=int(Binlen2[i]):
			C[length - 1].coe[i+24] +=NTRU.p
			C[length - 1].coe[i +24] %= NTRU.q

	print('\t第二阶段数据嵌入完毕!\n')
	end=time.process_time()
	print('两个阶段总嵌入时间为{}'.format(end-start))
	encryptData2=''
	for c in C:
		for ch in c.coe:
			encryptData2+=chr(ch)
	return encryptData2,t
def Receiver(encryptData2,t,lenB):
	C = list()
	count = 1
	c = list()
	for ch in encryptData2:
		c.append(ord(ch))
		if (count % NTRU.N == 0):
			C.append(poly(c))
			c = list()
		count += 1
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
		L2 += str(C[len(C)-1].coe[i +24]%2)
		L1 += str(C[len(C)-1].coe[i ]%2)
	ad1Len = int(L1, 2)
	ad2Len = int(L2, 2)
	fl=0
	#先提取第二阶段隐藏数据
	for c in C:
		if fl==1:
			break
		for i in range(0,NTRU.N):
			if ad2Len > lenB:
				str2 = bin(c.coe[i] % int(pow(2,lenB))).replace('0b', '')
				if len(str2) < lenB :
					while len(str2)<lenB:
						str2 = '0' + str2
				A2.append(str2)
				ad2Len -= lenB
			else:
				#处理最后的字符
				str2 = bin(c.coe[i] % int(pow(2, lenB))).replace('0b', '')
				if len(str2) < ad2Len:
					while len(str2) < ad2Len:
						str2 = '0' + str2
				A2.append(str2)
				ad2Len -= len(str2)
				fl=1
				break
	str3 = ''.join(A2)
	bb = re.findall(r'.{7}', str3)
	secretData2 = ""
	for b in bb:
		secretData2 += chr(int(b, 2))
	print('第二阶段隐藏数据:')
	print(secretData2)
	#提取第一阶段数据
	for c in C:
		m1=NTRU.decrypto(c)
		m1.expend(NTRU.N)
		message1.append(m1.coe)

	for me in message1:
		for j in range(0,7):
			P.append(str(me[j]))
		for i in range(0,t):
			if ad1Len >0:
				A.append(str(me[7+i]))
				ad1Len-=1;

	str1=''.join(P)
	bb1=re.findall(r'.{7}', str1)
	PlainText = ""
	for b1 in bb1:
		PlainText+=chr(int(b1,2))
	print('原始载体数据:')
	print(PlainText)
	str2 = ''.join(A)
	bb = re.findall(r'.{7}', str2)
	secretData1 = ""
	for b in bb:
		secretData1 += chr(int(b, 2))
	print('第一阶段隐藏数据:')
	print(secretData1)




def main():
	encryptData=Owner()
	# print('加密载体数据：')
	# print(encryptData)
	lenB=int(input("输入一个系数隐藏的位数："))
	encryptData2,t=DataHider(encryptData,lenB)
	# print('携带隐藏数据的加密载体数据：')
	# print(encryptData2)
	Receiver(encryptData2,t,lenB)
if __name__ == '__main__':
    main()
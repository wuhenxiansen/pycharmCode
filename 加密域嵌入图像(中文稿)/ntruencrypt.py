from poly import poly
from poly import can_not_div_Error
from poly import egcd
import cv2
import numpy as np
import re
import time
import random
import matplotlib.pyplot as plt
import numpy as np
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
		#c2.expend(self.N)c
		m.expend(self.N)
		for i in range(0, self.N):
			c.coe[i] = self.p * c.coe[i] + m.coe[i]
			c.coe[i] %= self.q
			if c.coe[i] > self.q // 2:
				c.coe[i] -= self.q
			if c.coe[i] <= -self.q // 2:
				c.coe[i] += self.q
		#print('密文：{}'.format(c.coe))
		return c
	def decrypto(self,m):
		a = self.private_key.StarMult(m,self.N,self.q)
		#print('a.coe:{}'.format(a.coe))
		#print('私钥是：{}'.format(self.private_key.coe))
		for i in range(0,len(a.coe)):
			if a.coe[i] < -self.q / 2:
				a.coe[i] += self.q
			if a.coe[i] > self.q / 2:
				a.coe[i] = a.coe[i] - self.q
		#print('a.coe:{}'.format(a.coe))
		M = a.StarMult(self.Fp,self.N,self.p).polydiv(self.P,self.p)[1]
		return M
"""
TEST
"""
NTRU = ntru(503, 3, 256, Fp=poly([-1, 0, 1, 1]), public_key=poly([1, 2, 0, -2, -1]),private_key=poly([-1, 1, 0, 0, 1]))
NTRU.createKey_pair()
def Owner():

	#print('Public Key：{}'.format(NTRU.private_key.coe))
	#print('Private Key：{}'.format(NTRU.public_key.coe))
	print('\t数据拥有者加密过程:\n')
	image = cv2.imread(r"03.png", cv2.IMREAD_GRAYSCALE)  # 以灰度模式加载图片
	# print(image)
	rows, cols = image.shape[:2]
	pixel_count = rows * cols
	image_array = image.reshape(1, pixel_count)[0]
	#print(image_array)
	LS = pixel_count
	print(LS)
	message=[]
	for i in range(0,LS):
		message.append(image_array[i])
	plainText = list()
	for m in message:
		m=bin(m).replace('0b', '')
		if len(m)<8:
			m=(8-len(m))*'0'+m
		temp = list()
		for bi in m:
			bi=int(bi)
			temp.append(bi)
		plainText.append(temp)
	#print(plainText)
	length = len(message)
	index = 0
	C = list()
	#encryptData=''#密文串
	while index<length:
		if index%1000==0:
			print(index)
		c= NTRU.encrypto(poly(plainText[index])) #得到密文

		C.append(c)
		# for ch in c.coe:
		# 	encryptData+=chr(ch)
		index+=1
	return C,rows,cols
def DataHider(C,t,s):

	print('\t数据隐藏者嵌入数据过程:\n')

	secrectimage1 = cv2.imread(r"11.png", cv2.IMREAD_GRAYSCALE)  # 以灰度模式加载图片

	rows1, cols1 = secrectimage1.shape[:2]
	pixel_count = rows1 * cols1
	secrectimage_array = secrectimage1.reshape(1, pixel_count)[0]

	AdL1 = pixel_count
	message1 = []
	for i in range(0, AdL1):
		message1.append(secrectimage_array[i])
	data1 = ''
	for m in message1:
		m = bin(m).replace('0b', '')
		if len(m) < 8:
			m = (8 - len(m)) * '0' + m
		data1 +=m

	#print('It\'s Binary code:{}'.format(data1))
	#处理二进制串
	secrectimage2 = cv2.imread(r"12.png", cv2.IMREAD_GRAYSCALE)  # 以灰度模式加载图片

	rows2, cols2 = secrectimage2.shape[:2]
	pixel_count = rows2 * cols2
	secrectimage2_array = secrectimage2.reshape(1, pixel_count)[0]

	AdL2 = pixel_count
	message2 = []
	for i in range(0, AdL2):
		message2.append(secrectimage2_array[i])
	data2 = ''
	for m in message2:
		m = bin(m).replace('0b', '')
		if len(m) < 8:
			m = (8 - len(m)) * '0' + m
		data2 += m
	#print(data2)
	start = time.process_time()
	length=len(C)#密文长度
	length1=len(data1)#第一阶段隐藏数据总二进制位长度
	Binlen1 = bin(length1).replace('0b','')
	print('字符长度:{},编码：{}'.format(length1,Binlen1))
	while len(Binlen1) < 32:
		Binlen1 = '0' + Binlen1
	#将隐藏数据的二进制流分为2^lenB为一组
	print(Binlen1)

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
				C[index].coe[index1+8]+=int(data1[cnt])
				C[index].coe[index1+8] %= NTRU.q
				cnt+=1
			index1+=1
		index+=1
	print('\t第一阶段数据嵌入完毕!\n')


	length2=len(data2)
	Binlen2 = bin(length2).replace('0b', '')
	while len(Binlen2) < 32:
		Binlen2 = '0' + Binlen2
	# 隐藏第二阶段数据
	#嵌入nbit数据
	print('字符长度:{},编码：{}'.format(length2, Binlen2))
	print(Binlen2)
	cnt=0
	index=0
	while index < length:#length 密文c长度
		#print('嵌入前：',C[index].coe)
		if cnt >= length2:
			break
		index1 = 0
		while index1 < s:
			if cnt >= length2:
				break
			if cnt < length2:
				if C[index].coe[index1 + t + 8] % 2 != int(data2[cnt]):
					C[index].coe[index1 + t + 8] += 1
					C[index].coe[index1 + t + 8] %= NTRU.q
				cnt += 1
			index1 += 1
		#print('嵌入后：',C[index].coe)
		index += 1
	#在最后一个像素点中隐藏数据表示嵌入数据的长度
	index1 = 0
	for i in range(0,32):
		if C[length - 1].coe[i+8 ] % 2 != int(Binlen1[i]):
			C[length - 1].coe[i+8 ] += NTRU.p
			C[length - 1].coe[i+8 ] %= NTRU.q
		if C[length - 1].coe[i +8+32]%2!=int(Binlen2[i]):
			C[length - 1].coe[i+8+32] +=NTRU.p
			C[length - 1].coe[i +8+32] %= NTRU.q

	print('\t第二阶段数据嵌入完毕!\n')
	end=time.process_time()
	print("两阶段总耗时:{}".format(end-start))

	return C,rows1,cols1,rows2,cols2,end-start
def Receiver(C,t,s,rows,cols,rows1,cols1,rows2,cols2):

	print('\t数据提取者提取数据过程:\n')
	message1=list()
	P = list()
	A = list()
	A2 = list()
	#第二阶段嵌入数据提取
	#先提取隐藏数据长度的信息
	L2 = ''
	L1 = ''
	for i in range(0,32):
		L2 += str(C[len(C)-1].coe[i +8+32]%2)
		L1 += str(C[len(C)-1].coe[i +8]%2)
	print(L1)
	print(L2)
	ad1Len = int(L1, 2)
	ad2Len = int(L2, 2)
	print('第二阶段数据长度：{}'.format(ad2Len))
	fl=0
	#先提取第二阶段隐藏数据
	for c in C:
		for i in range(0, s):
			if ad2Len > 0:
				A2.append(str(c.coe[i + t + 8] % 2))
				ad2Len -= 1
	str3 = ''.join(A2)
	ll=len(str3)
	print(ll)
	bb = re.findall(r'.{8}', str3)
	print(len(bb))
	secretData2 = np.zeros((1, len(bb)))
	index = 0
	for b1 in bb:
		secretData2[0, index] = int(b1, 2)
		index += 1
	print('第二阶段隐藏数据:')
	new_image1 = secretData2.reshape(rows2, cols2)
	# cv2.imshow("result080035", new_image)
	cv2.imwrite("secretImage2-t=200-12.png", new_image1)
	#提取第一阶段数据
	ii=0
	for c in C:
		if ii%1000==0:
			print(ii)
		m1=NTRU.decrypto(c)
		if 2 in m1.coe:
			print('密文：{}'.format(c.coe))
			print('明文：{}'.format(m1.coe))
		m1.expend(NTRU.N)
		message1.append(m1.coe)
		ii+=1
	flag=0
	for me in message1:
		for j in range(0,8):
			P.append(str(me[j]))
		if flag==0:
			for i in range(0,t):
				if ad1Len >0:
					A.append(str(me[8+i]))
					ad1Len-=1;
				else:
					flag=1
					break

	str1=''.join(P)
	#print(str1)
	bb1=re.findall(r'.{8}', str1)
	PlainText = np.zeros((1, len(C)))
	index=0
	for b1 in bb1:
		PlainText[0,index]=int(b1, 2)
		index+=1
	#print(PlainText[0])
	str2 = ''.join(A)
	bb2 = re.findall(r'.{8}', str2)
	secretData1 = np.zeros((1, len(bb2)))
	index = 0
	for b1 in bb2:
		secretData1[0, index] = int(b1, 2)
		index += 1
	print('第一阶段隐藏数据:')
	new_image2 = secretData1.reshape(rows1, cols1)
	# cv2.imshow("result080035", new_image)
	cv2.imwrite("secretImage1-t=200-11.png", new_image2)

	print('原始载体数据:')
	new_image = PlainText.reshape(rows,cols)
	#cv2.imshow("result080035", new_image)
	cv2.imwrite("result-t=200-03.png", new_image)

def main():
	C,rows,cols=Owner()#原始图像的行列等信息可以一并加密，这里为了后续处理方便直接传递给后面的函数使用

	C2,rows1,cols1,rows2,cols2,used_time=DataHider(C,200,200)#隐藏图像的行列信息可以用第二阶段方法进行隐藏，同上为了方便这里直接返回出来

	Receiver(C2,200,200,rows,cols,rows1,cols1,rows2,cols2)

if __name__ == '__main__':
    main()
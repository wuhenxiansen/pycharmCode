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
def gcd(a,b):
    while a!=0:
        a,b = b%a,a
    return b
#定义一个函数，参数分别为a,n，返回值为b
def findModReverse(a,m):#这个扩展欧几里得算法求模逆
    if gcd(a,m)!=1:
        return None
    u1,u2,u3 = 1,0,a
    v1,v2,v3 = 0,1,m
    while v3!=0:
        q = u3//v3
        v1,v2,v3,u1,u2,u3 = (u1-q*v1),(u2-q*v2),(u3-q*v3),v1,v2,v3
    return u1%m

class ntru:
    def __init__(self,N,p,q,Fp = None,Fq = None,g = None,hq = None,private_key = None,public_key = None):
        self.N = N
        self.p = p
        self.q = q
        self.private_key = private_key
        self.public_key = public_key
        self.Fp = Fp
        self.Fq = Fq
        self.g = g
        self.hq=hq
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

    def r_randpoly(self, one=None, _one=None, n=None):
        if one == None and _one == None:
            tot = random.randint(2, self.N - 1)
            one = random.randint(0, tot)
            _one = tot - one
        r = [0] * self.N
        flag = [-1] * self.N
        if n != None:
            idx = 0
            for i in n:
                r[idx] = i
                flag[idx] = 1
                if i == 1:
                    one -= 1
                idx += 1
        while one != 0 or _one != 0:
            pos = random.randint(0, self.N - 1)
            if flag[pos] == -1:
                if one > 0:
                    r[pos] = 1
                    flag[pos] = 1
                    one -= 1
                elif _one > 0:
                    r[pos] = -1
                    flag[pos] = 1
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
            return self._randpoly(13, 12)
        elif self.N == 167:
            return self._randpoly(21, 20)
        elif self.N == 503:
            return self._randpoly(73, 72)
        else:
            return self._randpoly()
    def randpoly_phi(self,n = None):
        if self.N == 107:
            if n==None:
                return self._randpoly(5,5)
            else:
                return self.r_randpoly(5, 5,n)
        if self.N == 167:
            if n==None:
                return self._randpoly(18,18)
            else:
                return self.r_randpoly(18, 18,n)
        elif self.N == 503:
            if n==None:
                return self._randpoly(55,55)
            else:
                return self.r_randpoly(55, 55,n)
        else:
            return self._randpoly()
    def get_public(self):
        #self.public_key =
        pass
    def createKey_pair(self):
        N = self.N
        q = self.q
        p = self.p
        self.private_key = self.randpoly_private()## f
        self.g = self.randpoly_g()
        while self.g.is_z():
            self.g = self.randpoly_g()
        tmp = q
        k = 0
        while tmp != 0:
            tmp = tmp // 2
            k += 1
        k -= 1
        while True:##循环直到随机多项式f分别对p,q有模逆
            try:
                self.Fq = self.private_key.inv(N,2,k)#mod 2^k求逆
                k=self.Fq.StarMult(NTRU.private_key,NTRU.N,NTRU.q)#k是[1]，就是整数1

                self.Fp = self.private_key.inv(N,p,1)
                if (self.Fq is not False) and (self.Fp is not False):
                    break
                self.private_key = self.randpoly_private()
            except can_not_div_Error:
                self.private_key = self.randpoly_private()
        while True:
            try:
                h = self.Fq.StarMult(self.g, N, q)
                self.public_key = h
                self.hq = self.public_key.inv(N,2,8)#mod 2^k求逆  实际上就是让多项式g可逆
                if self.hq is not False:
                    break
                self.g = self.randpoly_g()
                while self.g.is_z():
                    self.g = self.randpoly_g()
            except can_not_div_Error:
                self.g = self.randpoly_g()
                while self.g.is_z():
                    self.g = self.randpoly_g()
        ##s=self.hq.StarMult(self.public_key,NTRU.N,NTRU.q)
        return (h,self.private_key)
    def encrypto(self,m,n = None):
        phi = self.randpoly_phi(n)
        #print('随机项r:{}'.format(phi.coe))
        c = phi.StarMult(self.public_key,self.N,self.q)

        c.expend(self.N)
        #c2.expend(self.N)
        m.expend(self.N)
        for i in range(0,self.N):
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
    image = cv2.imread(r"09.png", cv2.IMREAD_GRAYSCALE)  # 以灰度模式加载图片
    # print(image)
    rows, cols = image.shape[:2]
    pixel_count = rows * cols
    image_array = image.reshape(1, pixel_count)[0]
    #print(image_array)
    LS = pixel_count
    #print(LS)
    #message=[]
    plainText = list()
    ii=0
    for m in image_array:

        m=bin(m).replace('0b', '')

        if len(m)<8:
            m=(8-len(m))*'0'+m
        temp = list()
        for bi in m:
            bi=int(bi)
            temp.append(bi)
        plainText.append(temp)
        ii+=1
    #print(plainText)
    print('\t数据隐藏者嵌入数据过程:\n')

    secrectimage1 = cv2.imread(r"Boat.png", cv2.IMREAD_GRAYSCALE)  # 以灰度模式加载图片

    rows1, cols1 = secrectimage1.shape[:2]
    pixel_count = rows1 * cols1
    secrectimage_array = secrectimage1.reshape(1, pixel_count)[0]

    data1 = ''
    for m in secrectimage_array:
        m = bin(m).replace('0b', '')
        if len(m) < 8:
            m = (8 - len(m)) * '0' + m
        data1 += m
    ##预处理待加密数据
    l = 5
    if NTRU.N == 107:
        l = 5
    elif NTRU.N == 167:
        l = 18
    elif NTRU.N == 503:
        l = 55

    length1 = len(data1)  # 第一阶段隐藏数据总二进制位长度
    Binlen1 = bin(length1).replace('0b', '')
    print('字符长度:{},编码：{}'.format(length1, Binlen1))
    while len(Binlen1) < 32:
        Binlen1 = '0' + Binlen1
    data1=Binlen1+data1  #data1前32比特表示隐藏数据的长度
    #print(data1)
    additionalData = list()
    temp = list()
    for idx in range(len(data1)):
        if idx!=0 and idx % l==0:
            additionalData.append(temp)
            temp=list()
        temp.append(int(data1[idx]))
    while len(temp) >0 and len(temp)<l:
            temp.append(0)
    additionalData.append(temp)
    listlen=len(additionalData)
    #print(listlen)
    length = len(plainText)
    index = 0
    C = list()
    r_idx=0
    #encryptData=''#密文串
    while index<length:
        if index%1000==0:
            print(index)
        ##改变多项式r
        if r_idx<listlen:
            c= NTRU.encrypto(poly(plainText[index]),additionalData[r_idx]) #得到密文
            c.expend(NTRU.N)
            r_idx+=1
        else:
            c = NTRU.encrypto(poly(plainText[index]))  # 得到密文
            c.expend(NTRU.N)
        C.append(c)
        index+=1
    return C,rows,cols,rows1,cols1
def DataHider(C,s):
    secrectimage2 = cv2.imread(r"Lena.png", cv2.IMREAD_GRAYSCALE)  # 以灰度模式加载图片
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
                if C[index].coe[index1 + 8] % 2 != int(data2[cnt]):
                    C[index].coe[index1 + 8] += 1
                    C[index].coe[index1 + 8] %= NTRU.q
                cnt += 1
            index1 += 1
        #print('嵌入后：',C[index].coe)
        index += 1
    #在最后一个像素点中隐藏数据表示嵌入数据的长度

    for i in range(0,32):
        if C[length - 1].coe[i + 8]%2!=int(Binlen2[i]):
            C[length - 1].coe[i + 8] +=1
            C[length - 1].coe[i + 8] %= NTRU.q

    print('\t第二阶段数据嵌入完毕!\n')
    end=time.process_time()
    print("第二阶段总耗时:{}".format(end-start))

    return C,rows2,cols2,end-start
def Receiver(C,s,rows,cols,rows1,cols1,rows2,cols2):
    print('提取第二阶段隐藏的数据')
    # 第二阶段嵌入数据提取
    # 先提取隐藏数据长度的信息
    L2 = ''
    A2 = list()
    for i in range(0, 32):
        L2 += str(C[len(C) - 1].coe[i + 8] % 2)
    print(L2)

    ad2Len = int(L2, 2)
    print('第二阶段数据长度：{}'.format(ad2Len))

    # 先提取第二阶段隐藏数据
    for c in C:
        for i in range(0, s):
            if ad2Len > 0:
                A2.append(str(c.coe[i + 8] % 2))
                ad2Len -= 1
    str3 = ''.join(A2)
    ll = len(str3)
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
    cv2.imwrite("secretImage2-Lena~.png", new_image1)

    print('解密')
    message1=list()
    ii=0

    cnt_len=list()
    l = 5

    if NTRU.N == 107:
        l = 5
    elif NTRU.N == 167:
        l = 18
    elif NTRU.N == 503:
        l = 55
    ad_i=0
    addi_data=list()
    for c in C:
        if ii%1000==0:
            print(ii)
        m1=NTRU.decrypto(c)#会改变c
        if 2 in m1.coe:
            print('密文：{}'.format(c.coe))
            print('明文：{}'.format(m1.coe))
        c.expend(NTRU.N)
        m1.expend(NTRU.N)
        #print(c.coe)
        for i in range(NTRU.N):
            c.coe[i] -= m1.coe[i]
            c.coe[i] %= NTRU.q

        r1 = c.StarMult(NTRU.hq, NTRU.N, NTRU.q)
        r1.expend(NTRU.N)
        # print(c1.coe)
        mr = findModReverse(NTRU.p, NTRU.q)

        for i in range(NTRU.N):
            r1.coe[i] *= mr
            r1.coe[i] %= NTRU.q
            if r1.coe[i] >= 128:
                r1.coe[i] -= NTRU.q
        # 提取数据
        # 先提取前32bit数据
        #print(r1.coe)
        for i in range(l):
            if len(cnt_len) <32:
                cnt_len.append(str(r1.coe[i]))
            else:
                total_len=int(''.join(cnt_len), 2)
                if ad_i< total_len:
                    addi_data.append(str(r1.coe[i]))
                    ad_i+=1
        m1.expend(NTRU.N)
        message1.append(m1.coe)
        ii+=1
    P = list()

    for me in message1:
        for j in range(0,8):
            P.append(str(me[j]))
    str1=''.join(P)
    #print(str1)
    bb1=re.findall(r'.{8}', str1)
    PlainText = np.zeros((1, len(C)))
    index=0
    for b1 in bb1:
        PlainText[0,index]=int(b1, 2)
        index+=1
    #print(PlainText[0])

    adstr=''.join(addi_data)
    #print(adstr)
    bb2 = re.findall(r'.{8}', adstr)
    addiText = np.zeros((1, len(bb2)))
    index = 0
    for b2 in bb2:
        addiText[0,index] = int(b2, 2)
        index += 1

    print('原始载体数据:')
    new_image = PlainText.reshape(rows,cols)
    #cv2.imshow("result080035", new_image)
    cv2.imwrite("result-09~.png", new_image)

    print('隐藏数据:')
    new_image2 = addiText.reshape(rows1, cols1)
    # cv2.imshow("result080035", new_image)
    cv2.imwrite("secretImage-Boat~.png", new_image2)
def main():
    C,rows,cols,rows1,cols1=Owner()#原始图像的行列等信息可以一并加密，这里为了后续处理方便直接传递给后面的函数使用
    C,rows2,cols2,time=DataHider(C,150)
    Receiver(C,150,rows,cols,rows1,cols1,rows2,cols2)

if __name__ == '__main__':
    main()
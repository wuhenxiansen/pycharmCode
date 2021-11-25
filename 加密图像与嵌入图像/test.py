lenB=int(input('输入k:'))
n=int(pow(2,lenB))
sum=0
for i in range(256):
	index=0
	s=set()

	while (i + 3 * index) < 256 and len(s)<n:
		s.add((i + 3 * index) % n)
		index += 1
	index1=0
	while (i - 3 * index1) >=0 and len(s)<n:
		s.add((i - 3 * index1) % n)
		index1 += 1
	if len(s)==n:
		sum+=1
	else:
		print(s)
	print(sum)
# a=int(input('输入a:'))
# b=int(input('输入b:'))
# index=0
# while (a + 3 * index) < 256 and (a+3*index)%256<b:
# 	index+=1
# 	if (a + 3 * index%256)==b:
# 		print(index)
# 		break
# index1=0
# while (a - 3 * index1) >=0 and (a-3*index1)%256>b:
# 	index1+=1
# 	if (a - 3 * index%256)==b:
# 		print(index1)
# 		break

with open('测试.txt','r',encoding='utf-8') as f:
    results=f.readlines()
strings=''
for s in results:
    strings+=s
print(strings)
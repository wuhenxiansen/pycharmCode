#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time     : 2020/11/24 11:28
# @Author   : MonsterKK
# @File     : test.py
# @Descript :
import numpy as np
e=0.5
path='D:/zhoutao/data/train_2000000.txt'
def new_train_set(path,float):
    totalLine=0
    total=0
    empty_dict = dict()#创建一个空字典
    with open(path, 'r', errors='ignore') as f:
        line=f.readline()#自带换行
        line=line.rstrip('\n') #  移除行尾换行符
        while line:
            totalLine=totalLine+1
            if line in empty_dict.keys():
                empty_dict[line]+=1
            else:
                empty_dict[line]=1
            line=f.readline()
            line = line.rstrip('\n')  #  移除行尾换行符
    print("总行数：{}".format(totalLine))
    for k,v in empty_dict.items():
        v/=totalLine  #原频率
        #print("原频率：{}:{}".format(k, v))
        v=pow(v,e)  #处理
        empty_dict[k]=v;#更新
        #print("新频率：{}:{}".format(k, v))
        total+=v
    print("newtotal:{}".format(total))
    for k,v in empty_dict.items():
        v=v/total #处理后出现频率
        v=v*totalLine
        empty_dict[k]=round(v)#四舍五入
    for k,v in empty_dict.items():
        print("新频率：{}，新次数：{}".format(k,v))
    lines=[]
    for k,v in empty_dict.items():
        i=0
        while i<v:
            lines.append(k)
            i+=1
    np.random.shuffle(lines)
    return  lines
lines=new_train_set(path,e)
with open('D:/zhoutao/data/new_train_2000000.txt', 'w+', errors='ignore') as f:
    for i in lines:
        #写入文件
        f.write(i+'\n')


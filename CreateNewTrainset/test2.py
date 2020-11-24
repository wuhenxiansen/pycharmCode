#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time     : 2020/11/24 17:00
# @Author   : MonsterKK
# @File     : test2.py
# @Descript :
path='D:/zhoutao/data/train_2000000.txt'
def new_train_set(path):
    totalLine=0
    total=0
    empty_dict = dict()
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
    for k, v in empty_dict.items():
        if k=='123456789':
            print("{}:{}".format(k,v))
new_train_set(path)
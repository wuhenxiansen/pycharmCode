#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time     : 2021/4/22 16:46
# @Author   : User
# @File     : test.py
# @Descript :

N=2048
s=5
p=[3,5,7,11,13,17,19]
for i in p :
    st = set()
    index=0
    while len(st) <N:
        t=(s+index*i)%N
       # print(t)
        st.add(t)
        index+=1
    print(index)

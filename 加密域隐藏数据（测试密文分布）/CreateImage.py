#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time     : 2021/12/29 22:18
# @Author   : User
# @File     : CreateImage.py
# @Descript :
import cv2
import numpy as np
import random
fileList=["t1.png","t2.png","t3.png","t4.png"]
for i in fileList:
    secrectimage1 = cv2.imread(i, cv2.IMREAD_GRAYSCALE)  # 以灰度模式加载图片

    rows1, cols1 = secrectimage1.shape[:2]
    print(rows1,cols1)
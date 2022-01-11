#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time     : 2021/11/27 21:06
# @Author   : User
# @File     : CalPSNR.py
# @Descript :
from PIL import Image
import numpy
import math
import cv2

def psnr(img1, img2):
    mse = numpy.mean((img1/1.0 - img2/1.0) ** 2)
    if mse <1.0e-10:
        return 1000000
    PIXEL_MAX = 255.0
    return 20 * math.log10(PIXEL_MAX / math.sqrt(mse))


img1 = cv2.imread(r"10.png", cv2.IMREAD_GRAYSCALE)  # 以灰度模式加载图片
img2 = cv2.imread(r"secretImage2-2.10.png", cv2.IMREAD_GRAYSCALE)  # 以灰度模式加载图片


i1_array = numpy.array(img1)
i2_array = numpy.array(img2)
rows, cols = img1.shape[:2]
pixel_count = rows * cols
image_array1 = img1.reshape(1, pixel_count)[0]
image_array2 = img2.reshape(1, pixel_count)[0]
r12 = psnr(i1_array, i2_array)
print(r12)
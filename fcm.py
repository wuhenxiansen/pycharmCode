#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time     : 2020/11/6 20:28
# @Author   : MonsterKK
# @File     : fcm.py
# @Descript :
import cv2
import numpy as np

C = 2
M = 2
EPSILON = 0.001


def get_init_fuzzy_mat(pixel_count):
    global C
    fuzzy_mat = np.zeros((C, pixel_count))
    #print(fuzzy_mat)
    for col in range(pixel_count):
        temp_sum = 0
        randoms = np.random.rand(C - 1, 1)#返回C-1行，1列的（0，1）之间随机数
        for row in range(C - 1):
            fuzzy_mat[row, col] = randoms[row, 0] * (1 - temp_sum)
            temp_sum += fuzzy_mat[row, col]
        fuzzy_mat[-1, col] = 1 - temp_sum#数组最后一行第col个元素
    return fuzzy_mat


def get_centroids(data_array, fuzzy_mat):
    global M
    #print(fuzzy_mat.shape[:2])
    class_num, pixel_count = fuzzy_mat.shape[:2] #输出的是(2,像素点)
    centroids = np.zeros((class_num, 1))#两个聚类中心初始化为0
    for i in range(class_num):
        fenzi = 0.
        fenmu = 0.
        for pixel in range(pixel_count):
            fenzi += np.power(fuzzy_mat[i, pixel], M) * data_array[0, pixel]#np.power(x,y) 计算x的y次方
            fenmu += np.power(fuzzy_mat[i, pixel], M)
        centroids[i, 0] = fenzi / fenmu
    return centroids

def eculid_distance(pixel_1, pixel_2):
    return np.power(pixel_1 - pixel_2, 2)


def cal_fcm_function(fuzzy_mat, centroids, data_array):
    global M
    class_num, pixel_count = fuzzy_mat.shape[:2]
    target_value = 0.0
    for c in range(class_num):
        for p in range(pixel_count):
            target_value += eculid_distance(data_array[0, p], centroids[c, 0]) * np.power(fuzzy_mat[c, p], M)
    return target_value


def get_label(fuzzy_mat, data_array):
    pixel_count = data_array.shape[1]
    label = np.zeros((1, pixel_count))

    for i in range(pixel_count):
        if fuzzy_mat[0, i] > fuzzy_mat[1, i]:
            label[0, i] = 0
        else:
            label[0, i] = data_array[i]#
    return label

def cal_fuzzy_mat(data_array, centroids):
    global M
    pixel_count = data_array.shape[1]
    class_num = centroids.shape[0]
    new_fuzzy_mat = np.zeros((class_num, pixel_count))
    for p in range(pixel_count):
        for c in range(class_num):
            temp_sum = 0.
            Dik = eculid_distance(data_array[0, p], centroids[c, 0])
            for i in range(class_num):
                temp_sum += np.power(Dik / (eculid_distance(data_array[0, p], centroids[i, 0])), (1 / (M - 1)))
            new_fuzzy_mat[c, p] = 1 / temp_sum
    return new_fuzzy_mat

def fcm(init_fuzzy_mat, init_centroids, data_array):
    global EPSILON
    last_target_function = cal_fcm_function(init_fuzzy_mat, init_centroids, data_array)
    print("迭代次数 = 1, 目标函数值 = {}".format(last_target_function))
    fuzzy_mat = cal_fuzzy_mat(data_array, init_centroids)
    centroids = get_centroids(data_array, fuzzy_mat)
    target_function = cal_fcm_function(fuzzy_mat, centroids, data_array)
    print("迭代次数 = 2, 目标函数值 = {}".format(target_function))
    count = 3
    while count < 100:
        if abs(target_function - last_target_function) <= EPSILON:
            break
        else:
            last_target_function = target_function
            fuzzy_mat = cal_fuzzy_mat(data_array, centroids)
            centroids = get_centroids(data_array, fuzzy_mat)
            print("fuzzy_mat={},centroids={}".format(fuzzy_mat,centroids))
            target_function = cal_fcm_function(fuzzy_mat, centroids, data_array)
            print("迭代次数 = {}, 目标函数值 = {}".format(count, target_function))
            count += 1
    return fuzzy_mat, centroids, target_function


image = cv2.imread(r"22.bmp", cv2.IMREAD_GRAYSCALE)#以灰度模式加载图片
#print(image)
rows, cols = image.shape[:2]
pixel_count = rows * cols
image_array = image.reshape(1, pixel_count)
#print(image_array)
# 初始模糊矩阵
init_fuzzy_mat = get_init_fuzzy_mat(pixel_count)
#print(init_fuzzy_mat)
# 初始聚类中心
init_centroids = get_centroids(image_array, init_fuzzy_mat)
#print(init_centroids)
fuzzy_mat, centroids, target_function = fcm(init_fuzzy_mat, init_centroids, image_array)
label = get_label(fuzzy_mat, image_array)
new_image = label.reshape(rows, cols)
cv2.imshow("result", new_image)
cv2.imwrite("fcm_result2.bmp", new_image)
cv2.waitKey(0)
cv2.destroyAllWindows()
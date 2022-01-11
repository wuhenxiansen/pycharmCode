#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time     : 2021/7/13 16:24
# @Author   : User
# @File     : histogram.py
# @Descript : 柱状图

import matplotlib.pyplot as plt
import numpy as np
import random
import matplotlib.ticker as ticker
# 这两行代码解决 plt 中文显示的问题
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False

# 输入统计数据
used_times=[25,30,20,18]
	# xishu=[[50,50],[100,100],[200,200]]
	# for li in xishu:
	# 	C2,rows1,cols1,rows2,cols2,used_time=DataHider(C,li[0],li[1])
	# 	used_times.append(used_time)

Xaxis = ('128*128的图像', '256*256的图像', '512*512的图像',"1204*1024的图像")


bar_width = 0.5  # 条形宽度
index_male = np.arange(len(Xaxis))

# 使用两次 bar 函数画出两组条形图
plt.bar(index_male, height=used_times, width=bar_width, color='b')

plt.legend()  # 显示图例
plt.xticks(index_male, Xaxis)  # 让横坐标轴刻度显示 waters 里的饮用水， index_male + bar_width/2 为横坐标轴刻度的位置
plt.ylabel('总嵌入时间（ms）')  # 纵坐标轴标题
# plt.title('不同长度（L）的字符串在不同参数下数据隐藏的总耗时')  # 图形标题
plt.savefig('test.png')

used_times=[125,230,20]
Xaxis=('s=500,t=500','s=200,t=100','s=200,t=200')


bar_width = 0.5  # 条形宽度
index_male = np.arange(len(Xaxis))

# 使用两次 bar 函数画出两组条形图
plt.bar(index_male, height=used_times, width=bar_width, color='b')

plt.legend()  # 显示图例
plt.xticks(index_male, Xaxis)  # 让横坐标轴刻度显示 waters 里的饮用水， index_male + bar_width/2 为横坐标轴刻度的位置
plt.ylabel('总嵌入时间（ms）')  # 纵坐标轴标题
# plt.title('不同长度（L）的字符串在不同参数下数据隐藏的总耗时')  # 图形标题
plt.savefig('test2.png')
plt.show()

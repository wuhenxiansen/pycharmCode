#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time     : 2021/12/29 13:45
# @Author   : User
# @File     : test.py
# @Descript :
import matplotlib.pyplot as plt
import numpy as np
import random
import matplotlib.ticker as ticker
# 这两行代码解决 plt 中文显示的问题
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False
used_times=[0.264,0.512,1.035,2.124,3.985,8.231,15.987]
Xaxis = ('128*128', '256*128','256*256', '512*256','512*512','1024*512',"1204*1024")

bar_width = 0.5  # 条形宽度
index_male = np.arange(len(Xaxis))
# 使用两次 bar 函数画出两组条形图
plt.bar(index_male, height=used_times, width=bar_width, color='g')
plt.legend()  # 显示图例
plt.xticks(index_male, Xaxis)  # 让横坐标轴刻度显示 waters 里的饮用水， index_male + bar_width/2 为横坐标轴刻度的位置
plt.ylabel('总嵌入时间（s）')  # 纵坐标轴标题
plt.xlabel('作为隐藏数据的不同隐藏图像大小')
# plt.title('不同长度（L）的字符串在不同参数下数据隐藏的总耗时')  # 图形标题
plt.savefig('differLen_used_time.png')
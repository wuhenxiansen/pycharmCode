#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time     : 2021/7/13 16:24
# @Author   : User
# @File     : histogram.py
# @Descript : 柱状图

import matplotlib.pyplot as plt
import numpy as np

# 这两行代码解决 plt 中文显示的问题
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False

# 输入统计数据
waters = ('L=500', 'L=1000', 'L=5000','L=10000')
buy_number_male = [25, 48, 252, 507]
buy_number_female = [49, 105, 538, 1070]
buy_number_ = [101, 203, 1134, 2134]
bar_width = 0.25  # 条形宽度
index_male = np.arange(len(waters))
index_female = index_male + bar_width
index_=index_male + bar_width+bar_width
# 使用两次 bar 函数画出两组条形图
plt.bar(index_male, height=buy_number_male, width=bar_width, color='r', label='s+t=100')
plt.bar(index_female, height=buy_number_female, width=bar_width, color='g', label='s+t=200')
plt.bar(index_, height=buy_number_, width=bar_width, color='b', label='s+t=400')
plt.legend()  # 显示图例
plt.xticks(index_male + bar_width, waters)  # 让横坐标轴刻度显示 waters 里的饮用水， index_male + bar_width/2 为横坐标轴刻度的位置
plt.ylabel('总嵌入时间（ms）')  # 纵坐标轴标题
#plt.title('不同长度（L）的字符串在不同参数下数据隐藏的总耗时')  # 图形标题

plt.show()
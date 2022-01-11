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
waters=[]
for i in range(50):
	if i%50==0and i!=0:
		waters.append(i)
	else:
		waters.append('')
print(waters)
buy_number_male=[]
#waters = ('0', '1', '2','3', '4','5','6', '7', '8','9', '10', '11', '12','13', '14','15','16', '17', '18','19','20', '21', '22','23', '24','25','26', '27', '28','29', '30','31','0', '1', '2','3', '4','5''0', '1', '2','3', '4','5''0', '1', '2','3', '4','5''0', '1', '2','3', '4','5''0', '1', '2','3', '4','5''0', '1', '2','3', '4','5''0', '1', '2','3', '4','5','0', '1', '2','3', '4','5''0', '1', '2','3', '4','5''0', '1', '2','3', '4','5','0', '1', '2','3', '4','5''0', '1', '2','3', '4','5')
for i in range(50):
	buy_number_male.append(random.randint(0,100))

bar_width = 0.5  # 条形宽度
index_male = np.arange(len(waters))

# 使用两次 bar 函数画出两组条形图
plt.bar(index_male, height=buy_number_male, width=bar_width, color='b', label='lena')

plt.legend()  # 显示图例
plt.xticks(index_male, waters)  # 让横坐标轴刻度显示 waters 里的饮用水， index_male + bar_width/2 为横坐标轴刻度的位置
plt.ylabel('总嵌入时间（ms）')  # 纵坐标轴标题
#plt.title('不同长度（L）的字符串在不同参数下数据隐藏的总耗时')  # 图形标题
plt.show()
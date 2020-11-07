#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time     : 2019/10/12 16:55
# @Author   : MonsterKK
# @File     : Box.py
# @Descript : 抽奖盒子里的球

import matplotlib.pyplot as plt
import numpy as np
import matplotlib

# 设置matplotlib正常显示中文和符号
matplotlib.rcParams['font.sans-serif'] = ['SimHei']   # 用黑体显示中文
matplotlib.rcParams['axes.unicode_minus'] = False     # 正常显示符号

# 柱子总数
N = 9
# 包含每个柱子对应值的序列
data = np.array([2, 4, 6, 8, 9, 7, 5, 3, 1])/45

# 包含每个柱子下标的序列
index = np.arange(N)+1

# 柱子的宽度
width = 1

# 绘制柱状图，每根柱子的颜色为蓝色
plt.bar(x=index, height=data, width=width, color="blue")
plt.show()
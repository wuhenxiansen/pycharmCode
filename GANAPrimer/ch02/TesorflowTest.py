#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time     : 2019/10/12 9:52
# @Author   : MonsterKK
# @File     : TesorflowTest.py
# @Descript : Tensorflow功能测试

import tensorflow as tf
import numpy as np

# 输出字符
# Tensorflow中所有元素都记为Tensor，所以需要使用tf的常数变量
# 使用Session来提供运行环境用户Tensorflow的图计算，否则程序不会执行计算
hello = tf.constant('Hello Tensorflow!')
sess = tf.compat.v1.Session()  # 推荐使用tf.compat.v1.Session()而不是tf.Session()
# print(sess.run(hello))

# 加法和乘法运算
a = tf.constant(2)
b = tf.constant(3)
with tf.compat.v1.Session() as sess:
    """
    一个Session可能会拥有一些资源，例如Variable或者Queue。
    当我们不再需要该session的时候，需要将这些资源进行释放。有两种方式：
    ① 调用session.close()方法；
    ② 使用with tf.Session()创建上下文（Context）来执行，当上下文退出时自动释放。

    """
    # print(sess.run(a))
    # print(sess.run(b))
    # print(sess.run(a+b))
    # print(sess.run(a*b))

# 使用placeholder设置变量计算
# 推荐使用tf.compat.v1.placeholder
a = tf.compat.v1.placeholder(tf.int16)
b = tf.compat.v1.placeholder(tf.int16)
add = tf.add(a, b)
mul = tf.multiply(a, b)
# with tf.compat.v1.Session() as sess:
# print(sess.run(add, feed_dict={a: 2, b: 3}))
# print(sess.run(mul, feed_dict={a: 2, b: 3}))

# 矩阵乘法
# expected an indented block 需要缩进的块
matrix1 = tf.constant([3., 3.])
matrix2 = tf.constant([[2.], [2.]])
product = tf.multiply(matrix1, matrix2)


# with tf.compat.v1.Session() as sess:
#     result = sess.run(product)
#     print(result)

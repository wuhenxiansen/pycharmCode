#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time     : 2019/10/25 18:54
# @Author   : MonsterKK
# @File     : UDPServer.py
# @Descript :

import socket
address = ('127.0.0.1', 31500)
server = socket.socket(type=socket.SOCK_DGRAM)
server.bind(('192.168.1.165', 7890))
print("服务端已开启7890端口，正在等待被连接")
data, address = server.recvfrom(1024)
print("client>>", data.decode('utf-8'))
print("客户端连接的socket地址：", address)
server.sendto(b'drink more water!', address)
server.close()

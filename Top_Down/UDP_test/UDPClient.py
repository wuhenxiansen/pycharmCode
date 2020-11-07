#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time     : 2019/10/25 18:51
# @Author   : MonsterKK
# @File     : UDPClient.py
# @Descript :

import socket
client = socket.socket(type=socket.SOCK_DGRAM)
send_data = b'hello sheenstar'
client.sendto(send_data, ('192.168.1.165', 7890))
re_Data, address = client.recvfrom(1024)
print("server>>", re_Data.decode('utf-8'))
client.close()
#!/usr/bin/python
# -*- coding: utf-8 -*-

import socket
import sys
import redis
from _thread import *

HOST = ''
PORT = 18060
Bufsiz = 1024
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print("Socket created")
# Bind socket to local host and port
try:
    s.bind((HOST, PORT))
except (socket.error, msg):
    print('Bind failed. Error Code : ' + str(msg[0]) + ' Message ' + msg[1])
    sys.exit()
print("Socket bind complete")
# Start listening on socket
s.listen(10)
print("Socket now listening")

# Function for handling connections. This will be used to create threads
# redis
client = redis.StrictRedis(host='localhost', port=6379, db=1)
def clientthread(conn,ipaddr):
    #infinite loop so that function do not terminate and thread do not end.
    while True:
        # Receiving from client
        data = conn.recv(Bufsiz)
        # reply = 'OK...' + data
        # conn.sendall(reply)
        client.rpush(ipaddr, data)
        #print(ipaddr)
        print(data)
        if not data:
            break
    #came out of loop
    conn.close()

# now keep talking with the client
while True:
    #wait to accept a connection - blocking call
    conn, addr = s.accept()
    ipaddr = addr[0]
    print('Connected with ' + addr[0] + ':' + str(addr[1]))
    # 会有本地回环地址在尝试连接，去除
    if(addr[0]!="127.0.0.1"):
        start_new_thread(clientthread, (conn, addr[0],))
s.close()

#!/usr/bin/python
# -*- coding: utf-8 -*-

import redis
from packOSC import bank, release, valueB1, valueB2, valueB3, valueB4

client = redis.StrictRedis(host = 'localhost', port = 6379, db = 1)
# key为不同传感器对应的IP
# key = sys.argv[1]
key = "192.168.0.102"

BeFlag = 0
BeCount = 0
Timestep = 3 #出现多少次代表 按下
status_1_Open = 0 # 按键1按下
status_2_Open = 0 # 按键2按下
status_3_Open = 0 # 激光1无遮挡
status_4_Open = 0 # 激光2无遮挡
status_1_Close = 0 # 按键1松开
status_2_Close = 0 # 按键2松开
status_3_Close = 0 # 激光1遮挡
status_4_Close = 0 # 激光2遮挡


while True:
    data = client.blpop(key)
    #data是列表结构，第一个结点为key值，分析时将其去掉
    #strg = ''.encode('utf-8').join(data[1:])
    #print(data)
    strg = data[1]
    value = strg.split(b"S")
    value = value[1]
    item = value.decode('ascii')

    if len(item) == 4:
        if (BeFlag == 0) & (item[0] == '1') & (item[1] == '1'):
            BeCount = BeCount + 1
            # 下面的数字5得实际测试
            startTimestep = 10
            if BeCount > startTimestep:
                print("already 5 mins")
                BeCount = 0
                BeFlag = 1
                bank(int(1), int(1))
            else:
                print("press")

        elif BeFlag == 1:
            # 按键1
            if (item[0] == '1'):
                status_1_Open = status_1_Open + 1
                status_1_Close = 0
            elif (item[0] == '0'):
                status_1_Close = status_1_Close + 1
                status_1_Open = 0

            # 按键2
            if (item[1] == '1'):
                status_2_Open = status_2_Open + 1
                status_2_Close = 0
            elif (item[1] == '0'):
                status_2_Close = status_2_Close + 1
                status_2_Open = 0

            # 激光1
            if (item[2] == '0'):
                status_3_Open = status_3_Open + 1
                status_3_Close = 0
            elif (item[2] == '1'):
                status_3_Close = status_3_Close + 1
                status_3_Open = 0

            # 激光2
            if (item[3] == '0'):
                status_4_Open = status_4_Open + 1
                status_4_Close = 0
            elif (item[3] == '1'):
                status_4_Close = status_4_Close + 1
                status_4_Open = 0
        else:
            print("not start yet!!!!!")

        # 输出结果
        if status_1_Open == Timestep:
            print("1:Status_Button_Press")
            status_1_Close = 0
            valueB1(0)

        if status_2_Open == Timestep:
            print("2:Status_Button_Press")
            status_2_Close = 0
            valueB2(0)

        if status_3_Open == Timestep:
            print("3:Status_Laser_Shelter")
            status_3_Close = 0
            valueB3(0)

        if status_4_Open == Timestep:
            print("4:Status_Laser_Shelter")
            status_4_Close = 0
            valueB4(0)

        if status_1_Close == Timestep:
            release()
            print("1:Status_Button_Open")
            status_1_Open = 0
            valueB1(1)

        if status_2_Close == Timestep:
            print("2:Status_Button_Open")
            status_2_Open = 0
            valueB2(1)

        if status_3_Close == Timestep:
            print("3:Status_Laser_Shine")
            status_3_Open = 0
            valueB3(1)

        if status_4_Close == Timestep:
            print("4:Status_Laser_Shine")
            valueB4(1)
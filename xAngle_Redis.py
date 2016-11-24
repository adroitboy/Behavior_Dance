#!/usr/bin/python
# -*- coding: utf-8 -*-

import redis
from packOSC import bank, release, valueA

client = redis.StrictRedis(host='localhost', port=6379, db=1)
# key 为不同传感器对应的IP
# key = sys.argv[1]
key = "192.168.0.101"

# 全局变量sect[1-4]记录在某一区域连续出现的次数，初始化为0
continueNum = 18
sect = dict()
for i in range(1,5):
    sect['%s' % i] = 0

sectNum = 0
# 判断xAngle在哪一section
def section(xAngle):
    global sectNum
    if ( 0 < xAngle) & (185 >= xAngle):
        sectNum = 1
    elif (185 < xAngle) & (290 >= xAngle):
        sectNum = 2
    elif (290 < xAngle) & (395 >= xAngle):
        sectNum = 3
    elif (395 < xAngle) & (600 >= xAngle):
        sectNum = 4
    return sectNum

#返回sect中的最大值和对应的下标，numMax：区域编号，valueMax：次数
def maxValue(sect):
    numMax = 0
    valueMax = 0
    for k, v in sect.items():
        if v == max(sect.values()):
            numMax = k
            valueMax = v
    return numMax, valueMax


CurrSec = -1
lastValue = -1
while True:
    data = client.blpop(key)
    
    strg = data[1]

    fiveAngleValue = strg.split(b"YY,")
    fiveAngleValue = fiveAngleValue[1:]
    
    num = len(fiveAngleValue)
    for i in range(num - 1):
        if len(fiveAngleValue[i+1]) == 25:
            singleAngleValue = fiveAngleValue[i+1].split(b",")
            xAngle = singleAngleValue[0]
            #angle val            
            #print(xAngle,)
            # 这个需要改！！！！！
            val = (int(xAngle)*4)-100
            valueA(float(val))
            result = section(int(xAngle))
            if CurrSec != result:
                #保证连续continueNum个出现才可，中间断开的要清0
                if ( lastValue != -1) & ( lastValue != result):
                    sect['%s' % lastValue] = 0
                sect['%s' % result] = sect['%s' % result] + 1
                lastValue = result
                numMax, valueMax = maxValue(sect)

                if valueMax >= continueNum:
                    ### section
                    numMax = int(numMax)
                    
                    """
                    if numMax == 1:
                        bank(int(1),int(2))
                    elif numMax == 2:
                        release()
                    elif numMax == 3:
                        bank(int(1),int(2))
                    elif numMax == 4:
                        release()
                    """

                    print(numMax)

                    #print('\r')
                    #print(numMax + ' section')
                    CurrSec = int(numMax)
                    sect['%s' % numMax] = 0

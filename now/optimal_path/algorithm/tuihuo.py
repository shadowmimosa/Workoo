import os
import sys
import math
import numpy as np

from random import choice, shuffle, sample, uniform

#假设下面是五个地点的距离对称矩阵(Wij = Wji)
names = ['重庆', '上海', '北京', '广州', '昆明']
arr = ([0, 50, 30, 10, 10], [50, 0, 60, 30,
                             20], [30, 60, 0, 80,
                                   70], [20, 30, 80, 0,
                                         60], [10, 20, 70, 60, 0])

num = len(arr)

print("模拟退火算法查找最短路径：")


### 参数：最小路径的最后一个节点和邻域
def valSimulateAnnealSum(curnode, nextnodeList, t):

    if nextnodeList == None or len(nextnodeList) < 1:
        print("empty")
        return 0

    maxcost = sys.maxsize
    retnode = 0

    for node in nextnodeList:
        # print "curnode : ",curnode ," node: " ,node ," mincost : ",mincost

        t *= 0.98  ## 退火因子
        if arr[curnode][node] < maxcost:
            maxcost = arr[curnode][node]
            retnode = node
        ## 以一定的概率接受较差的解
        else:
            #r = uniform(0, 1)
            r = math.exp((arr[curnode][node] - maxcost) / t)
            if arr[curnode][node] > maxcost and t > t_min and math.exp(
                (arr[curnode][node] - maxcost) / t) > r:
                #print " t = " ,t , "maxcost = ", maxcost , " arr = " ,arr[curnode][node],   "  exp = ",math.exp((arr[curnode][node] - maxcost)/t)  ,  " r = ",r , "t_min = " ,t_min
                retnode = node
                maxcost = arr[curnode][node]
                return (retnode, maxcost, t)

    return (retnode, maxcost, t)


indexList = [i for i in range(num)]  ### 原始的节点序列
selectedList = []  ## 选择好的元素

### 具体思想是： 从剩余的元素中随机选择十分之一的元素，作为邻域。然后从邻域中选择一个元素作为已经构建好的最小路径的下一个节点，
#  使得该路径
mincost = sys.maxsize  ###最小的花费

count = 0  ### 计数器
t = 100  ## 初始温度
t_min = 50  ## 最小温度
while count < num:
    count += 1
    ### 构建一个邻域: 如果indexList中元素个数大于10个，则取样的个数为剩余元素个数的十分之一的整数。否则为剩余元素个数对10的取余数
    leftItemNum = len(indexList)
    #  print "leftItemNum:" ,leftItemNum
    #nextnum = leftItemNum // 10 if leftItemNum >= 10 else leftItemNum % 10
    #nextnodeList = sample(indexList, nextnum)  ### 从剩余的节点中选出nextnum个节点
    if leftItemNum < 2:
        leftItemNum = 1
    else:
        leftItemNum -= 1

    nextnodeList = sample(indexList, leftItemNum)

    if len(selectedList) == 0:
        item = choice(nextnodeList)
        selectedList.append(item)
        indexList.remove(item)
        mincost = 0
        continue

    curnode = selectedList[len(selectedList) - 1]
    # print "nextnodeList:" ,nextnodeList
    nextnode, maxcost, t = valSimulateAnnealSum(curnode, indexList,
                                                t)  ### 对待选的序列路径求和

    ### 将返回的路径值添加到原来的路径值上，同时，在剩余的节点序列中，删除nextnode节点
    mincost += maxcost
    indexList.remove(nextnode)
    selectedList.append(nextnode)

print("最合适的路径为：", selectedList)
print("对应城市", names)
print("路径节点个数：", len(selectedList))
print("最小花费为：", mincost)
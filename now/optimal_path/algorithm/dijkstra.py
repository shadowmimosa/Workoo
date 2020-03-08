#!/bin/python
# -*- coding:utf-8 -*-


def dijkstra(graph, startIndex, path, cost, infinity):
    """
    求解各节点最短路径，获取path，和cost数组，
    path[i] 表示vi节点的前继节点索引，一直追溯到起点。
    cost[i] 表示vi节点的花费
    """
    lenth = len(graph)
    v = [0] * lenth
    # 初始化 path，cost，V
    for i in range(lenth):
        if i == startIndex:
            v[startIndex] = 1
        else:
            cost[i] = graph[startIndex][i]
            path[i] = (startIndex if (cost[i] < infinity) else -1)
    # print v, cost, path
    for i in range(1, lenth):
        minCost = infinity
        curNode = -1
        for w in range(lenth):
            if v[w] == 0 and cost[w] < minCost:
                minCost = cost[w]
                curNode = w
        # for 获取最小权值的节点
        if curNode == -1: break
        # 剩下都是不可通行的节点，跳出循环
        v[curNode] = 1
        for w in range(lenth):
            if v[w] == 0 and (graph[curNode][w] + cost[curNode] < cost[w]):
                cost[w] = graph[curNode][w] + cost[curNode]  # 更新权值
                path[w] = curNode  # 更新路径
        # for 更新其他节点的权值（距离）和路径
    return path


if __name__ == '__main__':
    infinity = 2147483647
    graph = [
        [infinity, infinity, 10, infinity, 30, 100],
        [infinity, infinity, 5, infinity, infinity, infinity],
        [infinity, infinity, infinity, 50, infinity, infinity],
        [infinity, infinity, infinity, infinity, infinity, 10],
        [infinity, infinity, infinity, 20, infinity, 60],
        [infinity, infinity, infinity, infinity, infinity, infinity],
    ]
    path = [0] * 6
    cost = [0] * 6
    print(dijkstra(graph, 0, path, cost, infinity))
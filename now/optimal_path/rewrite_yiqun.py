# -*- coding: utf-8 -*-
import random
import copy
import time
import sys
import math
import tkinter  #//GUI模块
import threading
from functools import reduce

# 参数
'''
ALPHA:信息启发因子，值越大，则蚂蚁选择之前走过的路径可能性就越大
      ，值越小，则蚁群搜索范围就会减少，容易陷入局部最优
BETA:Beta值越大，蚁群越就容易选择局部较短路径，这时算法收敛速度会
     加快，但是随机性不高，容易得到局部的相对最优
'''
(ALPHA, BETA, RHO, Q) = (1.0, 2.0, 0.5, 100.0)
# 城市数，蚁群
(city_num, ant_num) = (50, 50)

distance_x = [
    178, 272, 176, 171, 650, 499, 267, 703, 408, 437, 491, 74, 532, 416, 626,
    42, 271, 359, 163, 508, 229, 576, 147, 560, 35, 714, 757, 517, 64, 314,
    675, 690, 391, 628, 87, 240, 705, 699, 258, 428, 614, 36, 360, 482, 666,
    597, 209, 201, 492, 294
]
distance_y = [
    170, 395, 198, 151, 242, 556, 57, 401, 305, 421, 267, 105, 525, 381, 244,
    330, 395, 169, 141, 380, 153, 442, 528, 329, 232, 48, 498, 265, 343, 120,
    165, 50, 433, 63, 491, 275, 348, 222, 288, 490, 213, 524, 244, 114, 104,
    552, 70, 425, 227, 331
]

(city_num, ant_num) = (8, 8)

distance_x = [
    70.300, 147.973, 82.993, 118.359, 124.901, 71.679, 145.102, 89.484
]
distance_y = [
    86.467, 56.796, 116.138, 106.372, 124.388, 72.253, 128.810, 99.096
]

distance_x = [
    22.770300, 22.847973, 22.782993, 22.818359, 22.824901, 22.771679,
    22.845102, 22.789484
]
distance_y = [
    114.386467, 114.356796, 114.416138, 114.406372, 114.424388, 114.372253,
    114.428810, 114.399096
]

distance_x = [
    770.300, 847.973, 782.993, 818.359, 824.901, 771.679, 845.102, 789.484
]
distance_y = [
    386.467, 356.796, 416.138, 406.372, 424.388, 372.253, 428.810, 399.096
]

#城市距离和信息素
# distance_graph = [[0.0 for col in range(city_num)] for raw in range(city_num)]
pheromone_graph = [[1.0 for col in range(city_num)] for raw in range(city_num)]

distance_graph = [[0, 31483, 37478, 35532, 44441, 42105, 33301, 44181, 33651],
                  [31483, 0, 18265, 8189, 7731, 9320, 2284, 11953, 2871],
                  [37478, 18265, 0, 27866, 10314, 9853, 19944, 13501, 16299],
                  [35532, 8189, 27866, 0, 15293, 12379, 9409, 15890, 10616],
                  [44441, 7731, 10314, 15293, 0, 2558, 8335, 6206, 4614],
                  [42105, 9320, 9853, 12379, 2558, 0, 10093, 3650, 6448],
                  [33301, 2284, 19944, 9409, 8335, 10093, 0, 12669, 4199],
                  [44181, 11953, 13501, 15890, 6206, 3650, 12669, 0, 8846],
                  [33651, 2871, 16299, 10616, 4614, 6448, 4199, 8846, 0]]


# distance_graph = [
#     [0, 43119, 35532, 32964, 36742, 38350, 31577, 32613, 32239, 37817, 34155],
#     [43119, 0, 9934, 5768, 2211, 10407, 7032, 7518, 9642, 9202, 6810],
#     [35532, 9934, 0, 9929, 13707, 28497, 8542, 8805, 5595, 27964, 5866],
#     [32964, 5768, 9929, 0, 5138, 16607, 2394, 2858, 6579, 16074, 9050],
#     [36742, 2211, 13707, 5138, 0, 12490, 7226, 7712, 8717, 11285, 5885],
#     [38350, 10407, 28497, 16607, 12490, 0, 17343, 17825, 19949, 744, 17117],
#     [31577, 7032, 8542, 2394, 7226, 17343, 0, 536, 4764, 17283, 7235],
#     [32613, 7518, 8805, 2858, 7712, 17825, 536, 0, 5019, 17538, 7490],
#     [32239, 9642, 5595, 6579, 8717, 19949, 4764, 5019, 0, 19918, 5648],
#     [37817, 9202, 27964, 16074, 11285, 744, 17283, 17538, 19918, 0, 16584],
#     [34155, 6810, 5866, 9050, 5885, 17117, 7235, 7490, 5648, 16584, 0]
# ]

#----------- 蚂蚁 -----------
class Ant(object):

    # 初始化
    def __init__(self, ID):

        self.ID = ID  # ID
        self.__clean_data()  # 随机初始化出生点

    # 初始数据
    def __clean_data(self):

        self.path = []  # 当前蚂蚁的路径
        self.total_distance = 0.0  # 当前路径的总距离
        self.move_count = 0  # 移动次数
        self.current_city = -1  # 当前停留的城市
        self.open_table_city = [True for i in range(city_num)]  # 探索城市的状态

        city_index = random.randint(0, city_num - 1)  # 随机初始出生点
        self.current_city = city_index
        self.path.append(city_index)
        self.open_table_city[city_index] = False
        self.move_count = 1

    # 选择下一个城市  
    def __choice_next_city(self):

        next_city = -1
        select_citys_prob = [0.0 for i in range(city_num)]  #存储去下个城市的概率
        total_prob = 0.0

        # 获取去下一个城市的概率
        for i in range(city_num):
            if self.open_table_city[i]:
                try:
                    # 计算概率：与信息素浓度成正比，与距离成反比
                    select_citys_prob[i] = pow(
                        pheromone_graph[self.current_city][i], ALPHA) * pow(
                            (1.0 / distance_graph[self.current_city][i]), BETA)
                    total_prob += select_citys_prob[i]
                except ZeroDivisionError as e:
                    print(
                        'Ant ID: {ID}, current city: {current}, target city: {target}'
                        .format(ID=self.ID,
                                current=self.current_city,
                                target=i))
                    sys.exit(1)

        # 轮盘选择城市
        if total_prob > 0.0:
            # 产生一个随机概率,0.0-total_prob
            temp_prob = random.uniform(0.0, total_prob)
            for i in range(city_num):
                if self.open_table_city[i]:
                    # 轮次相减
                    temp_prob -= select_citys_prob[i]
                    if temp_prob < 0.0:
                        next_city = i
                        break

        # 未从概率产生，顺序选择一个未访问城市
        # if next_city == -1:
        #     for i in range(city_num):
        #         if self.open_table_city[i]:
        #             next_city = i
        #             break

        if (next_city == -1):
            next_city = random.randint(0, city_num - 1)
            while ((self.open_table_city[next_city]) == False
                   ):  # if==False,说明已经遍历过了
                next_city = random.randint(0, city_num - 1)

        # 返回下一个城市序号
        return next_city

    # 计算路径总距离
    def __cal_total_distance(self):

        temp_distance = 0.0

        for i in range(1, city_num):
            start, end = self.path[i], self.path[i - 1]
            temp_distance += distance_graph[start][end]

        # 回路
        end = self.path[0]
        temp_distance += distance_graph[start][end]
        self.total_distance = temp_distance

    # 移动操作
    def __move(self, next_city):

        self.path.append(next_city)
        self.open_table_city[next_city] = False
        self.total_distance += distance_graph[self.current_city][next_city]
        self.current_city = next_city
        self.move_count += 1

    # 搜索路径
    def search_path(self):

        # 初始化数据
        self.__clean_data()

        # 搜素路径，遍历完所有城市为止
        while self.move_count < city_num:
            # 移动到下一个城市
            next_city = self.__choice_next_city()
            self.__move(next_city)

        # 计算路径总长度
        self.__cal_total_distance()


#----------- TSP问题 -----------


class TSP(object):
    def __init__(self, n=8):

        self.n = n
        self.new()
        self.search_path()

    # 初始化
    def new(self, evt=None):
        # # # 计算城市之间的距离
        # for i in range(city_num):
        #     for j in range(city_num):
        #         temp_distance = pow((distance_x[i] - distance_x[j]), 2) + pow(
        #             (distance_y[i] - distance_y[j]), 2)
        #         temp_distance = pow(temp_distance, 0.5)
        #         distance_graph[i][j] = float(int(temp_distance + 0.5))

        # 初始城市之间的距离和信息素
        for i in range(city_num):
            for j in range(city_num):
                pheromone_graph[i][j] = 1.0

        self.ants = [Ant(ID) for ID in range(ant_num)]  # 初始蚁群
        self.best_ant = Ant(-1)  # 初始最优解
        self.best_ant.total_distance = 1 << 31  # 初始最大距离
        self.iter = 1  # 初始化迭代次数

    # 开始搜索
    def search_path(self, evt=None):

        while True:
            # 遍历每一只蚂蚁
            for ant in self.ants:
                # 搜索一条路径
                ant.search_path()
                # 与当前最优蚂蚁比较
                if ant.total_distance < self.best_ant.total_distance:
                    # 更新最优解
                    self.best_ant = copy.deepcopy(ant)
            # 更新信息素
            self.__update_pheromone_gragh()
            print(u"迭代次数：", self.iter, u"最佳路径总距离：",
                  int(self.best_ant.total_distance))
            print(self.best_ant.path)
            self.iter += 1

    # 更新信息素
    def __update_pheromone_gragh(self):

        # 获取每只蚂蚁在其路径上留下的信息素
        temp_pheromone = [[0.0 for col in range(city_num)]
                          for raw in range(city_num)]
        for ant in self.ants:
            for i in range(1, city_num):
                start, end = ant.path[i - 1], ant.path[i]
                # 在路径上的每两个相邻城市间留下信息素，与路径总距离反比
                temp_pheromone[start][end] += Q / ant.total_distance
                temp_pheromone[end][start] = temp_pheromone[start][end]

        # 更新所有城市之间的信息素，旧信息素衰减加上新迭代信息素
        for i in range(city_num):
            for j in range(city_num):
                pheromone_graph[i][
                    j] = pheromone_graph[i][j] * RHO + temp_pheromone[i][j]


if __name__ == '__main__':
    TSP()
import sys
import copy
import random

(ALPHA, BETA, RHO, Q) = (1.0, 2.0, 0.5, 100.0)
(city_num, dog_num) = (50, 50)
pheromone_graph = [[1.0 for col in range(city_num)] for raw in range(city_num)]
distance_graph = [[1.0 for col in range(city_num)] for raw in range(city_num)]
waiting = 250

class Dog(object):
    def __init__(self, ID):

        self.ID = ID
        self.__clean_data()

    def __clean_data(self):

        self.path = []
        self.total_distance = 0.0
        self.move_count = 0
        self.current_city = -1
        self.open_table_city = [True for i in range(city_num)]

        city_index = random.randint(0, city_num - 1)
        self.current_city = city_index
        self.path.append(city_index)
        self.open_table_city[city_index] = False
        self.move_count = 1

    def __choice_next_city(self):

        next_city = -1
        select_citys_prob = [0.0 for i in range(city_num)]
        total_prob = 0.0

        for i in range(city_num):
            if self.open_table_city[i]:
                try:
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

        if total_prob > 0.0:
            temp_prob = random.uniform(0.0, total_prob)
            for i in range(city_num):
                if self.open_table_city[i]:
                    temp_prob -= select_citys_prob[i]
                    if temp_prob < 0.0:
                        next_city = i
                        break

        if (next_city == -1):
            next_city = random.randint(0, city_num - 1)
            while ((self.open_table_city[next_city]) == False):
                next_city = random.randint(0, city_num - 1)

        return next_city

    def __cal_total_distance(self):

        temp_distance = 0.0

        for i in range(1, city_num):
            start, end = self.path[i], self.path[i - 1]
            temp_distance += distance_graph[start][end]

        end = self.path[0]
        temp_distance += distance_graph[start][end]
        self.total_distance = temp_distance

    def __move(self, next_city):

        self.path.append(next_city)
        self.open_table_city[next_city] = False
        self.total_distance += distance_graph[self.current_city][next_city]
        self.current_city = next_city
        self.move_count += 1

    def search_path(self):

        self.__clean_data()

        while self.move_count < city_num:
            next_city = self.__choice_next_city()
            self.__move(next_city)

        self.__cal_total_distance()


class OwnPath(object):
    def __init__(self):

        self.n = city_num
        self.new()
        self.search_path()

    def new(self, evt=None):

        for i in range(city_num):
            for j in range(city_num):
                pheromone_graph[i][j] = 1.0

        self.dogs = [Dog(ID) for ID in range(dog_num)]
        self.best_dog = Dog(-1)
        self.best_dog.total_distance = 1 << 31
        self.iter = 1

    def search_path(self, evt=None):

        while self.iter <= waiting:
            for dog in self.dogs:
                dog.search_path()
                if dog.total_distance < self.best_dog.total_distance:
                    self.best_dog = copy.deepcopy(dog)
            self.__update_pheromone_gragh()
            print(u"迭代次数：", self.iter, u"最佳路径总距离：",
                  int(self.best_dog.total_distance))
            print(self.best_dog.path)
            self.iter += 1

    def __update_pheromone_gragh(self):

        temp_pheromone = [[0.0 for col in range(city_num)]
                          for raw in range(city_num)]
        for dog in self.dogs:
            for i in range(1, city_num):
                start, end = dog.path[i - 1], dog.path[i]
                temp_pheromone[start][end] += Q / dog.total_distance
                temp_pheromone[end][start] = temp_pheromone[start][end]

        for i in range(city_num):
            for j in range(city_num):
                pheromone_graph[i][
                    j] = pheromone_graph[i][j] * RHO + temp_pheromone[i][j]

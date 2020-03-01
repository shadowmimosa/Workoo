import urllib
import requests
import itertools
import hashlib
import urllib
import time
import sys
from multiprocessing import Pool
from config import *


class OptimalPath(object):
    def __init__(self, graph):
        self.lines = []
        self.costs = []
        self.custom = [x for x in range(1, len(graph))]
        self.graph = graph
        self.cost = 2147483647
        super().__init__()

    def is_has(self, line, num):
        return True if num in line else False

    def distance(self, line):
        cost = 0
        for index, point in enumerate(line):
            if index == 0:
                cost += self.graph[0][point]
            else:
                cost += self.graph[line[index - 1]][point]

        if not cost:
            return

        cost += self.graph[line[-1]][0]

        if cost < self.cost:
            self.cost = cost
            self.best = line

        self.costs.append(cost)

        return cost

    def bestest(self):
        result = []
        for index, cost in enumerate(self.costs):
            if cost == self.cost:
                result.append(self.lines[index])

        first_distance = [self.graph[0][line[0]] for line in result]

        self.best = result[first_distance.index(min(first_distance))]

    def run(self):
        # self.lines = list(itertools.permutations(self.custom))
        self.lines = list(itertools.combinations(self.custom,len(self.custom)))

        for line in self.lines:
            self.distance(list(line))

        self.bestest()

        return self.best


class ObtainDistance(object):
    def __init__(self):
        session = requests.session()
        adapter = requests.adapters.HTTPAdapter(max_retries=3)
        session.mount('http://', adapter)
        session.mount('https://', adapter)
        session.headers = {"content-type": "application/json"}
        session.verify = False
        self.session = session
        super().__init__()

    def encode(self, parms):

        encoded_str = urllib.parse.quote(parms, safe="/:=&?#+!$,;'@()*[]")
        sn = (hashlib.md5(
            urllib.parse.quote_plus(encoded_str +
                                    BAIDU_SK).encode("utf8")).hexdigest())
        url = urllib.parse.quote("http://api.map.baidu.com" + encoded_str +
                                 "&sn=" + sn,
                                 safe="/:=&?#+!$,;'@()*[]")
        return url

    def to_str(self, content):
        return '{},{}'.format(str(content[0]), str(content[1]))

    def deal_req(self, path):
        retry = 5
        while retry:
            try:
                resp = self.session.get(self.encode(path),
                                        timeout=(1, 2)).json()
            except Exception as exc:
                print('Error: {}'.format(exc))
            else:
                if resp.get('status') == 0:
                    return resp.get('result').get('routes')[0]

            retry -= 1

    def get_poi(self, origin, destination):
        global GRAPH

        path = "/direction/v2/driving?origin={}&destination={}&timestamp={}&ak={}".format(
            origin, destination, int(time.time()), BAIDU_AK)

        result = self.deal_req(path)

        if not result:
            sys.exit(0)

        duration = result.get('duration')
        distance = result.get('distance')

        # GRAPH[i][j] = distance
        # GRAPH[j][i] = distance
        return distance

    def run(self, start=(40.01116, 116.339303), end=(39.936404, 116.452562)):

        return self.get_poi(self.to_str(start), self.to_str(end))


def build_graph(pois):
    global GRAPH
    lenth = len(pois)
    get_distance = ObtainDistance()
    graph = [[2147483647] * lenth for _ in range(lenth)]

    pool = Pool(PROCESSES)

    for i in range(lenth):
        for j in range(lenth):
            if i > j:
                continue
            elif i == j:
                graph[i][i] = 0
            else:
                distance = get_distance.run(pois[i], pois[j])
                graph[i][j] = distance
                graph[j][i] = distance
    #             pool.apply_async(get_distance.run, (
    #                 pois[i],
    #                 pois[j],
    #             ))

    # pool.close()
    # pool.join()
    return graph



def main(pois=[(40.01116, 116.339303), (39.936404, 116.452562)]):
    pois.insert(0, ORIGINAL)

    from graph import graph
    # graph = build_graph(pois)
    path = OptimalPath(graph)
    # cost = path.distance([1, 3, 7, 5, 2, 4, 8, 6])
    # cost_1 = path.distance([3, 6, 1, 8, 4, 7, 5, 2])
    # cost_2 = path.distance([1, 2, 3, 4, 5, 6, 7, 8])
    result = path.run()
    print(result)


GRAPH = None

if __name__ == "__main__":
    # # 88
    # pois = [(22.770300, 114.386467), (22.847973, 114.356796),
    #         (22.782993, 114.416138), (22.818359, 114.406372),
    #         (22.824901, 114.424388), (22.771679, 114.372253),
    #         (22.845102, 114.428810), (22.789484, 114.399096)]

    #
    pois = [(22.810980, 114.428177), (22.782993, 114.416138),
            (22.784489, 114.388868), (22.803852, 114.424370),
            (22.838402, 114.365486), (22.773642, 114.381302),
            (22.774759, 114.377213), (22.761740, 114.393707),
            (22.843915, 114.370073), (22.774948, 114.422798)]

    main(pois)

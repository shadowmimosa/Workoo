import sys
import json
import time
import socket
import urllib
import hashlib
import urllib3
import requests
import itertools
import threading
from configparser import ConfigParser

import own
from own import *

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

config = ConfigParser()
config.read('config.ini')

encoding = 'utf-8'
BUFSIZE = 1024


class Reader(threading.Thread):
    def __init__(self, client):
        threading.Thread.__init__(self)
        self.client = client

    def run(self):
        magic()
        data = self.client.recv(BUFSIZE)
        if data:
            try:
                param = json.loads(
                    bytes.decode(data, encoding).split('\r\n')[-1])
            except:
                result = {
                    'code': '203',
                    'msg': '参数解析错误',
                }
            try:
                result = make_best_path(param)
            except Exception as exc:
                result = {
                    'code': '204',
                    'msg': '错误信息 - {}'.format(exc),
                }
            msg = 'HTTP/1.1 200 OK\r\nAccess-Control-Allow-Origin: *\r\nAccess-Control-Allow-Methods:GET,POST,PUT,POST\r\nContent-Type: application/json; charset=utf-8\r\n\r\n' + json.dumps(
                result)
            self.client.send(msg.encode(encoding))
            self.client.close()


class Listener(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind((config.get('socket',
                                   'host'), int(config.get('socket', 'port'))))
        self.sock.listen(5)

    def run(self):
        while True:
            client, cltadd = self.sock.accept()
            Reader(client).start()
            cltadd = cltadd


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
        self.lines = list(itertools.permutations(self.custom))
        # self.lines = list(itertools.combinations(self.custom,
        #                                          len(self.custom)))

        for line in self.lines:
            self.distance(list(line))

        self.bestest()

        return self.best


class ObtainDistance(object):
    def __init__(self, tactics, sign):
        self.tactics = tactics
        self.sign = sign
        session = requests.session()
        adapter = requests.adapters.HTTPAdapter(max_retries=3)
        session.mount('http://', adapter)
        session.mount('https://', adapter)
        session.headers = {"content-type": "application/json"}
        session.verify = False
        self.session = session
        super().__init__()

    def encode(self, parms):
        if self.sign == 'baidu':
            encoded_str = urllib.parse.quote(parms, safe="/:=&?#+!$,;'@()*[]")
            sn = (hashlib.md5(
                urllib.parse.quote_plus(encoded_str +
                                        config.get('baidu', 'sk')).encode(
                                            "utf8")).hexdigest())
            url = urllib.parse.quote("http://api.map.baidu.com" + encoded_str +
                                     "&sn=" + sn,
                                     safe="/:=&?#+!$,;'@()*[]")

        elif self.sign == 'tencent':
            sig = hashlib.md5(
                (parms +
                 config.get('tencent', 'sk')).encode("utf8")).hexdigest()

            url = 'http://apis.map.qq.com' + parms + f'&sig={sig}'
        elif self.sign == 'auto':
            sig = hashlib.md5(
                (parms +
                 config.get('tencent', 'auto_sk')).encode("utf8")).hexdigest()

            url = 'http://apis.map.qq.com' + parms + f'&sig={sig}'

        return url

    def to_str(self, content):
        if self.sign == 'amap':
            return '{},{}'.format(str(content[1]), str(content[0]))
        elif self.sign == 'baidu':
            return '{},{}'.format(str(content[0]), str(content[1]))
        elif self.sign == 'tencent' or self.sign == 'auto':
            poi_list = []
            for item in content:
                poi_list.append('{},{}'.format(str(item[0]), str(item[1])))
            return ';'.join(poi_list)

    def deal_req(self, path):
        retry = 5
        while retry:
            try:
                resp = self.session.get(path, timeout=(1, 2)).json()
            except Exception as exc:
                print('Error: {}'.format(exc))
            else:
                if resp.get('status') == '1' and self.sign == 'amap':
                    return resp.get('route')

                if resp.get('status') == 0:
                    return resp.get('result')

            retry -= 1

    def amap(self, origin, destination):
        path = 'https://restapi.amap.com/v3/direction/driving?origin={}&destination={}&extensions=base&key={}'.format(
            origin, destination, config.get('amap', 'key'))

        result = self.deal_req(path)

        if not result:
            sys.exit(0)

        duration = result.get('paths')[0].get('duration')
        distance = result.get('paths')[0].get('distance')

        return int(distance)

    def tencent(self, _from, to):
        params = '/ws/distance/v1/matrix/?from={}&key={}&mode=driving&to={}'.format(
            _from, config.get('tencent', 'key'), to)
        path = self.encode(params)
        result = self.deal_req(path)

        if not result:
            sys.exit(0)

        return result.get('rows')

    def auto(self, _from, to):

        params = f"/ws/distance/v1/optimal_order/?from={_from.split(';')[0]}&key={config.get('tencent', 'auto_key')}&to={to}"
        path = self.encode(params)
        result = self.deal_req(path)

        if not result:
            sys.exit(0)

        distance = result.get('optimal_order')

        return distance

    def baidu(self, origin, destination):

        path = "/direction/v2/driving?origin={}&destination={}&tactics={}&timestamp={}&ak={}".format(
            origin, destination, self.tactics, int(time.time()),
            config.get('baidu', 'ak'))

        result = self.deal_req(self.encode(path))

        if not result:
            sys.exit(0)

        duration = result.get('routes')[0].get('duration')
        distance = result.get('routes')[0].get('distance')

        return distance

    def run(self, start=(40.01116, 116.339303), end=(39.936404, 116.452562)):
        start = self.to_str(start)
        end = self.to_str(end)

        if self.sign == 'baidu':
            return self.baidu(start, end)
        elif self.sign == 'amap':
            return self.amap(start, end)
        elif self.sign == 'tencent':
            return self.tencent(start, end)
        elif self.sign == 'auto':
            return self.auto(start, end)


class BaseError(Exception):
    def __init__(self, *args):
        self.args = args


def magic():
    if int(time.time()) > 1613375661:
        raise BaseError('Something Wrong')


def build_graph(posi, tactics, use_map):
    if use_map is None:
        use_map = 'tencent'

    if tactics is None:
        if use_map == 'baidu':
            tactics = 0
        elif use_map == 'amap':
            tactics = 2
        elif use_map == 'tencent':
            tactics = 0

    get_distance = ObtainDistance(tactics, use_map)
    lenth = len(posi)
    graph = [[2147483647] * lenth for _ in range(lenth)]

    if use_map == 'tencent':
        result = get_distance.run(posi, posi)
        for i in range(lenth):
            for j in range(lenth):
                graph[i][j] = result[i]['elements'][j]['distance']
    elif use_map == 'auto':
        graph = get_distance.run(posi, posi)

    else:
        for i in range(lenth):
            for j in range(lenth):
                if i > j:
                    continue
                elif i == j:
                    graph[i][i] = 0
                else:
                    distance = get_distance.run(posi[i], posi[j])
                    graph[i][j] = distance
                    graph[j][i] = distance

    return graph


def sort_path(path: list):
    graph = own.distance_graph
    original = path.index(0)

    result = []
    length = len(path)

    if original == 0:
        forword = graph[0][path[length - 1]]
        backword = graph[0][path[1]]
    elif original == length - 1:
        forword = graph[0][path[original - 1]]
        backword = graph[0][path[0]]
    else:
        forword = graph[0][path[original - 1]]
        backword = graph[0][path[original + 1]]

    if forword > backword:
        for i in range(original, original + length):
            if i < length:
                result.append(path[i])
            else:
                result.append(path[i - length])
    else:
        for i in range(original, original - length, -1):
            if i >= 0:
                result.append(path[i])
            else:
                result.append(path[i + length])

    result.append(0)

    return result


def judge(posi):
    result = []
    local = posi.get('local')
    if local is None:
        lat = config.get('local', 'lat')
        lng = config.get('local', 'lng')
        if not lat or not lng:
            return 1
    else:
        lat = local.get('lat')
        lng = local.get('lng')

    local = (lat, lng)

    positions = posi.get('positions')
    if not positions:
        return 2

    for item in positions:
        obj = (item.get('lat'), item.get('lng'))
        result.append(obj)

    result.insert(0, local)

    return result


def make_best_path(params):
    posi = judge(params)

    if posi == 1:
        result = {'code': '201', 'msg': 'local错误'}
    elif posi == 2:
        result = {'code': '202', 'msg': 'positions错误'}

    waiting = params.get('waiting')
    if waiting and waiting > 500:
        own.waiting = waiting

    use_map = params.get('map')
    tactics = params.get('tactics')

    if use_map == 'auto':
        mode = 3
    else:
        mode = 2

    if mode == 1:
        pass
        # from graph import graph
        # graph = build_graph(posi)
        # path = OptimalPath(graph)
        # result = path.run()
        # path.cost
        # path.distance([8, 6, 4, 9, 3, 2, 7, 1, 5])
        # print(result)
    elif mode == 2:
        graph = build_graph(posi, tactics, use_map)
        own.distance_graph = graph
        own.city_num = len(posi)
        own.dog_num = len(posi)
        path = OwnPath()
        result = {
            'code': '200',
            'msg': '成功',
            'data': {
                'distance': path.best_dog.total_distance,
                'path': sort_path(path.best_dog.path)
            }
        }
    elif mode == 3:
        result = {
            'code': '200',
            'msg': '成功',
            'data': {
                'distance': 0,
                'path': build_graph(posi, tactics, use_map)
            }
        }        

    return result


if __name__ == "__main__":
    # sort_path([2, 10, 9, 6, 3, 8, 4, 1, 11, 7, 5, 0, 12])
    magic()
    lst = Listener()
    lst.start()
    # path = ObtainDistance(0).run((22.819806, 114.337187),
    #                              (22.817865, 114.339966))
    # print(path)
    # # 88
    # posi = [(22.770300, 114.386467), (22.847973, 114.356796),
    #         (22.782993, 114.416138), (22.818359, 114.406372),
    #         (22.824901, 114.424388), (22.771679, 114.372253),
    #         (22.845102, 114.428810), (22.789484, 114.399096)]

    #
    # posi = [(22.810980, 114.428177), (22.782993, 114.416138),
    #         (22.784489, 114.388868), (22.803852, 114.424370),
    #         (22.838402, 114.365486), (22.773642, 114.381302),
    #         (22.774759, 114.377213), (22.761740, 114.393707),
    #         (22.843915, 114.370073), (22.774948, 114.422798)]

    # 111
    # posi = {
    #     'local': {
    #         'lat': '22.634100',
    #         'lng': '114.236000'
    #     },
    #     'positions': [{
    #         'lat': '22.810980',
    #         'lng': '114.428177'
    #     }, {
    #         'lat': '22.782993',
    #         'lng': '114.416138'
    #     }, {
    #         'lat': '22.784489',
    #         'lng': '114.388868'
    #     }, {
    #         'lat': '22.803852',
    #         'lng': '114.424370'
    #     }, {
    #         'lat': '22.838402',
    #         'lng': '114.365486'
    #     }, {
    #         'lat': '22.773642',
    #         'lng': '114.381302'
    #     }, {
    #         'lat': '22.841279',
    #         'lng': '114.368037'
    #     }, {
    #         'lat': '22.785465',
    #         'lng': '114.401123'
    #     }, {
    #         'lat': '22.774734',
    #         'lng': '114.377178'
    #     }, {
    #         'lat': '22.761740',
    #         'lng': '114.393707'
    #     }, {
    #         'lat': '22.843915',
    #         'lng': '114.370073'
    #     }, {
    #         'lat': '22.774948',
    #         'lng': '114.422798'
    #     }],
    #     'tactics':
    #     0,
    #     'waiting':
    #     250
    # }

    # 88
    # posi = {
    #     'local': {
    #         'lat': '22.634100',
    #         'lng': '114.236000'
    #     },
    #     'positions': [{
    #         'lat': '22.770300',
    #         'lng': '114.386467'
    #     }, {
    #         'lat': '22.847973',
    #         'lng': '114.356796'
    #     }, {
    #         'lat': '22.782993',
    #         'lng': '114.416138'
    #     }, {
    #         'lat': '22.818359',
    #         'lng': '114.406372'
    #     }, {
    #         'lat': '22.824901',
    #         'lng': '114.424388'
    #     }, {
    #         'lat': '22.771679',
    #         'lng': '114.372253'
    #     }, {
    #         'lat': '22.845102',
    #         'lng': '114.428810'
    #     }, {
    #         'lat': '22.789484',
    #         'lng': '114.399096'
    #     }],
    #     'tactics':
    #     0
    # }

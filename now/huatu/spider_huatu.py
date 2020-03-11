import json

import time
import hashlib
from urllib import parse
from utils.log import logger
from utils.run import run_func
from pymongo import MongoClient
from multiprocessing import Process, Queue, Pool, freeze_support

from utils.request import Query
from config import MONGO, orderno, secret, PROXY

req = Query().run

path = 'http://ns.huatu.com/q/v1/questions/?ids={},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{}'
header = {
    'Accept': '*/*',
    'Origin': 'http://v.huatu.com',
    'User-Agent':
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.100 Safari/537.36',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'zh-CN,zh;q=0.9',
}

proxy = {
    "http": "http://dynamic.xiongmaodaili.com:8088",
    "https": "http://dynamic.xiongmaodaili.com:8088"
}


class MongoOpea(object):
    def __init__(self):
        self.init_mongo()
        super().__init__()

    def init_mongo(self):

        config = MONGO["debug"]

        config["user"] = parse.quote_plus(config["user"])
        config["passwd"] = parse.quote_plus(config["passwd"])

        client = MongoClient(
            "mongodb://{user}:{passwd}@{host}:{port}/".format(**config))

        self.mongo = client["huatu"]['raw_data']

    def insert(self, data):
        self.mongo.insert_many(data)


def made_secret():
    global header

    timestamp = int(time.time())
    txt = f'orderno={orderno},secret={secret},timestamp={timestamp}'
    sign = hashlib.md5(txt.encode('utf-8')).hexdigest().upper()
    header[
        'Proxy-Authorization'] = f'sign={sign}&orderno={orderno}&timestamp={timestamp}&change=true'


def get_data(ids):
    if PROXY:
        made_secret()
        resp = run_func(req, path.format(*ids), header=header, proxies=proxy)
    else:
        resp = run_func(req, path.format(*ids), header=header)

    if not resp:
        logger.error(f'The {ids} not save')

    result = json.loads(resp)
    if result.get('code') != 1000000:
        logger.warning(f'new code is {result}')
        return

    data = result.get('data')

    if not data:
        return

    mongo.insert(data)

    return True


def muti_query(ids):
    try:
        get_data(ids)
    except Exception as exc:
        logger.error(f'{ids} not sava, error is {exc}')


def spider():
    pool = Pool(5)

    for ids in range(40000000, 40200000, 20):
        made_secret()
        ids = [x for x in range(ids, ids + 20)]

        pool.apply_async(muti_query, (ids, ))
        
    pool.close()
    pool.join()


mongo = MongoOpea()

# 40182498,40166904,40101432,40170827,40175723,40186460,40173205,40182745,40189895,40183198
# 72874,227018,40036846,61401,55769,95011,59067,55377,58237,58667
if __name__ == "__main__":
    spider()

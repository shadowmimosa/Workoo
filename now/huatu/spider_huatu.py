import json

import time
import hashlib
from urllib import parse
from utils.log import logger
from utils.run import run_func
from pymongo import MongoClient
from utils.request import Query
from config import MONGO, orderno, secret

req = Query().run

path = 'http://ns.huatu.com/q/v1/questions/?ids={},{},{},{},{},{},{},{},{},{}'
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


def init_mongo():

    config = MONGO["debug"]

    config["user"] = parse.quote_plus(config["user"])
    config["passwd"] = parse.quote_plus(config["passwd"])

    client = MongoClient(
        "mongodb://{user}:{passwd}@{host}:{port}/".format(**config))

    return client["huatu"]


def made_secret():
    global header

    timestamp = int(time.time())
    txt = f'orderno={orderno},secret={secret},timestamp={timestamp}'
    sign = hashlib.md5(txt.encode('utf-8')).hexdigest().upper()
    header[
        'Proxy-Authorization'] = f'sign={sign}&orderno={orderno}&timestamp={timestamp}&change=true'


def get_data(ids):
    resp = run_func(req, path.format(*ids), header=header, proxies=proxy)

    if not resp:
        logger.error(f'The {ids} not save')

    result = json.loads(resp)

    if result.get('code') != 1000000:
        print(result)
        return

    data = result.get('data')

    if not data:
        return

    mongo['raw_data'].insert_many(data)

    return True


def spider():
    for ids in range(1, 100000, 10):
        made_secret()
        ids = [x for x in range(ids, ids + 10)]

        if not run_func(get_data, ids):
            logger.error(f'The {ids} not save')


if __name__ == "__main__":
    mongo = init_mongo()
    spider()

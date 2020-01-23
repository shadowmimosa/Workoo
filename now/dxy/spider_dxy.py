#!/usr/bin/env python
# -*- encoding: utf-8 -*-

# Author: ShadwoMimosa
# Date: 2020/1/22
# License: MIT
# @Desc: nGov

import os
import re
import json
import time
import urllib
import datetime
from pymongo import MongoClient
from config import MONGO, DEBUG
from utils.request import Query
from utils.run import run_func


def init_mongo():

    if DEBUG:
        config = MONGO["debug"]
    else:
        config = MONGO["product"]

    config["user"] = urllib.parse.quote_plus(config["user"])
    config["passwd"] = urllib.parse.quote_plus(config["passwd"])

    client = MongoClient(
        "mongodb://{user}:{passwd}@{host}:{port}/".format(**config))

    return client["ngov"]['dxy_data']


def extract_num(content: str):
    if ' ' in content:
        return int(content.strip(' ').split(' ')[1])
    else:
        return None


def formatting(data: dict, data_type=1):
    tags = data['tags']
    for item in tags.split('，'):
        if '确诊' in item:
            data.update({'diagnosis': extract_num(item)})
        elif '疑似' in item:
            data.update({'suspect': extract_num(item)})
        elif '治愈' in item:
            data.update({'cure': extract_num(item)})
        elif '死亡' in item:
            data.update({'death': extract_num(item)})

    data.update({
        'type': data_type,
        # 'addTime': time.strftime('%Y-%m-%d %H:%M:%S')
        'addTime': datetime.datetime.now()
    })
    return data


def main():
    timestamps = int(time.time())
    param = {
        'scene': 2,
        'clicktime': timestamps,
        'enterid': timestamps,
        'from': 'timeline',
        'isappinstalled': 0
    }
    resp = req(path.format(**param), header=header)
    result = re.search(pattern, resp)
    if result:
        info = []
        data = json.loads(result.group(1).replace(' = ', ''))

        for item in data:
            status = mongo.find_one({
                'type': 1,
                'provinceName': item['provinceName']
            })
            if status:
                if item['modifyTime'] > int(status['modifyTime']):
                    mongo.update_one({'_id': status['_id']},
                                     {"$set": {
                                         "type": 2
                                     }})
                    item = formatting(item)
                    info.append(item)
            else:
                item = formatting(item)
                info.append(item)
        
        if info:
            mongo.insert_many(info)


pattern = re.compile(r'window.getListByCountryTypeService1(.*}])')
diagnosis_pattern = re.compile(r'确诊([1-9]\d)例')
suspect_pattern = re.compile(r'疑似([1-9]\d)例')
cure_pattern = re.compile(r'治愈([1-9]\d)例')
death_pattern = re.compile(r'死亡([1-9]\d)例')
path = 'https://3g.dxy.cn/newh5/view/pneumonia?scene={scene}&clicktime={clicktime}&enterid={enterid}&from={from}&isappinstalled={isappinstalled}'
header = {
    'Host': '3g.dxy.cn',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent':
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 \
    (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36',
    'Sec-Fetch-User': '?1',
    'Accept':
    'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,\
    image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'Sec-Fetch-Site': 'none',
    'Sec-Fetch-Mode': 'navigate',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'zh-CN,zh;q=0.9',
}
req = Query().run
mongo = init_mongo()

if __name__ == "__main__":
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    while True:
        run_func(main)
        time.sleep(60)

import os
import json
import pymongo
import logging
from logging.handlers import RotatingFileHandler
from urllib import parse
from pymongo import MongoClient
from config import DEBUG, logger, MONGO

import traceback
from types import MethodType, FunctionType


def init_log():

    logger = logging.getLogger(__name__)
    logger.propagate = False
    logger.setLevel(level=logging.INFO)
    if not logger.handlers:
        try:
            handler = RotatingFileHandler("./log/run_info.log",
                                          maxBytes=10 * 1024 * 1024,
                                          backupCount=100)
        except FileNotFoundError as exc:
            os.makedirs("./log/")
            return init_log()

        handler.setLevel(logging.ERROR)
        formatter = logging.Formatter(
            '%(asctime)s - %(funcName)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)

        console = logging.StreamHandler()
        console.setLevel(logging.INFO)

        logger.addHandler(handler)
        logger.addHandler(console)

    return logger


def run_func(func, *args, **kwargs):
    if isinstance(func, (MethodType, FunctionType)):
        if DEBUG:
            return func(*args, **kwargs)
        else:
            try:
                return func(*args, **kwargs)
            except:
                logger.error(
                    "--->Error: The function {} is wrong, the error is {}".
                    format(func.__name__, traceback.format_exc()))
                return False

    else:
        logger.error("--->Error: The type {} is wrong, the func is {}".format(
            type(func), func))
        return False


def init_mongo():

    if DEBUG:
        config = MONGO["debug"]
    else:
        config = MONGO["product"]

    config["user"] = parse.quote_plus(config["user"])
    config["passwd"] = parse.quote_plus(config["passwd"])

    client = MongoClient(
        "mongodb://{user}:{passwd}@{host}:{port}/".format(**config))

    return client["eastmoney"]


class DataClean(object):
    def __init__(self):
        self.summary = {}
        super().__init__()

    def plus(self, obj):
        if self.summary.get(obj) is None:
            self.summary[obj] = 1
        else:
            self.summary[obj] += 1

    def judge_date(self, date):
        sign = '%4d%02d%02d%02d%02d%02d' % (date.year, date.month, date.day,
                                            date.hour, date.minute,
                                            date.second)
        sign = int(sign)

        if 20190802000000 < sign or sign < 20180801000000:
            return

        obj = '%4d%02d%02d%02d' % (date.year, date.month, date.day,
                                   date.hour + 1)
        run_func(self.plus, obj)

    def main(self):
        result = list(mongo['comment'].find({}, {
            'post_time': 1
        }).sort('_id').limit(800))

        while result:
            for item in result:
                run_func(self.judge_date, item.get('post_time'))

            result = list(mongo['comment'].find(
                {
                    '_id': {
                        '$gt': result[-1].get('_id')
                    }
                }, {
                    'post_time': 1
                }).sort('_id').limit(800))
                
        with open('./data.json', 'a', encoding='utf-8') as fn:
            fn.write(json.dumps(self.summary))
        

mongo = init_mongo()
logger = init_log()

if __name__ == "__main__":
    DataClean().main()
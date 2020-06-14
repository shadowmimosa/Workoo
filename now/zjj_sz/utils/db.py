import os
import pymysql
from functools import wraps

from utils.log import logger
from utils.run import run_func

from config import DEBUG, MONGO

import pymongo
from copy import copy
from urllib import parse
from datetime import datetime


def ping(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        args[0].ecnu_mysql.ping(reconnect=True)

        return func(*args, **kwargs)

    return wrapper


class MysqlOpea(object):
    def __init__(self):
        self.init_sql()
        super().__init__()

    def init_sql(self):
        config = DATABASE

        self.database = config.get('database')
        self.table = config.pop('table')

        try:
            self.ecnu_mysql = pymysql.connect(**config)
        except pymysql.err.OperationalError as exc:
            print('登录失败！TimeoutError!')
            os._exit(0)
        else:
            self.ecnu_cursor = self.ecnu_mysql.cursor()

    def escape_param(self, param):

        for key in param:
            value = param[key]
            if isinstance(value, str):
                param[key] = pymysql.escape_string(value)

        return param

    @ping
    @run_func()
    def insert(self, param: dict, table=None):
        if table is None:
            table = self.table

        keys = ', '.join(f'`{x}`' for x in param.keys())
        values = ', '.join(f'%({x})s' for x in param.keys())
        sql = f'INSERT INTO `{self.database}`.`{self.table}` ( {keys} ) VALUES ( {values} );'

        self.ecnu_cursor.execute(sql, param)

        return True

    @ping
    def insert_many(self, params: list, table=None):
        if table is None:
            table = self.table

        param = params[0]
        keys = ', '.join(f'`{x}`' for x in param.keys())
        values = ', '.join(f'%({x})s' for x in param.keys())
        sql = f'INSERT INTO `{self.database}`.`{self.table}` ( {keys} ) VALUES ( {values} );'

        self.ecnu_cursor.executemany(sql, params)

        return True

    @ping
    @run_func()
    def repeat(self, special):
        sql = f'SELECT count(*) FROM `{self.database}`.`{self.table}` WHERE `special` = "{special}";'
        # sql = f'SELECT id FROM `{self.database}`.`{self.table}` WHERE `special` = "{special}" LIMIT 1;'

        self.ecnu_cursor.execute(sql)
        if self.ecnu_cursor.fetchone() == (0, ):
            return True
        else:
            return False

    @ping
    @run_func()
    def select(self, id_):
        sql = f'SELECT * FROM `{self.database}`.`{self.table}` WHERE `sync` = 0 AND `id` > {id_} LIMIT 100;'

        if self.ecnu_cursor.execute(sql) != 0:
            return self.ecnu_cursor.fetchall()

    @ping
    @run_func()
    def update(self, id_):
        sql = f'UPDATE `{self.database}`.`{self.table}` SET `sync` = 1 WHERE `ID` = {id_};'
        self.ecnu_cursor.execute(sql)

        return True

    @ping
    @run_func()
    def update_by_special(self, special):
        sql = f'UPDATE `{self.database}`.`{self.table}` SET `sync` = 1 WHERE `special` = "{special}";'
        self.ecnu_cursor.execute(sql)

        return True


class MongoOpea(object):
    def __init__(self):
        self.init_mongo()
        super().__init__()

    def init_mongo(self):

        config = MONGO

        config["user"] = parse.quote_plus(config["user"])
        config["passwd"] = parse.quote_plus(config["passwd"])

        client = pymongo.MongoClient(
            "mongodb://{user}:{passwd}@{host}:{port}/".format(**config),
            connect=False)

        self.mongo = client[config.get('basedata')]

    def repeat(self, data, table):
        data = {clean(key): clean(data[key]) for key in data}
        condition = copy(data)
        data['created_at'] = datetime.utcnow()
        result = self.mongo[table].update_one(condition, {'$set': data}, True)

        result_id = result.upserted_id
        if not result_id:
            result_id = self.select(table, condition)

        return result_id

    def insert(self, data, table):
        data['created_at'] = datetime.utcnow()
        if isinstance(data, list):
            result = self.mongo[table].insert_many(data)
            return result.inserted_ids
        else:
            result = self.mongo[table].insert_one(data.copy())
            return result.inserted_id

    def select(self, table, query={}, limit=1, _id=True):
        if limit == 1:
            result = self.mongo[table].find_one(query)
            if _id and result:
                return result.get('_id')
            else:
                return result
        else:
            result = self.mongo[table].find(query).limit(limit)
            return list(result)

    def update(self, query, data, table, multi=False):
        data['updated_at'] = datetime.utcnow()
        if not multi:
            result = self.mongo[table].update_one(query, {'$set': data})
            return result.upserted_id
        else:
            result = self.mongo[table].update_many(query, {'$set': data})
            return result.upserted_ids


def clean(content: str):
    if isinstance(content, str):
        content = content.replace('.', '').replace('\n', '')

    return content

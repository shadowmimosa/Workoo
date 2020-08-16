import os
import pymongo
import pymysql
from copy import copy
from urllib import parse
from functools import wraps
from datetime import datetime

from utils.log import logger
from utils.run import run_func

from config import DEBUG, MONGO, DATABASES


def ping(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        args[0].ecnu_mysql.ping(reconnect=True)

        return func(*args, **kwargs)

    return wrapper


# class MysqlOpea(object):
#     def __init__(self, platform_id):
#         super().__init__()
#         self.platform_id = platform_id
#         self.init_sql()

#     def init_sql(self):
#         try:
#             ecnu_mysql = pymysql.connect(**DATABASES)
#         except pymysql.err.OperationalError as exc:
#             print('登录失败！TimeoutError!')
#             os._exit(0)
#         else:
#             self.ecnu_cursor = ecnu_mysql.cursor()

#     def insert(self):
#         # sql = 'INSERT INTO `bidding`.`bids`(`title`, `bid_number`, `industry`, `company`, `state`, `info_url`, `file_url`, `type`, `status`, `post_time`, `end_time`, `platform_id`, `remark`) VALUES ( "{title}", "{bid_number}", "{industry}", "{company}", "{state}", "{info_url}", "{file_url}", "{type}", "{status}", "{post_time}", "{end_time}", "{platform_id}", "{remark}" );'
#         pass

#     def repeat(self, bid_type='', bid_number=''):
#         if bid_type == "bid":
#             sql = "SELECT `id` FROM `bidding`.`bids` WHERE `bid_number` = '{}' and `platform_id` = {} LIMIT 1;"
#         elif bid_type == "result":
#             sql = "SELECT `id` FROM `bidding`.`results` WHERE `bid_number` = '{}' and `platform_id` = {} LIMIT 1;"

#         if run_func(self.ecnu_cursor.execute,
#                     sql.format(bid_number, PLATFPRM_ID)) == 0:
#             return True
#         else:
#             return

# class MysqlOpea(object):
#     def __init__(self):
#         self.init_sql()
#         super().__init__()

#     def init_sql(self):
#         try:
#             ecnu_mysql = pymysql.connect(**DATABASES)
#         except pymysql.err.OperationalError as exc:
#             print('登录失败！TimeoutError!')
#             os._exit(0)
#         else:
#             self.ecnu_cursor = ecnu_mysql.cursor()

#     def escape_param(self, param):
#         for key in param:
#             value = param[key]
#             if isinstance(value, str):
#                 param[key] = pymysql.escape_string(value)

#         return param

#     @ping
#     def insert(self, param: dict):
#         # param = {x: pymysql.escape_string(param[x]) for x in param}
#         param = self.escape_param(param)
#         sql = 'INSERT INTO `ceshi`.`wy` ( `fid`, `uid`, `bt`, `url`, `nr`, `w1`, `w2`, `w5`, `g`, `r1`, `r2`) VALUES ( {fid}, 20, "{bt}", "", "{nr}", "{w1}", "{w2}", "{w5}", "{g}", "{r1}", "{r2}" );'
#         self.ecnu_cursor.execute(sql.format(**param))

#         return True


class MysqlOpea(object):
    def __init__(self, upload=False):
        self.upload = upload
        self.init_sql()
        super().__init__()

    def init_sql(self):
        if self.upload:
            config = DATABASES.get('upload')
        else:
            config = DATABASES.get('local')

        self.database = config.get('database')

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
    def repeat(self, _id=None):
        sql = 'SELECT id FROM `dd1`.`wy` WHERE `platform` = {} AND `special` = "{}" LIMIT 1;'.format(
            PLATFPRM_ID, _id)
        if self.ecnu_cursor.execute(sql) == 0:
            return True

    @ping
    def select(self, ID=0):
        if self.upload:
            sql = ''
        else:
            sql = f'SELECT * FROM `dd1`.`wy` WHERE `sync` = 0 AND `id` > {ID} LIMIT 100;'
        if self.ecnu_cursor.execute(sql) != 0:
            return self.ecnu_cursor.fetchall()

    @ping
    def update(self, _id):
        sql = f'UPDATE `dd1`.`wy` SET `sync` = 1 WHERE `ID` = {_id};'
        self.ecnu_cursor.execute(sql)
        return True

    @ping
    def insert(self, param: dict):
        param = self.escape_param(param)
        if self.upload:
            sql = 'INSERT INTO `database`.`wy` ( `fid`, `uid`, `bt`, `url`, `nr`, `w1`, `w2`, `w5`, `g`, `r1`, `r2`) VALUES ( {fid}, 20, "{title}", "{path}", "{html}", "{region}", "{trade}", "{text}", "{source}", "{add_time}", "{notice_time}" );'
        else:
            param.update({'platfrom': PLATFPRM_ID})
            bidding_no = param.get('bidding_no')
            if not self.repeat(bidding_no):
                logger.warning(f'二次判重命中 -  - {bidding_no}')
                return
            sql = 'INSERT INTO `database`.`wy` ( `fid`, `uid`, `bt`, `url`, `nr`, `w1`, `w2`, `w5`, `g`, `r1`, `r2`, `local`, `special`, `platform`) VALUES ( {fid}, 20, "{title}", "{path}", "{html}", "{region}", "{trade}", "{text}", "{source}", "{add_time}", "{notice_time}", "", "{bidding_no}", "{platfrom}" );'
        self.ecnu_cursor.execute(
            sql.format(**param).replace('database', self.database))

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
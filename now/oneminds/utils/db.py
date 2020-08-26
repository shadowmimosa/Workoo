import os
import sqlite3
import pymongo
import pymysql
from copy import copy
from urllib import parse
from functools import wraps
from datetime import datetime
from urllib3.util import parse_url
from warnings import filterwarnings
filterwarnings("ignore", category=pymysql.Warning)

from utils.log import logger
from config import MONGO, DATABASES


def ping(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        args[0].ecnu_mysql.ping(reconnect=True)

        return func(*args, **kwargs)

    return wrapper


class MysqlOpea(object):
    def __init__(self, database={}):
        if database:
            self.config = database
        else:
            self.config = DATABASES

        self.init_sql()
        super().__init__()

    def init_sql(self):
        self.config['port'] = int(self.config['port'])
        self.config['autocommit'] = True
        self.database = self.config.pop('database')

        try:
            self.ecnu_mysql = pymysql.connect(**self.config)
        except pymysql.err.OperationalError:
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
    def repeat(self, table, condition):
        if self.ecnu_cursor.execute(
                f'SELECT ID FROM `{self.database}`.`{table}` WHERE {condition} LIMIT 1;'
        ) > 0:
            return self.ecnu_cursor.fetchall()[0][0]

    @ping
    def select(self, sql):
        if self.ecnu_cursor.execute(sql) != 0:
            return self.ecnu_cursor.fetchall()

    @ping
    def update(self, _id):
        sql = f'UPDATE `dd1`.`wy` SET `sync` = 1 WHERE `ID` = {_id};'
        self.ecnu_cursor.execute(sql)
        return True

    @ping
    def change_grounding(self, _id):
        sql = f'UPDATE `{self.database}`.`oscshop_lionfish_comshop_goods` SET `grounding` = 0 WHERE `id` = {_id};'
        self.ecnu_cursor.execute(sql)

    @ping
    def insert_good(self, param: dict):
        table = 'oscshop_lionfish_comshop_goods'
        codes = param.get('codes')
        param = self.escape_param(param)
        param.update({'database': self.database})
        param.update({'table': table})

        if self.ecnu_cursor.execute(
                f'SELECT ID FROM `{self.database}`.`{table}` WHERE `codes` = "{codes}" LIMIT 1;'
        ) > 0:
            _id = self.ecnu_cursor.fetchall()[0][0]
            sql = 'UPDATE `{database}`.`{table}` SET `goodsname` = "{goodsname}", `subtitle` = "{subtitle}", `grounding` = {grounding}, `price` = "{price}", `costprice` = "{costprice}", `productprice` = "{productprice}", `sales` = "{sales}", `codes` = "{codes}", `total` = "{total}", `is_all_sale` = "{is_all_sale}", `index_sort` = {index_sort} WHERE `id` = {_id};'
            param.update({'_id': _id})
            self.ecnu_cursor.execute(sql.format(**param))
            return _id
        else:
            sql = 'INSERT INTO `{database}`.`{table}` ( `goodsname`, `subtitle`, `grounding`, `price`, `costprice`, `productprice`, `sales`, `codes`, `total`, `is_all_sale`, `index_sort` ) VALUES ( "{goodsname}", "{subtitle}", {grounding}, "{price}", "{costprice}", "{productprice}", "{sales}", "{codes}", "{total}", "{is_all_sale}", {index_sort} );'
            # sql = 'INSERT INTO `{database}`.`oscshop_lionfish_comshop_goods` ( `goodsname`, `subtitle`, `grounding`, `price`, `costprice`, `productprice`, `sales`, `codes`, `total`, `is_seckill`, `showsales`, `dispatchtype`, `dispatchid`, `dispatchprice`, `weight`, `hasoption`, `credit`, `buyagain`, `buyagain_condition`, `buyagain_sale`, `addtime` ) VALUES ( "{goodsname}", "{subtitle}", {grounding}, "{price}", "{costprice}", "{productprice}", "{sales}", "{codes}", "{total}", "{is_seckill}", 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 );'
            self.ecnu_cursor.execute(sql.format(**param))

            return self.ecnu_cursor.lastrowid

    @ping
    def insert_category(self, name, pid=None, sort=0):
        table = 'oscshop_lionfish_comshop_goods_category'
        if self.ecnu_cursor.execute(
                f'SELECT ID FROM `{self.database}`.`{table}` WHERE `name` = "{name}" LIMIT 1;'
        ) > 0:
            return self.ecnu_cursor.fetchall()[0][0]

        if pid:
            sql = f'INSERT INTO `{self.database}`.`{table}`(`pid`, `name`, `sort_order`, `is_show`, `is_type_show`) VALUES ( {pid}, "{name}", {sort}, 0, 1);'
        else:
            sql = f'INSERT INTO `{self.database}`.`{table}`(`name`, `sort_order`, `is_show`, `is_type_show`) VALUES ( "{name}", {sort}, 1, 1);'

        self.ecnu_cursor.execute(sql)

        return self.ecnu_cursor.lastrowid

    @ping
    def configure_category(self, cate_id, goods_id):
        table = 'oscshop_lionfish_comshop_goods_to_category'
        if self.ecnu_cursor.execute(
                f'SELECT ID FROM `{self.database}`.`{table}` WHERE `goods_id` = "{goods_id}" LIMIT 1;'
        ) > 0:
            sql = f'UPDATE `{self.database}`.`{table}` SET `cate_id` = {cate_id} WHERE `goods_id` = {goods_id};'
        else:
            sql = f'INSERT INTO `{self.database}`.`{table}` (`cate_id`, `goods_id`) VALUES ({cate_id}, {goods_id});'

        self.ecnu_cursor.execute(sql)

        return True

    @ping
    def insert_common(self, param: dict):
        param = self.escape_param(param)
        param.update({'database': self.database})
        goods_id = param.get('goods_id')
        table = 'oscshop_lionfish_comshop_good_common'
        param.update({'table': table})

        if self.ecnu_cursor.execute(
                f'SELECT ID FROM `{self.database}`.`{table}` WHERE `goods_id` = "{goods_id}" LIMIT 1;'
        ) > 0:
            sql = 'UPDATE `{database}`.`{table}` SET `big_img` = "{big_img}", `goods_start_count` = "{goods_start_count}", `video` = "{video}", `oneday_limit_count` = "{oneday_limit_count}", `content` = "{content}", `diy_arrive_details` = "{diy_arrive_details}" , `pick_up_type` = "{pick_up_type}", `is_spike_buy` = "{is_spike_buy}" WHERE `goods_id` = {goods_id};'
        else:
            sql = 'INSERT INTO `{database}`.`{table}` (`goods_id`, `big_img`, `goods_start_count`, `video`, `oneday_limit_count`, `content`, `diy_arrive_details`, `pick_up_type`, `is_spike_buy` ) VALUES ( {goods_id}, "{big_img}", "{goods_start_count}", "{video}", "{oneday_limit_count}", "{content}", "{diy_arrive_details}", "{pick_up_type}", "{is_spike_buy}" );'

        self.ecnu_cursor.execute(sql.format(**param))
        return True

    @ping
    def insert_image(self, goods_id, images):
        sql = 'INSERT INTO `{}`.`oscshop_lionfish_comshop_goods_images`(`goods_id`, `image`) VALUES ({}, "{}");'
        if len(images) > 1:
            images = images[:-1]

        for image in images:
            uri = parse_url(image)
            image = f'{uri.scheme}://{uri.host}/{uri.path}'

            if self.ecnu_cursor.execute(
                    f'SELECT ID FROM `{self.database}`.`oscshop_lionfish_comshop_goods_images` WHERE `goods_id` = "{goods_id}" AND `image` = "{image}" LIMIT 1;'
            ) == 0:
                self.ecnu_cursor.execute(
                    sql.format(self.database, goods_id, image))


class SqliteOpea(object):
    def __init__(self, db):
        self.connect = sqlite3.connect('goods.db', isolation_level=None)
        self.cursor = self.connect.cursor()
        super().__init__()

    def select(self):
        sql = 'SELECT codes FROM goods'
        self.cursor.execute(sql)

        result = self.cursor.fetchall()
        result = [x[0] for x in result]
        return result

    def select_good(self, codes):
        sql = f'SELECT goods, category FROM goods WHERE codes = {codes}'
        self.cursor.execute(sql)
        result = self.cursor.fetchone()
        if result:
            return result[0], result[1]

    def update(self, codes):
        sql = f'UPDATE goods SET grounding = 0 WHERE codes = {codes}'
        self.cursor.execute(sql)

    def insert(self, data):
        sql = 'INSERT INTO goods VALUES (%s)' % data
        self.cursor.execute(sql)


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

        self.mongo = client[config.get('database')]

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

import os
import pymysql
import threading
from functools import wraps

from config import DATABASES


def ping(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        args[0].ecnu_mysql.ping(reconnect=True)

        return func(*args, **kwargs)

    return wrapper


class MysqlOpea(threading.local):
    def __init__(self, dict_=False):
        self.dict_ = dict_
        self.init_sql()
        super().__init__()

    def init_sql(self):
        config = DATABASES

        try:
            self.ecnu_mysql = pymysql.connect(**config)
        except pymysql.err.OperationalError:
            print('登录失败！TimeoutError!')
            os._exit(0)
        else:
            if self.dict_:
                self.ecnu_cursor = self.ecnu_mysql.cursor(
                    cursor=pymysql.cursors.DictCursor)
            else:
                self.ecnu_cursor = self.ecnu_mysql.cursor()

    def escape_param(self, param):
        for key in param:
            value = param[key]
            if isinstance(value, str):
                param[key] = pymysql.escape_string(value)

        return param

    @ping
    def insert(self, param: dict):
        param = self.escape_param(param)
        cols = ', '.join('`{}`'.format(k) for k in param.keys())
        val_cols = ', '.join('%({})s'.format(k) for k in param.keys())

        sql = 'INSERT INTO `ichengyun`.`ichengyun` ( %s ) VALUES ( %s );'
        res_sql = sql % (cols, val_cols)

        self.ecnu_cursor.execute(res_sql, param)

        return True

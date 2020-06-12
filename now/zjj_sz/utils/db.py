import os
import pymysql
from functools import wraps

from utils.log import logger
from utils.run import run_func

from config import DEBUG, DATABASE


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
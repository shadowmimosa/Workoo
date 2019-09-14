import os
import time
import pymysql
import pandas as pd

DEBUG = False


class DealCicpa(object):
    def __init__(self):

        self.select_sql = "SELECT * FROM `workoo`.`whalebj`;"
        self.init_sql()

    def init_sql(self):
        from config import DATABASES
        try:
            if DEBUG:
                config = DATABASES["debug"]
            else:
                config = DATABASES["product"]

            ecnu_mysql = pymysql.connect(**config)

        except pymysql.err.OperationalError as exc:
            print('登录失败！TimeoutError!')
            os._exit(0)
        else:
            self.ecnu_mysql = ecnu_mysql
            self.ecnu_cursor = ecnu_mysql.cursor()

    def check_time(self, content):
        clock = content.split(" ")[-1].split(":")[0]
        if clock >= 14 and clock <= 20:
            return True

    def run(self):
        self.ecnu_cursor.execute(self.select_sql)

        info_ = pd.read_sql(self.select_sql, self.ecnu_mysql)
        info_.to_excel("./data.xlsx", index=False)


if __name__ == "__main__":
    DealCicpa().run()
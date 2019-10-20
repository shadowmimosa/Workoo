import os
import pandas
import pymysql
import datetime
from config import DEBUG, logger


class DataClean(object):
    def __init__(self):
        self.init_sql()
        self.info = pandas.DataFrame(columns=["Id", "股吧", "日期", "发帖量"])

    def init_sql(self):
        from config import DATABASES
        try:
            if DEBUG:
                config = DATABASES["debug"]
            else:
                config = DATABASES["product"]

            ecnu_mysql = pymysql.connect(**config)

        except pymysql.err.OperationalError as exc:
            logger.error("--->Error: 登录失败！TimeoutError!")
            os._exit(0)
        else:
            self.ecnu_cursor = ecnu_mysql.cursor()

    def get_date(self):
        date_temp = datetime.datetime.strptime(
            self.date, "%Y-%m-%d") + datetime.timedelta(days=-1)

        if date_temp.month <= 7 and date_temp.year <= 2018:
            return False
        else:
            self.last_date = self.date
            self.date = date_temp.strftime("%Y-%m-%d")

            return True

    def get_guba(self):
        select_sql = "SELECT `id`, `name` FROM `workoo`.`eastmoney_list`;"
        self.ecnu_cursor.execute(select_sql)
        gubas = self.ecnu_cursor.fetchall()

        for guba in gubas:
            yield guba

    def get_count(self):
        while True:
            if self.get_date() is True:
                select_sql = "SELECT COUNT( `Id` ) FROM `workoo`.`eastmoney_comment_{}` WHERE `GubaId` = '{}' AND `PostTime` < '{} 15:00:00' AND `PostTime` > '{} 15:00:00';"

                self.ecnu_cursor.execute(
                    select_sql.format(self.guba % 5, self.guba, self.last_date,
                                      self.date))
                count = self.ecnu_cursor.fetchone()[0]
                self.info = self.info.append({
                    "Id": "{:0>6}".format(self.guba),
                    "股吧": self.guba_name,
                    "日期": self.last_date,
                    "发帖量": count
                },
                                             ignore_index=True)
            else:
                break

    def main(self):
        yield_guba = self.get_guba()

        while True:
            self.date = "2019-08-01"

            try:
                guba_temp = next(yield_guba)
                self.guba = guba_temp[0]
                self.guba_name = guba_temp[1]
            except StopIteration:
                break
            else:
                self.get_count()
                logger.info("Info: the {} is done".format(self.guba))

        self.info.to_excel("./data_count.xlsx", index=False)


if __name__ == "__main__":
    DataClean().main()
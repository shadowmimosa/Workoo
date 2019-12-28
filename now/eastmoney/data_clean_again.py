import os
import re
import json
import bson
import pymysql
import pymongo
import datetime
from urllib import parse
from pymongo import MongoClient
from config import DEBUG, logger, MONGO


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
        with open('./again.json', 'r', encoding='utf-8') as fn:
            gubas = json.loads(fn.read())

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

                insert_sql = "INSERT INTO `workoo`.`eastmoney_count`(`GubaId`, `name`, `date`, `count`) VALUES ('{}', '{}', '{}', {});"
                sql = insert_sql.format(self.guba, self.guba_name,
                                        self.last_date, count)
                self.ecnu_cursor.execute(
                    insert_sql.format("{:0>6}".format(self.guba),
                                      self.guba_name, self.last_date, count))

                # self.info = self.info.append({
                #     "Id": "{:0>6}".format(self.guba),
                #     "股吧": self.guba_name,
                #     "日期": self.last_date,
                #     "发帖量": count
                # },
                #                              ignore_index=True)
            else:
                break

    def main(self):
        yield_guba = self.get_guba()

        while True:
            self.date = "2019-08-01"

            try:
                self.guba = next(yield_guba)
            except StopIteration:
                break
            else:
                self.get_count()
                logger.info("Info: the {} is done".format(self.guba))

        logger.info("success")


def clean_date():
    # pattern = re.compile(r'/\s+$/')
    # regex = bson.regex.Regex.from_native(pattern)
    # regex.flags ^= re.UNICODE

    while True:
        result = list(mongo['comment'].find({'post_time': {
            '$type': 2
        }},
                                            limit=1))

        if len(result) > 0:
            data = result[0]
            data['post_time'] = datetime.datetime.strptime(
                data['post_time'].strip(' '), "%Y-%m-%d %H:%M:%S")
            mongo['comment'].update_one({'_id': data['_id']}, {'$set': data})
            print('down')
        else:
            break


mongo = init_mongo()

if __name__ == "__main__":
    # DataClean().main()
    clean_date()

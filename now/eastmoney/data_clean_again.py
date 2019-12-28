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
        # date_temp = datetime.datetime.strptime(
        #     self.date, "%Y-%m-%d") + datetime.timedelta(days=-1)
        date_temp = self.date + datetime.timedelta(days=-1)
        if date_temp.month <= 7 and date_temp.year <= 2018:
            return False
        else:
            self.last_date = self.date
            # self.date = date_temp.strftime("%Y-%m-%d")
            self.date = date_temp

            return True

    def get_guba(self):
        with open('./data/again.json', 'r', encoding='utf-8') as fn:
            gubas = json.loads(fn.read())

        for guba in gubas:
            yield guba

    def get_count(self):
        while True:
            if self.get_date() is True:
                mongo['comment'].find({
                    '$and': [{
                        "post_time": {
                            '$lte':
                            datetime.datetime.strptime("2019-12-28 23:31:29")
                        }
                    }, {
                        "post_time": {
                            '$gte':
                            datetime.datetime.strptime("2019-11-06 23:31:38")
                        }
                    }]
                })
                a = self.ecnu_cursor.fetchone()
                count = self.ecnu_cursor.fetchone()[0]

                insert_sql = "INSERT INTO `workoo`.`eastmoney_count`(`GubaId`, `name`, `date`, `count`) VALUES ('{}', '{}', '{}', {});"
                sql = insert_sql.format(self.guba, self.guba_name,
                                        self.last_date, count)
                self.ecnu_cursor.execute(
                    insert_sql.format("{:0>6}".format(self.guba),
                                      self.guba_name, self.last_date, count))

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
    pattern = re.compile(r'\s+$')
    regex = bson.regex.Regex.from_native(pattern)
    regex.flags ^= re.UNICODE

    # 'post_time': regex 正则
    # 'post_time': { '$type': 2 } Sting 类型
    result = list(mongo['comment'].find({'post_time': regex}))

    for data in result:
        data['post_time'] = datetime.datetime.strptime(
            data['post_time'].strip(' '), "%Y-%m-%d %H:%M:%S")
        mongo['comment'].update_one({'_id': data['_id']}, {'$set': data})
        print('down')


mongo = init_mongo()

if __name__ == "__main__":
    # DataClean().main()
    clean_date()
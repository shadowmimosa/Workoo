import os
import time
import json
import random
import pymysql
import traceback

from urllib import parse
from datetime import datetime
from pymongo import MongoClient
from types import MethodType, FunctionType

from config import DEBUG, logger
from utils.request import Query
from utils.soup import DealSoup


class DealEastmoney(object):
    def __init__(self):

        self.page_path = "http://guba.eastmoney.com/list,{},f_{}.html"

        self.header = {
            "Host":
            "guba.eastmoney.com",
            "Upgrade-Insecure-Requests":
            "1",
            "User-Agent":
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36",
            "Accept":
            "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3",
            "Referer":
            "http://guba.eastmoney.com/list,600000.html",
            "Accept-Encoding":
            "gzip, deflate",
            "Accept-Language":
            "zh-CN,zh;q=0.9",
            "Cookie":
            "st_asi=delete; st_si=44083802765114; qgqp_b_id=31b26f667b2c3030c63e6f35ff9c6868; st_pvi=64525288303559; st_sp=2019-09-18%2014%3A45%3A59; st_inirUrl=http%3A%2F%2Fguba.eastmoney.com%2Flist%2C600519.html; st_sn=59; st_psi=20190923232546423-117001301474-2888167628"
        }

        self.request = Query()
        self.soup = DealSoup().judge
        self.select_id_sql = "select `id` from `workoo`.`eastmoney_list` where `status` = 0 Limit 1;"
        self.update_guba_status_sql = "UPDATE `workoo`.`eastmoney_list` SET `status` = {} WHERE `id` = {};"
        self.insert_comment_sql = "INSERT INTO `workoo`.`eastmoney_comment_{guba_id}`(`GubaId`, `ReadCount`, `CommentCount`, `Title`, `Author`, `PostTime`) VALUES ('{GubaId}', '{read_count}', '{comment_count}', '{title}', '{author}', '{post_time}');"
        self.judge_time_sql = "SELECT `Id` FROM `workoo`.`eastmoney_comment_{guba_id}` WHERE `PostTime` = '{post_time}' AND `Author` = '{author}' AND `Title` = '{title}' LIMIT 1;"
        # self.init_sql()
        self.init_mongo()

    def init_mongo(self):
        from config import MONGO

        if DEBUG:
            config = MONGO["debug"]
        else:
            config = MONGO["product"]

        config["user"] = parse.quote_plus(config["user"])
        config["passwd"] = parse.quote_plus(config["passwd"])

        client = MongoClient(
            "mongodb://{user}:{passwd}@{host}:{port}/".format(**config))

        self.mongo = client["eastmoney"]["comment"]

    def deal_resp(self, path, header, data=None):
        # magic_time(0, 1)
        while True:
            resp = self.request.run(path, header=header, data=data)
            if isinstance(resp, str):
                return resp
            elif isinstance(resp, int):
                if resp == 502:
                    time.sleep(5)
                    logger.warning("--->Warning: http 500 now, try it")
                    continue
                elif resp == 400:
                    time.sleep(5)
                    logger.warning("--->Warning: http 400 now, try it")
                    continue

    def deal_soup(self, *args, **kwargs):
        return self.run_func(self.soup, *args, **kwargs)

    def deal_sql(self, sql):
        return self.run_func(self.ecnu_cursor.execute, sql)

    def deal_mongo(self, data):
        return self.run_func(self.mongo.insert_many, data)

    def get_id(self):
        with open("./data/lack.json", "r", encoding="utf-8") as fn:
            data = json.loads(fn.read())

        for guba_id in data:
            yield guba_id

    def deal_text(self, content: str):
        if isinstance(content, str):
            return content.replace("\\", "\\\\").replace("'", "\\'").replace(
                '"', '\\"')
        else:
            logger.error(
                "--->Error: the text is wrong, the type is {}, the text is {}".
                format(type(content, content)))

    def deal_count(self, content: str):
        if isinstance(content, str):
            if "万" in content:
                content = content.replace("万", "")
                count = int(float(content) * 10000)
            elif "亿" in content:
                content = content.replace("亿", "")
                count = int(float(content) * 100000000)
            else:
                count = int(content)
            return count
        else:
            logger.error(
                "--->Error: the text is wrong, the type is {}, the text is {}".
                format(type(content, content)))

    def judge_time(self):
        return datetime.strptime(
            self.date, '%Y-%m-%d %H:%M:%S') < datetime.strptime(
                '2018-08-01 00:00:00', '%Y-%m-%d %H:%M:%S')

    def deal_post(self, post: str):
        return post.replace("发表于 ", "").replace(" 东方财富Android版", "").replace(
            " 东方财富iPhone版", "").replace(" 股吧网页版",
                                        "").replace(" 股吧手机网页版", "").replace(
                                            " 东方财富电脑版", "")

    def insert_comment(self, comment):

        if self.run_func(self.deal_mongo, comment) is not None:
            # logger.info("--->Info: insert successful")
            pass
        else:
            logger.error("--->Error: insert failed")

    def clean_comment(self, comment):
        comment["read_count"] = self.run_func(self.deal_count,
                                              comment.get("read_count"))
        comment["comment_count"] = self.run_func(self.deal_count,
                                                 comment.get("comment_count"))

        comment["title"] = self.run_func(self.deal_text, comment.get("title"))
        comment["author"] = self.run_func(self.deal_text,
                                          comment.get("author"))

        comment["post_time"] = self.run_func(self.deal_post,
                                             comment.get("post_time"))
        return comment

    def get_comment(self, item):
        temp = self.deal_soup(self.deal_soup(item, {"class": "l3 a3"}), "a")

        read_count = self.deal_soup(item, {"class": "l1 a1"}).text
        comment_count = self.deal_soup(item, {"class": "l2 a2"}).text
        title = temp["title"]
        author = self.deal_soup(item, {"class": "l4 a4"}).text
        post_time = self.get_post_time(temp["href"])

        comment = {
            "read_count": read_count,
            "comment_count": comment_count,
            "title": title,
            "author": author,
            "post_time": post_time,
            "GubaId": self.guba_id
        }

        return self.clean_comment(comment)

    def get_post_time(self, href):
        path = "http://guba.eastmoney.com{}".format(href)
        resp = self.deal_resp(path, self.header)
        div = self.deal_soup(resp, attr={"class": "zwfbtime"})

        return div.text

    def deal_detail(self, path):
        resp = self.deal_resp(path, self.header)
        # resp = self.deal_resp(
        #     "http://guba.eastmoney.com/list,002933,f_225.html", self.header)

        comment_divs = self.deal_soup(
            resp, attr={"class": "articleh"}, all_tag=True)

        if len(comment_divs) == 0:
            self.date = "1970-01-01 00:00:00"
            return

        comment_list = []

        for comment_div in comment_divs:
            comment_em = self.deal_soup(comment_div, "em")
            if comment_em is not None:
                if comment_em.text in ["讨论", "悬赏", "公告", "资讯", "置顶", "话题"]:
                    continue
                elif "icon_list_hot" in comment_em.attrs["class"]:
                    continue
                elif "qa" in comment_em.attrs["class"]:
                    continue

            comment_list.append(self.run_func(self.get_comment, comment_div))

        self.insert_comment(comment_list)
        self.date = comment_list[-1]["post_time"]

    def deal_page(self):
        page = 1
        while True:
            path = self.page_path.format(self.guba_id, page)
            self.run_func(self.deal_detail, path)

            if self.judge_time():
                page += 1
            else:
                return

    def run_func(self, func, *args, **kwargs):
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

        else:
            logger.error(
                "--->Error: The type {} is wrong, the func is {}".format(
                    type(func), func))

    def main(self):
        guba = self.get_id()
        while True:
            try:
                self.guba_id = next(guba)
            except StopIteration:
                logger.info("--->Info: all guba is done")
                break
            else:
                self.date = "2019-11-01 00:00:00"
                self.run_func(self.deal_page)

            magic_time(5, 60)


def magic_time(lower: float = 0, upper: float = 5):
    magic = round(random.uniform(lower, upper), 2)
    logger.info("--->Info: Magic Time {} Now".format(magic))
    time.sleep(magic)


if __name__ == "__main__":
    DealEastmoney().main()

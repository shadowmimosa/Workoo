import os
import time
import random
import pymysql
import traceback

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
            "st_asi=delete; st_si=44083802765114; qgqp_b_id=f05dd488c42a506604d4b94ca4098e56; st_pvi=64525288303559; st_sp=2019-09-18%2014%3A45%3A59; st_inirUrl=http%3A%2F%2Fguba.eastmoney.com%2Flist%2C600519.html; st_sn=59; st_psi=20190923232546423-117001301474-2888167628"
        }

        self.request = Query()
        self.soup = DealSoup().judge
        self.select_id_sql = "select `id` from `workoo`.`eastmoney_list` where `status` = 0 Limit 1;"
        self.insert_comment_sql = "INSERT INTO `workoo`.`eastmoney_comment_{guba_id}`(`GubaId`, `ReadCount`, `CommentCount`, `Title`, `Author`, `PostTime`) VALUES ('{GubaId}', '{read_count}', '{comment_count}', '{title}', '{author}', '{post_time}');"
        self.judge_time_sql = "SELECT `Id` FROM `workoo`.`eastmoney_comment_{guba_id}` WHERE `PostTime` = '{post_time}' AND `Author` = '{author}' AND `Title` = '{title}' LIMIT 1;"
        self.update_guba_id_sql = "UPDATE `workoo`.`eastmoney_list` SET `status` = 1 WHERE `id` = {};"
        self.init_sql()

        self.year = 2019
        self.last_month = 9

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

    def judge_already(self):
        a = self.judge_time_sql.format(**self.comment)
        if self.run_func(self.deal_sql,
                         self.judge_time_sql.format(**self.comment)) == 0:
            return True
        else:
            return

    def deal_resp(self, path, header, data=None):
        magic_time(0, 3)
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

    def get_id(self):
        # c = "{0:06d}".format(a[0])
        if self.run_func(self.deal_sql, self.select_id_sql) != 0:
            self.guba_id = "{:0>6}".format(self.ecnu_cursor.fetchone()[0])
            return True
        else:
            logger.info("--->Info: all guba is done")
            return False

    def deal_text(self, content: str):
        if isinstance(content, str):
            return content.replace("'", "\\'")
        else:
            logger.error(
                "--->Error: the text is wrong, the type is {}, the text is {}".
                format(type(content, content)))

    def deal_count(self, content: str):
        if isinstance(content, str):
            if "万" in content:
                content = content.replace("万", "")
                count = int(float(content) * 10000)
            else:
                count = int(content)
            return count
        else:
            logger.error(
                "--->Error: the text is wrong, the type is {}, the text is {}".
                format(type(content, content)))

    def judge_year(self, month: int):
        if isinstance(month, int):
            if self.last_month == 1 and month == 12:
                self.year -= 1

            self.last_month = month
        elif isinstance(month, str):
            try:
                self.run_func(self.judge_year, int(month))
            except ValueError:
                logger.error(
                    "--->Error: the month type is wrong, the month is {}".
                    format(month))

    def deal_time(self, post: str):
        post = post.replace(":", " ").replace("-", " ")
        time_list = post.split(" ")

        if len(time_list) == 4:
            time_obj = {
                "month": time_list[0],
                "day": time_list[1],
                "hour": time_list[2],
                "minute": time_list[3]
            }

            self.run_func(self.judge_year, time_obj["month"])

            time_obj["year"] = self.year
            time_obj["second"] = "00"

            return "{year}-{month}-{day} {hour}:{minute}:{second}".format(
                **time_obj)
        else:
            logger.error("--->Error: the time is wrong")

    def insert_comment(self):
        self.clean_comment()

        if self.run_func(self.judge_already):
            if self.run_func(self.deal_sql,
                             self.insert_comment_sql.format(
                                 **self.comment)) is not None:
                logger.info("--->Info: insert successful")

        else:
            logger.info("--->Info: existed already")

    def clean_comment(self, *args):
        self.comment["read_count"] = self.run_func(
            self.deal_count, self.comment.get("read_count"))
        self.comment["comment_count"] = self.run_func(
            self.deal_count, self.comment.get("comment_count"))

        self.comment["title"] = self.run_func(self.deal_text,
                                              self.comment.get("title"))
        self.comment["author"] = self.run_func(self.deal_text,
                                               self.comment.get("author"))

        self.comment["post_time"] = self.run_func(
            self.deal_time, self.comment.get("post_time"))

    def get_comment(self, item):
        read_count = self.deal_soup(item, {"class": "l1 a1"}).text
        comment_count = self.deal_soup(item, {"class": "l2 a2"}).text
        title = self.deal_soup(self.deal_soup(item, {"class": "l3 a3"}),
                               "a")["title"]
        author = self.deal_soup(item, {"class": "l4 a4"}).text
        post_time = self.deal_soup(item, {"class": "l5 a5"}).text

        self.comment = {
            "read_count": read_count,
            "comment_count": comment_count,
            "title": title,
            "author": author,
            "post_time": post_time,
            "guba_id": int(self.guba_id) % 5,
            "GubaId": self.guba_id
        }

        self.run_func(self.insert_comment)

    def deal_detail(self, path):
        resp = self.deal_resp(path, self.header)
        # resp = self.deal_resp(
        #     "http://guba.eastmoney.com/list,000002,f_43.html", self.header)

        comment_divs = self.deal_soup(
            resp, attr={"class": "articleh"}, all_tag=True)

        for comment_div in comment_divs:
            comment_em = self.deal_soup(comment_div, "em")
            if comment_em is not None:
                if comment_em.text in ["讨论", "悬赏", "公告", "资讯", "置顶"]:
                    continue
                elif "icon_list_hot" in comment_em.attrs["class"]:
                    continue
                elif "qa" in comment_em.attrs["class"]:
                    continue

            self.run_func(self.get_comment, comment_div)

    def done_guba(self):
        logger.info("--->Info: guba {} is done".format(self.guba_id))
        self.run_func(self.deal_sql,
                      self.update_guba_id_sql.format(self.guba_id))

    def deal_page(self):
        page = 1
        while True:
            path = self.page_path.format(self.guba_id, page)
            # self.deal_detail(path)
            self.run_func(self.deal_detail, path)

            if self.year <= 2018 and self.last_month <= 7:
                self.run_func(self.done_guba)
                return
            else:
                page += 1

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
        while True:
            if self.run_func(self.get_id):
                self.run_func(self.deal_page)
            else:
                break
            magic_time(5, 60)


def magic_time(lower: float = 0, upper: float = 5):
    magic = round(random.uniform(lower, upper), 2)
    logger.info("--->Info: Magic Time {} Now".format(magic))
    time.sleep(magic)


if __name__ == "__main__":
    DealEastmoney().main()
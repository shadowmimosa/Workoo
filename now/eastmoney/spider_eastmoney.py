import os
import time
import pymysql
import traceback

from config import DEBUG
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
        self.insert_comment_sql = "INSERT INTO `workoo`.`eastmoney_comment`(`GubaId`, `ReadCount`, `CommentCount`, `Title`, `Author`, `PostTime`) VALUES ('{}', '{}', '{}', '{}', '{}', '{}');"
        self.judge_time_sql = "SELECT `Id` FROM `workoo`.`eastmoney_comment` WHERE `PostTime` = '{}' AND `Author` = '{}' AND `Title` = '{}' LIMIT 1;"
        self.init_sql()

        self.year = 2019

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
            self.ecnu_cursor = ecnu_mysql.cursor()

    def judge_already(self, author, post_time, title):
        if self.ecnu_cursor.execute(
                self.judge_time_sql.format(post_time, author, title)) == 0:
            return True
        else:
            return

    def deal_resp(self, path, header, data=None):
        while True:
            resp = self.request.run(path, header=header, data=data)

            if isinstance(resp, str):
                return resp
            elif isinstance(resp, int):
                if resp == 502:
                    time.sleep(5)
                    print("500 now, try it")
                    continue
                elif resp == 400:
                    time.sleep(5)
                    print("400 now, try it")
                    continue

    def get_id(self):
        self.ecnu_cursor.execute(self.select_id_sql)
        # c = "{0:06d}".format(a[0])

        self.guba_id = "{:0>6}".format(self.ecnu_cursor.fetchone()[0])

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

            if int(time_obj["month"]) >= 11:
                self.year -= 1

            time_obj["year"] = self.year
            time_obj["second"] = "00"

            return "{year}{month}{day}{hour}{minute}{second}".format(
                **time_obj)
        else:
            print("--->Error: the time is wrong")

    def deal_detail(self, item):
        try:
            read_count = self.soup(item, {"class": "l1 a1"}).text
            comment_count = self.soup(item, {"class": "l2 a2"}).text
            title = self.soup(self.soup(item, {"class": "l3 a3"}),
                              "a")["title"]
            author = self.soup(item, {"class": "l4 a4"}).text
            post_time = self.deal_time(
                self.soup(item, {
                    "class": "l5 a5"
                }).text)
        except Exception as exc:
            print()

        if self.judge_already(author, post_time, title):
            self.ecnu_cursor.execute(
                self.insert_comment_sql.format(self.guba_id, read_count,
                                               comment_count, title, author,
                                               post_time))
        else:
            print("--->Info: existed already")

    def deal_page(self, parh):
        resp = self.deal_resp(parh, self.header)
        comment_divs = self.soup(
            resp, attr={"class": "articleh"}, all_tag=True)

        for comment_div in comment_divs:
            comment_em = self.soup(comment_div, "em")
            if comment_em is not None:
                if comment_em.text in ["讨论", "悬赏", "公告", "资讯", "置顶"]:
                    continue
                elif "icon_list_hot" in comment_em.attrs["class"]:
                    continue
                elif "qa" in comment_em.attrs["class"]:
                    continue

            self.deal_detail(comment_div)

    def test(self, name):
        if name > "":
            print(name)
        else:
            print(name)

    def run_func(self, func, *args):
        if not DEBUG:
            func(*args)
        else:
            try:
                func(*args)
            except:
                print("--->Error: the {} is wrong, the error is {}".format(
                    func.__name__, traceback.format_exc()))

    def main(self):
        self.get_id()
        page = 15
        while True:
            path = self.page_path.format(self.guba_id, page)
            self.run_func(self.test, page)
            # self.deal_page(path)

            page += 1


if __name__ == "__main__":
    DealEastmoney().main()
import os
import time
import random
import pymysql
import platform
import bs4
from bs4 import BeautifulSoup

from request import Query

system = platform.system()

if system == "Linux":
    DEBUG = False
elif system == "Windows":
    DEBUG = True


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
            self.ecnu_cursor = ecnu_mysql.cursor()

    def judge_already(self, author, post_time):
        return True
        # if sign == 0:
        #     sql = "SELECT `id` FROM `workoo`.`cicpa_offices` WHERE `证书编号` = '{}' LIMIT 1;"
        # else:
        #     sql = "SELECT `id` FROM `workoo`.`cicpa_staffs` WHERE `注册会计师证书编号` = '{}' LIMIT 1;"

        # if self.ecnu_cursor.execute(sql.format(code)) == 0:
        #     return True
        # else:
        #     return

    def remove_character(self, item_list: list):
        for item in item_list:
            if item == "\n":
                item_list.remove("\n")

        return item_list

    def deal_text(self, content):
        return content.replace("\t",
                               "").replace("\r", "").replace("\n", "").replace(
                                   " ", "").replace("\xa0", "").replace(
                                       "（", "(").replace("）", ")")

    def get_text(self):

        if self.key is None:
            return
        elif self.value is None:
            return
        else:
            key = self.key.replace("\t", "").replace("\n", "").replace(
                " ", "").replace("\xa0", "").replace("（", "(").replace(
                    "）", ")")
            value = self.value.replace("\t", "").replace("\n", "").replace(
                " ", "")
            self.key = None
            self.value = None

            if len(key) == 0:
                return
            else:
                try:
                    self.info[key] = value.replace("（请点击）", "").replace(
                        "请点击", "")
                except AttributeError as exc:
                    pass

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

    def deal_detail(self, item):
        read_count = self.soup(item, {"class": "l1 a1"}).text
        comment_count = self.soup(item, {"class": "l2 a2"}).text
        title = self.soup(self.soup(item, {"class": "l3 a3"}), "a")["title"]
        author = self.soup(item, {"class": "l4 a4"}).text
        post_time = self.soup(item, {
            "class": "l5 a5"
        }).text.replace(":", "").replace(" ", "").replace("-", "")
        post_time = "2019{}00".format(post_time)

        if self.judge_already(author, post_time):
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
            
            self.deal_detail(comment_div)

    def main(self):
        self.get_id()
        page = 1
        while True:
            path = self.page_path.format(self.guba_id, page)
            self.deal_page(path)
            page += 1


class DealSoup(object):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    # def __init__(self, content, attr: dict = None, all_tag: bool = False):
    # self.content = content
    # self.attr = attr
    # self.all_tag = all_tag

    # return self.judge()

    def find_tag_by_attr(self):
        if self.all_tag is False:
            return self.soup.find(attrs=self.attr)
        else:
            return self.soup.find_all(attrs=self.attr)

    def find_tag_by_name(self):
        if self.all_tag is False:
            return self.soup.find(self.attr)
        else:
            return self.soup.find_all(self.attr)

    def find_tag(self):
        if isinstance(self.attr, dict):
            return self.find_tag_by_attr()
        elif isinstance(self.attr, str):
            return self.find_tag_by_name()

    def init_soup(self):
        if isinstance(self.content, str):
            self.soup = BeautifulSoup(self.content, "lxml")
        elif isinstance(self.content, bs4.Tag):
            self.soup = self.content
        elif isinstance(self.content, bs4.BeautifulSoup):
            print("略略略")

    def judge(self, content, attr: dict = None, all_tag: bool = False):
        self.content = content
        self.attr = attr
        self.all_tag = all_tag

        self.init_soup()

        if self.attr is None:
            return self.soup
        else:
            return self.find_tag()

    # def judge(self, content, attr: dict = None, all_tag: bool = False):
    #     if isinstance(content, str):
    #         soup = BeautifulSoup(content, "lxml")
    #         if attr is None:
    #             return soup
    #         elif isinstance(attr, dict):
    #             if all_tag is False:
    #                 return soup.find(attrs=attr)
    #             else:
    #                 return soup.find_all(attrs=attr)
    #     elif isinstance(content, bs4.Tag):
    #         if isinstance(attr, dict):
    #             if all_tag is False:
    #                 return soup.find(attrs=attr)
    #             else:
    #                 return soup.find_all(attrs=attr)
    #     elif isinstance(content, bs4.BeautifulSoup):
    #         print("略略略")


if __name__ == "__main__":
    DealEastmoney().main()
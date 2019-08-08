import os
import pymysql
import json
import pandas as pd
import logging
import requests
import urllib3
import time
from logging.handlers import RotatingFileHandler
from pymysql.err import InternalError
import re


class BiliDeal(object):
    def __init__(self, index=""):
        self.index = index
        self.init_log()
        # self.proxies = False
        self.init_pool()
        self.url = "http://api.bilibili.com/x/reply?type=1&oid={}&pn={}&nohot=1&sort=0"
        self.headers = {
            "User-Agent":
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.140 Safari/537.36 Edge/17.17134",
            "Accept-Language": "zh-Hans-CN,zh-Hans;q=0.8,en-IE;q=0.5,en;q=0.3",
            "Accept":
            "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Upgrade-Insecure-Requests": "1",
            "Accept-Encoding": "gzip, deflate",
            "Host": "api.bilibili.com",
        }
        self.init_mysql()
        self.sql_insert_comment = 'INSERT INTO `bili_awv`.`comment_{}`(`avid`, `num`, `content`) VALUES ({}, {}, "{}");'
        self.sql_update_info = "UPDATE `bili_awv`.`av_info` SET `count` = {} WHERE `avid` = {};"
        self.run()
        self.ecnu_cursor.close()

    def init_mysql(self):
        try:
            ecnu_mysql = pymysql.connect(
                host='127.0.0.1',
                port=3306,
                user='root',
                passwd='shadow',
                database="bili_awv",
                use_unicode=True,
                charset="utf8mb4",
                autocommit=True)
        except pymysql.err.OperationalError as exc:
            print('登录失败！TimeoutError!')
            os._exit(0)
        else:
            self.ecnu_cursor = ecnu_mysql.cursor()

    def init_log(self):

        logger = logging.getLogger(__name__)
        logger.propagate = False
        logger.setLevel(level=logging.INFO)
        if not logger.handlers:
            try:

                handler = RotatingFileHandler(
                    "./log/run_info.log",
                    maxBytes=10 * 1024 * 1024,
                    backupCount=100)
                # handler = loggingFileHandler("./log/run_info.log")
            except FileNotFoundError as exc:
                os.makedirs("./log/")
                self.init_log()
                return
            handler.setLevel(logging.WARNING)
            formatter = logging.Formatter(
                '%(asctime)s - %(funcName)s - %(levelname)s - %(message)s')
            handler.setFormatter(formatter)

            console = logging.StreamHandler()
            console.setLevel(logging.WARNING)

            logger.addHandler(handler)
            logger.addHandler(console)

        self.logger = logger

    def init_pool(self):
        proxyHost = "http-dyn.abuyun.com"
        proxyPort = "9020"
        # 代理隧道验证信息
        proxyUser = "H23W005A02J5V10D"
        proxyPass = "CB31E09182BA20C4"

        proxyMeta = "http://%(user)s:%(pass)s@%(host)s:%(port)s" % {
            "host": proxyHost,
            "port": proxyPort,
            "user": proxyUser,
            "pass": proxyPass,
        }

        self.proxies = {
            "http": proxyMeta,
            "https": proxyMeta,
        }

    def get_session(self):
        """创建 session 示例，以应对多线程"""

        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

        # 设置重连次数
        requests.adapters.DEFAULT_RETRIES = 60
        # 设置连接活跃状态为False
        session = requests.session()
        session.keep_alive = False
        session.verify = False

        adapter = requests.adapters.HTTPAdapter(max_retries=30)
        # 将重试规则挂载到http和https请求
        session.mount('http://', adapter)
        session.mount('https://', adapter)

        return session

    def deal_re(self, byte=False, need_header=False, **kwargs):
        """requests of get"""

        url = kwargs.get("url")
        header = kwargs.get("header")
        try:
            data = kwargs.get("data")
        except:
            data = None

        sesscion_a = self.get_session()

        # print("---> 开始请求网址：{}".format(url))
        self.logger.info("---> 开始请求网址：{}".format(url))
        start_time = time.time()
        retry_count = 5
        while retry_count > 0:
            if self.proxies:
                try:
                    try:
                        if not data:
                            resp = sesscion_a.get(
                                url,
                                headers=header,
                                timeout=(2, 6),
                                allow_redirects=False,
                                proxies=self.proxies)
                        else:
                            resp = sesscion_a.post(
                                url,
                                headers=header,
                                data=data,
                                timeout=(2, 6),
                                proxies=self.proxies)
                        if resp.status_code != 200:
                            retry_count -= 1
                        else:
                            retry_count = 0
                    except Exception as exc:
                        self.logger.error(
                            "---> The error is {}, and the website is {}. Now try again just one time."
                            .format(exc, url))
                        retry_count -= 1

                except ValueError as exc:
                    retry_count -= 1
                    try:
                        if not data:
                            resp = sesscion_a.get(
                                url, headers=header, timeout=(2, 6))
                        else:
                            resp = sesscion_a.post(
                                url, headers=header, data=data, timeout=(2, 6))
                    except Exception as exc:
                        self.logger.error(
                            "---> The error is {}, and the website is {}. Now try again just one time."
                            .format(exc, url))
                        self.deal_re(url=url, header=header, data=data)
            else:
                try:
                    if not data:
                        resp = sesscion_a.get(
                            url,
                            headers=header,
                            allow_redirects=False,
                            timeout=(2, 6))
                    else:
                        resp = sesscion_a.post(
                            url, headers=header, data=data, timeout=(2, 6))
                    retry_count = 0
                except Exception as exc:
                    retry_count -= 1
                    self.logger.error(
                        "---> The error is {}, and the website is {}. Now try again just one time."
                        .format(exc, url))
                    self.deal_re(url=url, header=header, data=data)

        end_time = time.time()

        try:
            if resp.status_code == 200:
                magic_time = end_time - start_time
                self.logger.info(
                    "--->Info: Request successful. It takes {:.3} seconds".
                    format(magic_time))
                return resp
            elif resp.status_code == 302:
                return resp.headers
            else:
                self.logger.error("--->Info {} 请求失败！状态码为{}，共耗时{:.3}秒".format(
                    url, resp.status_code, end_time - start_time))
        except UnboundLocalError as exc:
            self.logger.error(
                "--->Error: deal re is error, the error is {}".format(exc))
            return None

    def bulid_table(self):
        sql = """CREATE TABLE `comment_{}` (
            `id` INT ( 100 ) NOT NULL AUTO_INCREMENT,
            `avid` VARCHAR ( 20 ) NOT NULL,
            `num` VARCHAR ( 20 ) NOT NULL,
            `content` VARCHAR ( 2048 ) NOT NULL,
            PRIMARY KEY ( `id` )
            ) ENGINE = INNODB DEFAULT CHARSET = UTF8MB4;"""

        for index in range(0, 128):
            self.ecnu_cursor.execute(sql.format(index))

    def av_into_data(self):
        sql = "INSERT INTO `bili_awv`.`av_info`(`avid`, `count`) VALUES ({}, NULL);"
        with open("./area24results.csv", "r", encoding="utf-8") as fn:
            av_list = fn.read().split("\n")

        for avid in av_list:
            self.ecnu_cursor.execute(sql.format(avid))

    def insert_comment(self, content):
        if content:
            for value in content:
                # comment = value["content"]["message"].encode("utf-8")
                comment = value["content"]["message"].replace("\\", "\\\\")
                # print(comment)
                # self.ecnu_cursor.execute(r"INSERT INTO `bili_awv`.`comment_111`(`avid`, `content`) VALUES (17842287, '\\' );")
                sql = self.sql_insert_comment.format(
                    self.avid % 128, self.avid, self.pagenum, comment)
                # sql = """INSERT INTO `bili_awv`.`comment_111` ( `avid`, `content` )
                #         VALUES
                #         	( 17842287, '\\\\(//∇//)\\\\' );"""
                self.ecnu_cursor.execute(sql)
                self.pagenum += 1
        else:
            pass

    def format_resp(self):
        pass

    def get_comment(self):
        self.pagenum = 1
        resp = self.deal_re(
            url=self.url.format(self.avid, 1), header=self.headers)
        try:
            data = json.loads(resp.text)["data"]
        except KeyError as exc:
            self.logger.warning("--->Warning: the avid is wrong")
            return
        count = data["page"]["count"]
        self.ecnu_cursor.execute(self.sql_update_info.format(count, self.avid))
        self.insert_comment(data["replies"])
        page = int(count / 20) + 2

        for index in range(2, page):
            resp = self.deal_re(
                url=self.url.format(self.avid, index), header=self.headers)
            self.insert_comment(json.loads(resp.text)["data"]["replies"])

    def run(self):
        # self.bulid_table()
        # self.av_into_data()

        sql = 'SELECT * FROM `bili_awv`.`av_info` WHERE  `id` = {} limit 1'

        # for index in range(180393, 210543):
        try:
            self.ecnu_cursor.execute(sql.format(self.index))
            self.avid = self.ecnu_cursor.fetchone()[1]
            self.get_comment()
        except Exception as exc:
            self.logger.error(
                "--->Error: the {} is error, check it. the message is {}".
                format(self.index, exc))
        else:
            print("--->Info: the {} is successful".format(self.index))


def multi_query(processes=10):
    from multiprocessing import Process, Queue, Pool, freeze_support

    pool = Pool(processes)

    for index in range(190031, 210543):
        try:
            pool.apply_async(BiliDeal, (index, ))
        except Exception as exc:
            print(exc)

    pool.close()
    pool.join()


class DataClean():
    def __init__(self):
        self.sql_sel_info = "SELECT * FROM `av_info` WHERE `id` = {};"
        self.sql_sel_comment = "SELECT * FROM `comment_{}` WHERE `avid` = {};"
        self.sql_sel_count = "SELECT * FROM `comment_count` WHERE `content` = '{}' LIMIT 1;"
        self.sql_insert_count = "INSERT INTO `bili_awv`.`comment_count`(`content`, `count`) VALUES ('{}', '{}');"
        self.sql_update_count = "UPDATE `bili_awv`.`comment_count` SET`count` = {} WHERE `id` = {};"
        self.sql_insert_count_multi = "INSERT INTO `bili_awv`.`comment_count_{}`(`content`, `count`) VALUES ('{}', NULL);"
        self.init_log()
        self.init_mysql()
        self.df = pd.DataFrame(columns=["avid", "content"])
        # self.run()
        # self.ecnu_cursor.close()

    def init_log(self):

        logger = logging.getLogger(__name__)
        logger.propagate = False
        logger.setLevel(level=logging.INFO)
        if not logger.handlers:
            try:

                handler = RotatingFileHandler(
                    "./log/run_info.log",
                    maxBytes=10 * 1024 * 1024,
                    backupCount=100)
                # handler = loggingFileHandler("./log/run_info.log")
            except FileNotFoundError as exc:
                os.makedirs("./log/")
                self.init_log()
                return
            handler.setLevel(logging.WARNING)
            formatter = logging.Formatter(
                '%(asctime)s - %(funcName)s - %(levelname)s - %(message)s')
            handler.setFormatter(formatter)

            console = logging.StreamHandler()
            console.setLevel(logging.WARNING)

            logger.addHandler(handler)
            logger.addHandler(console)

        self.logger = logger

    def init_mysql(self):
        try:
            self.ecnu_mysql = pymysql.connect(
                host='127.0.0.1',
                port=3306,
                user='root',
                passwd='shadow',
                database="bili_awv",
                use_unicode=True,
                charset="utf8mb4",
                autocommit=True)
        except pymysql.err.OperationalError as exc:
            print('登录失败！TimeoutError!')
            os._exit(0)
        else:
            self.ecnu_cursor = self.ecnu_mysql.cursor()

    def judge_count(self, data):
        return data[2] != 0 and data[2] != None

    def check_zh(self, content):
        # pattern = re.compile(r"^[\u4e00-\u9fa5]{0,}$")
        return '\u4e00' <= content <= '\u9fa5'

    def to_csv(self, avid):
        # self.ecnu_cursor.execute(self.sql_sel_comment.format(avid % 128,avid))
        # data = self.ecnu_cursor.fetchall()
        # for value in data:
        df = pd.read_sql(
            self.sql_sel_comment.format(avid % 128, avid),
            con=self.ecnu_mysql,
        )
        # index_col="avid")
        df.drop("num", axis=1, inplace=True)
        df.drop("id", axis=1, inplace=True)

        self.df = self.df.append(df, sort=False)
        self.df.reset_index(
            level=None, drop=True, inplace=True, col_level=0, col_fill="")
        # print(self.df)
    def get_double(self):
        pass

    def get_count(self, avid):
        self.ecnu_cursor.execute(self.sql_sel_comment.format(avid % 128, avid))
        data = self.ecnu_cursor.fetchall()
        for value in data:
            sign = ""
            zh = value[3]
            # zh = '当时最喜欢这段了！歌也贼好听！'
            for singe in zh:
                if self.check_zh(singe):
                    sign += singe
                    if len(sign) == 2:
                        self.ecnu_cursor.execute(
                            self.sql_sel_count.format(sign))
                        count = self.ecnu_cursor.fetchone()
                        if count:
                            self.ecnu_cursor.execute(
                                self.sql_update_count.format(
                                    count[2] + 1, count[0]))
                            # self.ecnu_cursor.execute(
                            #     self.sql_insert_count.format(
                            #         sign, count[2] + 1))
                        else:
                            self.ecnu_cursor.execute(
                                self.sql_insert_count.format(sign, 1))
                        sign = sign[-1]

                    # if len(sign) >= 2:
                    #     self.ecnu_cursor.execute(
                    #         self.sql_sel_count.format(sign))
                    #     count = self.ecnu_cursor.fetchone()
                    #     if count:
                    #         self.ecnu_cursor.execute(
                    #             self.sql_insert_count.format(sign, count[2] + 1))
                    #     else:
                    #         self.ecnu_cursor.execute(
                    #             self.sql_insert_count.format(sign, 1))
                    #     sign = sign[-1]
                    # else:
                    #     sign += singe
                else:
                    sign = ""
        self.sql_sel_comment.format(avid % 128, avid)

    def run(self):
        for index in range(181079, 210543):
            try:
                self.ecnu_cursor.execute(self.sql_sel_info.format(index))
                data = self.ecnu_cursor.fetchone()
                if self.judge_count(data):
                    # self.to_csv(data[1])
                    self.get_count(data[1])
            except Exception as exc:
                self.logger.error(
                    "--->Error: the {} is error, check it. the message is {}".
                    format(index, exc))
            else:
                print("--->Info: the {} is successful".format(index))
        self.df.to_csv("./data/raw_{}.csv".format(int(time.time())))

    def multi_run(self, index):
        self.ecnu_cursor.execute(self.sql_sel_info.format(index))
        self.ecnu_cursor.execute(self.sql_sel_info.format(index))
        count = self.ecnu_cursor.fetchone()

        if self.judge_count(count):
            avid = count[1]
        else:
            return

        self.ecnu_cursor.execute(self.sql_sel_comment.format(avid % 128, avid))
        data = self.ecnu_cursor.fetchall()

        for value in data:
            sign = ""
            zh = value[3]
            # zh = '当时最喜欢这段了！歌也贼好听！'
            for singe in zh:
                if self.check_zh(singe):
                    sign += singe
                    if len(sign) == 2:

                        self.ecnu_cursor.execute(
                            self.sql_insert_count_multi.format(
                                index % 5, sign))

                        sign = sign[-1]
                else:
                    sign = ""


def multi_clean(processes=10):
    for index in range(191907, 198107):
        DataClean().multi_run(index)
    # from multiprocessing import Process, Queue, Pool, freeze_support

    # pool = Pool(processes)
    # # p = DataClean()
    # # q = p.multi_run

    # for index in range(190031, 210543):
    #     try:
    #         pool.apply_async(DataClean().multi_run, (index, ))
    #     except Exception as exc:
    #         print(exc)

    # pool.close()
    # pool.join()


def main(arg):

    # BiliDeal()
    if arg == "multi":
        multi_query(4)
    elif arg == "data_clean":
        # DataClean()
        multi_clean(1)


if __name__ == "__main__":
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    # for i in range(0x4e00, 0x9fa5):
    #     print(chr(i))

    # a = "两个硬币给支持(๑&gt;؂&lt;๑）"
    # for value in a:
    #     print(check_zh(value))

    # main("multi")

    main("data_clean")
    _2018_1_1 = 179507 + 17828943
    _2018_6_30 = 210542 + 25903201

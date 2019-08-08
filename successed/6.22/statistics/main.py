import requests
import urllib3
import time
import sys
import random
import os
import json
import logging
from logging.handlers import RotatingFileHandler
from bs4 import BeautifulSoup
import xlwt
import pandas as pd
import pymysql


class Query(object):
    def __init__(self):
        self.init_log()
        self.url = "http://www.stats.gov.cn/tjsj/tjbz/tjyqhdmhcxhfdm/2018/{}.html"
        self.header = {
            "Host": "www.stats.gov.cn",
            "Upgrade-Insecure-Requests": "1",
            "User-Agent":
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36",
            "Referer":
            "http://www.stats.gov.cn/tjsj/tjbz/tjyqhdmhcxhfdm/2018/",
            "Accept-Encoding": "gzip, deflate",
            "Accept-Language": "zh-CN,zh;q=0.9",
            "Cookie": "AD_RS_COOKIE=20082855",
        }

        if sys.platform == "win32":
            # self.proxies = False
            self.init_pool()
        else:
            self.init_pool()

        # self.proxies = False
        # self.run()  # 不友好

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
            console.setLevel(logging.INFO)

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

    def deal_re(self, byte=False, **kwargs):
        """requests of get"""

        url = kwargs.get("url")
        # header = kwargs.get("header")
        header = self.header
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
                                timeout=(1.5, 4.5),
                                proxies=self.proxies)
                        else:
                            resp = sesscion_a.post(
                                url,
                                headers=header,
                                data=data,
                                timeout=(1.5, 4.5),
                                proxies=self.proxies)
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
                                url, headers=header, timeout=(1.5, 4.5))
                        else:
                            resp = sesscion_a.post(
                                url,
                                headers=header,
                                data=data,
                                timeout=(1.5, 4.5))
                    except Exception as exc:
                        self.logger.error(
                            "---> The error is {}, and the website is {}. Now try again just one time."
                            .format(exc, url))
                        self.deal_re(url=url, header=header, data=data)
            else:
                try:
                    if not data:
                        resp = sesscion_a.get(
                            url, headers=header, timeout=(1.5, 4.5))
                    else:
                        resp = sesscion_a.post(
                            url, headers=header, data=data, timeout=(1.5, 4.5))
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
                resp.encoding = "gbk"
                # resp.encoding = resp.apparent_encoding
                magic_time = end_time - start_time
                self.logger.info(
                    "--->Info: Request successful. It takes {:.3} seconds".
                    format(magic_time))
                if byte:
                    return resp.content
                else:
                    return resp.text
            elif resp.status_code == 401:
                self.logger.warning(
                    "--->Warning: Retrying because error code 401")
                resp = self.deal_re(
                    byte=byte, url=url, header=header, data=data)
            elif resp.status_code == 503:
                print(resp.text)
            else:
                self.logger.error("--->Info {} 请求失败！状态码为{}，共耗时{:.3}秒".format(
                    url, resp.status_code, end_time - start_time))
        except UnboundLocalError as exc:
            self.logger.error(
                "--->Error: deal re is error, the error is {}".format(exc))
            return None

    def del_excel(self, data):
        try:
            self.info_ = self.info_.append(data)
        except AttributeError as exc:
            self.info_ = pd.DataFrame()
            self.del_excel(data)

    def search_(self, resp, url):
        soup = BeautifulSoup(resp, "lxml")
        table = soup.findAll("table")[-1]
        trs = table.findAll("tr")
        for tr in trs[1::]:
            data = []
            tds = tr.findAll("td")
            for td in tds:
                as_ = td.findAll("a")
                if len(as_) != 0:
                    for a in as_:
                        data.append(a.text)
                else:
                    data.append(td.text)
            try:
                self.get_html(url.replace(url.split("/")[-1], a["href"]))
            except NameError as exc:
                pass
            self.del_excel(data)

    def get_html(self, url):
        retry_count = 5
        while True:
            resp = self.deal_re(url=url, header=self.header)
            if resp:
                self.search_(resp, url)
                break
            elif retry_count >= 0:
                retry_count -= 0
                continue
            else:
                self.logger.warning(
                    "--->Warning: the {} was wrong, the resp is {}".format(
                        url, resp))

    def run(self, num):
        retry_count = 5

        while True:
            try:
                self.get_html(self.url.format(num))
                try:
                    self.info_.to_csv("./data/info_{}.csv".format(num))
                except FileNotFoundError as exc:
                    os.makedirs("./data/")
                    self.info_.to_csv("./data/info_{}.csv".format(num))
                finally:
                    del self.info_
                break
            except Exception as exc:
                self.info_.to_csv("./data/error_{}_{}.csv".format(
                    num, int(time.time())))
                retry_count -= 1
                if retry_count <= 0:
                    self.logger.error("--->Error: the error is {}".format(exc))
                    break
                else:
                    self.logger.warning(
                        "--->Waring: the error is {}, retry now".format(exc))
                    continue


def get_num():
    parameter = {
        "11": "北京市",
        "12": "天津市",
        "13": "河北省",
        "14": "山西省",
        "15": "内蒙古自治区",
        "21": "辽宁省",
        "22": "吉林省",
        "23": "黑龙江省",
        "31": "上海市",
        "32": "江苏省",
        "33": "浙江省",
        "34": "安徽省",
        "35": "福建省",
        "36": "江西省",
        "37": "山东省",
        "41": "河南省",
        "42": "湖北省",
        "43": "湖南省",
        "44": "广东省",
        "45": "广西壮族自治区",
        "46": "海南省",
        "50": "重庆市",
        "51": "四川省",
        "52": "贵州省",
        "53": "云南省",
        "54": "西藏自治区",
        "61": "陕西省",
        "62": "甘肃省",
        "63": "青海省",
        "64": "宁夏回族自治区",
        "65": "新疆维吾尔自治区",
    }
    for num in parameter:
        yield num


def single():
    yield_num = get_num()
    q = Query()
    while True:
        try:
            q.run(next(yield_num))
        except StopIteration:
            yield_num.close()
            break


def multi_processes(processes=10):
    """多进程，默认最多 10 个进程"""

    from multiprocessing import Process, Queue, Pool, freeze_support

    pool = Pool(processes)

    yield_num = get_num()
    q = Query()
    while True:
        time.sleep(0.25)
        try:
            pool.apply_async(q.run, (next(yield_num), ))
        except StopIteration:
            yield_num.close()
            break

    pool.close()
    pool.join()


class DataClean():
    def __init__(self):
        self.sql = "INSERT INTO `statistics`.`statistics_info`(`A1`, `A2`, `A3`, `A4`) VALUES ('{}', {}, '{}', {});"
        self.init_mysql()

    def init_mysql(self):
        try:
            self.ecnu_mysql = pymysql.connect(
                host='127.0.0.1',
                port=3306,
                user='root',
                passwd='shadow',
                database="statistics",
                use_unicode=True,
                charset="utf8",
                autocommit=True)
        except pymysql.err.OperationalError as exc:
            print('登录失败！TimeoutError!')
            os._exit(0)
        else:
            self.ecnu_cursor = self.ecnu_mysql.cursor()

    def run_sql(self):
        data = self.data
        if data == None or data == []:
            self.ecnu_cursor.close()
            self.ecnu_cursor.close()
        else:
            length = len(data)
            if length == 2:
                sql = self.sql.format(data[0], "NULL", data[-1], "NULL")
            elif length == 3:
                para = "'{}'".format(data[1])
                sql = self.sql.format(data[0], para, data[-1], "NULL")
            else:
                print("Error!!!")
            self.ecnu_cursor.execute(sql)

    def judge(self):
        for error in ["V", "�", "j"]:
            # for value in self.data:
            if error in self.data[-1]:
                return False
        return True

    def reget(self):
        url = "http://www.stats.gov.cn/tjsj/tjbz/tjyqhdmhcxhfdm/2018/{}/{}/{}/{}.html"
        para = self.data[0]
        if len(para) == 12:
            url = url.format(para[0:2], para[2:4], para[4:6], para[0:9])
        else:
            print("--->Error 2: the data is {}".format(self.data))
            return

        retry_count = 5
        while retry_count > 0:
            resp = Query().deal_re(url=url)
            if resp:
                soup = BeautifulSoup(resp, "lxml")
                table = soup.findAll("table")[-1]
                trs = table.findAll("tr")
                for tr in trs[1::]:
                    data = []
                    tds = tr.findAll("td")
                    for td in tds:
                        data.append(td.text)

                    if data[0] == para:
                        self.data = data
                        break

                retry_count = 0
            elif retry_count > 0:
                retry_count -= 1
                continue
            else:
                print("--->Warning: the {} was wrong, the resp is {}".format(
                    url, resp))

    def data_clean(self):
        self.data = []
        for _, _, files in os.walk("./data/"):
            for info in files:
                # if info != "info_11 - 副本.csv":
                #     continue
                info_csv = pd.read_csv("./data/{}".format(info))
                a = len(info_csv)
                for index in range(len(info_csv) - 1, -1, -1):
                    info_ = info_csv.iloc[index]
                    column_0 = info_["Unnamed: 0"]
                    column_1 = info_["0"]
                    # try:
                    #     int(column_1)
                    # except ValueError as exc:
                    #     self.judge(column_0,column_1)
                    self.data.append(column_1)

                    if column_0 == 0:
                        self.data.reverse()
                        try:
                            if self.judge() == False:
                                raise ValueError
                        except ValueError as exc:
                            print("--->Error 1: the data is {}, reget now".
                                  format(self.data))
                            self.reget()
                        finally:
                            self.run_sql()
                            self.data = []

                    # print(info_)

        self.run_sql()


try:
    ecnu_mysql = pymysql.connect(
        host='127.0.0.1',
        port=3306,
        user='root',
        passwd='shadow',
        database="statistics",
        use_unicode=True,
        charset="utf8",
        autocommit=True)
except pymysql.err.OperationalError as exc:
    print('登录失败！TimeoutError!')
    os._exit(0)
else:
    ecnu_cursor = ecnu_mysql.cursor()

# sql = "Select * from `statistics`.`statistics_info` LIMIT {},{};"
sql = "Select * from `statistics`.`statistics_info`;"
ecnu_cursor.execute(sql.format(0, 50000))

global count
count = 1


def query_sql():
    global count
    count += 1
    yield (ecnu_cursor.fetchone(), count)


def judge(content):
    count = content[1]
    content = content[0]
    try:
        content[2].encode("gbk")
        # print(count)
        # print(content[2].encode("gbk"))
    except UnicodeEncodeError as exc:
        if content[0] in ["420684103005", "500153108200", "510681114209"]:
            return
        print("--->Error: the {} is also unencode!!!".format(content))

        with open("./error.txt", "w+", encoding="utf-8") as fn:
            for error in content:
                if error == None:
                    error = "null"
                fn.write(error)
            fn.write("\n")
        data = content
        url = "http://www.stats.gov.cn/tjsj/tjbz/tjyqhdmhcxhfdm/2018/{}/{}/{}/{}.html"

        para = data[0]
        para0 = para[-1:-4:-1][::-1]
        para1 = para[-4:-7:-1][::-1]
        para2 = para[-7:-9:-1][::-1]
        para3 = para[-9:-11:-1][::-1]
        para4 = para[-11:-13:-1][::-1]

        if int(para0) == 0:
            if int(para1) == 0:
                url = "http://www.stats.gov.cn/tjsj/tjbz/tjyqhdmhcxhfdm/2018/{}/{}.html".format(
                    para4, "{}{}".format(para4, para3))
            else:
                url = "http://www.stats.gov.cn/tjsj/tjbz/tjyqhdmhcxhfdm/2018/{}/{}/{}.html".format(
                    para4, para3, "{}{}{}".format(para4, para3,
                                                  para2)).replace(
                                                      "00.html", ".html")
        else:
            url = "http://www.stats.gov.cn/tjsj/tjbz/tjyqhdmhcxhfdm/2018/{}/{}/{}/{}.html".format(
                para4, para3, para2, para.replace(para0, '')).replace(
                    "/00/", "/")

        retry_count = 5
        while retry_count > 0:
            resp = Query().deal_re(url=url)
            if resp:
                soup = BeautifulSoup(resp, "lxml")
                table = soup.findAll("table")[-1]
                trs = table.findAll("tr")
                for tr in trs[1::]:
                    data = []
                    tds = tr.findAll("td")
                    for td in tds:
                        data.append(td.text)

                    if data[0] == para:
                        need_ = data
                        break

                retry_count = 0
            elif retry_count > 0:
                retry_count -= 1
                continue
            else:
                print("--->Warning: the {} was wrong, the resp is {}".format(
                    url, resp))
        if len(need_) == 3:
            update_sql = "UPDATE `statistics`.`statistics_info` SET `A1` = '{}', `A2` = '{}', `A3` = '{}', `A4` = NULL WHERE `A1` = '{}' LIMIT 1;".format(
                need_[0], need_[1], need_[2], content[0])
        elif len(need_) == 2:
            update_sql = "UPDATE `statistics`.`statistics_info` SET `A1` = '{}', `A2` = NULL, `A3` = '{}', `A4` = NULL WHERE `A1` = '{}' LIMIT 1;".format(
                need_[0], need_[1], content[0])
        ecnu_cursor.execute(update_sql)


def multi_query(processes=10):
    from multiprocessing import Process, Queue, Pool, freeze_support

    pool = Pool(processes)

    yield_id = query_sql()

    while True:
        try:
            pool.apply_async(judge, (next(yield_id), ))
        except StopIteration:
            yield_id.close()
            break

    pool.close()
    pool.join()


def main():
    # single()
    # multi_processes(5)
    # DataClean().data_clean()
    # q = Query()
    # resp = q.deal_re(
    #     url=
    #     "http://www.stats.gov.cn/tjsj/tjbz/tjyqhdmhcxhfdm/2018/13/04/26/130426201.html"
    # )
    # # resp = resp.decode("gb2312").encode("utf-8")
    # soup = BeautifulSoup(resp, "lxml")
    # table = soup.findAll("table")[-1]
    # trs = table.findAll("tr")
    # for tr in trs:
    #     # print(tr.text.encode("gb2312").decode("gb2312"))
    #     print(tr.text)
    # print(resp)
    # multi_query()

    # while True:
    #     id_ = next(query_sql())
    #     try:
    #         if id_[0] != None:
    #             try:
    #                 judge(id_)
    #             except StopIteration:
    #                 query_sql.close()
    #                 break
    #         else:
    #             print(id_[-1])
    #             ecnu_cursor.execute(sql.format(id_[-1] - 100, id_[-1] + 50000))
    #             if id_==None:
    #                 break
    #     except:
    #         ecnu_cursor.close()
    #         ecnu_mysql.close()
    #         break
    while True:
        id_ = next(query_sql())
        try:
            if id_[0] != None:
                try:
                    judge(id_)
                except StopIteration:
                    query_sql.close()
                    break
            else:
                print(id_[-1])
                break
        except:
            ecnu_cursor.close()
            ecnu_mysql.close()
            break

    # judge("六")

    # judge("�")
    # judge("j")
    # judge("V")


if __name__ == "__main__":
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    print("�j\ufffd")
    print("j".encode("utf-8").decode("utf-8"))
    main()
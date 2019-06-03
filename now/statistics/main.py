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


class Query(object):
    def __init__(self, bookid):
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
        self.parameter_url = {
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

        if sys.platform == "win32":
            self.proxies = False
            # self.init_pool()
        else:
            self.init_pool()
        self.detail_path = "./data/index/{}.json"
        self.info_path = "./data/books/{}/info.json"
        self.media_path = "./data/books/{}/{}/{}.{}"
        self.bookid = bookid
        self.timestamp = self.format_timestamp()
        self.run()  # 不友好

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
            handler.setLevel(logging.INFO)
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

    def deal_re(self, byte=False, **kwargs):
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
                                timeout=(3.2, 10),
                                proxies=self.proxies)
                        else:
                            resp = sesscion_a.post(
                                url,
                                headers=header,
                                data=data,
                                timeout=(3.2, 10),
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
                                url, headers=header, timeout=(3.2, 30))
                        else:
                            resp = sesscion_a.post(
                                url,
                                headers=header,
                                data=data,
                                timeout=(3.2, 30))
                    except Exception as exc:
                        self.logger.error(
                            "---> The error is {}, and the website is {}. Now try again just one time."
                            .format(exc, url))
                        self.deal_re(url=url, header=header, data=data)
            else:
                try:
                    if not data:
                        resp = sesscion_a.get(
                            url, headers=header, timeout=(3.2, 30))
                    else:
                        resp = sesscion_a.post(
                            url, headers=header, data=data, timeout=(3.2, 30))
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
                resp.encoding = resp.apparent_encoding
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

    def format_timestamp(self):
        return int(time.time())

    def get_timestamp(self):
        if self.format_timestamp() - self.timestamp > 600:
            self.timestamp = self.format_timestamp()
        return self.timestamp

    def del_excel(self, data):
        try:
            self.info_ = self.info_.append(data)
        except AttributeError as exc:
            self.info_ = pd.DataFrame()
            self.del_excel(data)

    def search_(self, resp, url):
        data = []
        soup = BeautifulSoup(resp, "lxml")
        table = soup.findAll("table")[-1]
        trs = table.findAll("tr")
        for tr in trs[1::]:
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
        resp = self.deal_re(url=url, header=self.header)
        if resp:
            self.search_(resp, url)
        else:
            self.logger.warning("--->Warning: the {} was wrong".format(url))

    def run(self):
        try:
            for num in self.parameter_url:
                self.get_html(self.url.format(num))
            self.info_.to_csv("./info.csv")
        except Exception as exc:
            self.logger.error("--->Error: the error is {}".format(exc))
            self.info_.to_csv("./try_{}.csv".format(int(time.time())))


def main():
    Query("1")


if __name__ == "__main__":
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    main()
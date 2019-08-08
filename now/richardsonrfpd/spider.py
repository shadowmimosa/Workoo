import requests
import urllib3
import time
import logging
from logging.handlers import RotatingFileHandler
import os
import json
import urllib
import hashlib
from bs4 import BeautifulSoup
import random
import pandas as pd


class Query(object):
    def __init__(self):
        self.init_log()

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
            handler.setLevel(logging.ERROR)
            formatter = logging.Formatter(
                '%(asctime)s - %(funcName)s - %(levelname)s - %(message)s')
            handler.setFormatter(formatter)

            console = logging.StreamHandler()
            console.setLevel(logging.INFO)

            logger.addHandler(handler)
            logger.addHandler(console)

        self.logger = logger

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
            try:
                if not data:
                    resp = sesscion_a.get(
                        url,
                        headers=header,
                        allow_redirects=False,
                        timeout=(5, 25))
                elif isinstance(data, dict):
                    resp = sesscion_a.post(
                        url,
                        headers=header,
                        data=json.dumps(data),
                        timeout=(5, 25))
                else:
                    resp = sesscion_a.post(
                        url, headers=header, data=data, timeout=(5, 25))
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
                # print(resp.apparent_encoding)
                # resp.encoding = "ISO-8859-1"
                resp.encoding = "utf-8"
                magic_time = end_time - start_time
                self.logger.info(
                    "--->Info: Request successful. It takes {:.3} seconds".
                    format(magic_time))
                return resp
            elif resp.status_code == 302:
                # return resp.headers
                return None
            elif resp.status_code == 500:
                return resp
            else:
                self.logger.error("--->Info {} 请求失败！状态码为{}，共耗时{:.3}秒".format(
                    url, resp.status_code, end_time - start_time))
        except UnboundLocalError as exc:
            self.logger.error(
                "--->Error: deal re is error, the error is {}".format(exc))
            return None

    def run(self, path, header, data=None):
        resp = self.deal_re(url=path, header=header, data=data)
        if resp:
            return resp.text
        else:
            return resp


class ExtractInfo(object):
    def __init__(self):
        pass

    def extract_div(self, obj):
        return obj.findAll("div", attrs={"class": ["col-md-6"]})

    def extract_a(self, obj):
        return obj.find("a")

    def write_info(self, obj):
        href = obj["href"]
        text = obj.text
        raw_ = {
            "url": href,
            "name": text.split(" (")[0],
            "number": text.split(" (")[-1].replace(")", ""),
        }
        with open("./data/info_.json", "a", encoding="utf-8") as fn:
            fn.write(json.dumps(raw_))
            fn.write("\n")

    def judge(self, href):
        resp = Query().run(
            "https://www.richardsonrfpd.com{}".format(href), header={})
        soup = BeautifulSoup(resp, "lxml")

        for value in self.extract_div(soup):
            item = self.extract_a(value)
            href = item["href"]
            if "AllCategories" in href:
                self.judge(href)
            else:
                self.write_info(item)

    def extract_url(self):
        with open("./AllCategories.html", "r", encoding="utf-8") as fn:
            soup = BeautifulSoup(fn.read(), "lxml")

        for value in self.extract_div(soup):
            item = self.extract_a(value)

            href = item["href"]
            if "AllCategories" in href:
                self.judge(href)
            else:
                self.write_info(item)


class DealSpider(object):
    def __init__(self):
        self.query = Query()
        self.baseurl = "https://www.richardsonrfpd.com"
        self.info_ = pd.DataFrame(columns=["型号", "品牌", "库存"])

    def get_url(self):
        with open("./data/info_.json", "r", encoding="utf-8") as fn:
            data_list = fn.readlines()

        for value in data_list:
            yield json.loads(value)

    def get_url_double(self):
        with open("./log/error_log.log", "r", encoding="utf-8") as fn:
            data_list = fn.readlines()

        for value in data_list:
            yield value.replace("\n", "")

    def get_detail(self, url):
        resp = self.query.run(url, {})
        if resp == None:
            with open("./log/error_log.log", "a", encoding="utf-8") as fn:
                fn.write("{}\n".format(url))
            return
        else:
            soup = BeautifulSoup(resp, "lxml")
            table_obj = soup.find(
                "table",
                attrs={
                    "class": [
                        "table", "table-bordered", "table-hover",
                        "table-striped"
                    ]
                })
            tr_list = []
            for child in table_obj.children:
                if child != "\n":
                    tr_list.append(child)

            for index, value in enumerate(tr_list):
                if index < 2:
                    continue
                else:
                    td_list = []
                    for child in value.children:
                        if child != "\n":
                            td_list.append(child)
                    # for index, value in enumerate(td_list):
                    #     if index == 3:
                    #         good["型号"] = value.text
                    #     elif index == 4:
                    #         good["品牌"] = value.text
                    #     elif index == 7:
                    #         good["库存"] = value.text
                    good = {
                        "型号": td_list[3].text,
                        "品牌": td_list[4].text,
                        "库存": td_list[7].text,
                    }

                    self.info_ = self.info_.append(good, ignore_index=True)

    def auto_page(self, param):
        url = param["url"]
        page = int(int(param["number"]) / 25) + 1
        self.get_detail("{}{}".format(self.baseurl, url))
        if page > 1:
            for index in range(2, page + 1):
                url = "{baseurl}/Products/Search?page={page}&searchBox={name}&instockonly=False&setPageSize=25&fromFilter=true&isPageChange=True&fromPasteIn=False&endCategory={name}&X-Requested-With=XMLHttpRequest".format(
                    baseurl=self.baseurl, page=index, name=param["name"])
                self.get_detail(url)
        else:
            pass

    def main_doble(self):
        yield_url = self.get_url_double()
        while True:
            try:
                url = next(yield_url)
            except StopIteration:
                break
            else:
                self.get_detail(url)
        self.info_.to_excel(
            "./data/data_supple_{}.xlsx".format(int(time.time())), index=False)

    def main(self):
        # param = {
        #     "url": "/Products/Search?endCategory=Tap__Switch",
        #     "name": "Tap Switch",
        #     "number": "1"
        # }
        # self.auto_page(param)
        try:
            yield_url = self.get_url()
            while True:
                try:
                    param = next(yield_url)
                except StopIteration:
                    break
                else:
                    try:
                        self.auto_page(param)
                    except Exception as exc1:
                        print("exc1 is {}".format(exc1))
                        with open(
                                "./log/error_log.log", "a",
                                encoding="utf-8") as fn:
                            fn.write("{} {}\n".format(exc1.args[0], exc1[1]))
            self.info_.to_excel(
                "./data/data_{}.xlsx".format(int(time.time())), index=False)

        except Exception as exc:
            print("exc is {}".format(exc))
            self.info_.to_excel(
                "./data/data_error_{}.xlsx".format(int(time.time())),
                index=False)


if __name__ == "__main__":
    import os
    os.chdir(os.path.dirname(os.path.abspath(__file__)))

    # QueryObj = Query()
    # count = 0
    # with open("./data/info_.json", "r", encoding="utf-8") as fn:
    #     for value in fn.readlines():
    #         count += int(json.loads(value)["number"])
    # print(count)
    # get_id(QueryObj)  # 获取列表 id & 商品数量
    # get_detail(QueryObj)  # 遍历 id, 按页获取商品信息
    # data_clean()  # 提取数据
    # ExtractInfo().extract_url()
    # yield_url = get_url()
    # for i in range(10):
    #     print(next(yield_url))
    # DealSpider().main()
    DealSpider().main_doble()
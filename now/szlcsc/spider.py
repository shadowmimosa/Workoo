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
                        timeout=(2, 6))
                elif isinstance(data, dict):
                    resp = sesscion_a.post(
                        url,
                        headers=header,
                        data=json.dumps(data),
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
                # print(resp.apparent_encoding)
                # resp.encoding = "ISO-8859-1"
                resp.encoding = "utf-8"
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

    def run(self, path, header, data=None):
        resp = self.deal_re(url=path, header=header, data=data)
        return resp.text


def get_id(QueryObj):
    url_938 = "https://list.szlcsc.com/catalog/938.html"
    header_938 = {
        "Host":
        "list.szlcsc.com",
        # "Pragma": "no-cache",
        "Cache-Control":
        "no-cache",
        # "Upgrade-Insecure-Requests": "1",
        "User-Agent":
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.90 Safari/537.36",
        "Accept":
        "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3",
        "Referer":
        "https://www.szlcsc.com/catalog.html",
        "Accept-Encoding":
        "gzip, deflate, br",
        "Accept-Language":
        "zh-CN,zh;q=0.9",
        "Cookie":
        "acw_tc=7ae4faa715625790510296745ec353020a5c696b1f7616876db64fed6a; noLoginCustomerFlag=1dd323bc171d152a9750; noLoginCustomerFlag2=3bdaaa62fa63d281d790; Hm_lvt_e2986f4b6753d376004696a1628713d2=1562579059; SID=e14a4ddd-81bb-46af-8d9d-182a574062ed; Qs_lvt_290854=1562579056%2C1562946980; Qs_pv_290854=371936468931525500%2C2559049905854799000%2C798224791190914400%2C1241414071745198300%2C2405728068904306000; Hm_lpvt_e2986f4b6753d376004696a1628713d2=1562947075; JSESSIONID=DC78B41F64EC5B9F074808EA87C71C71.list"
    }
    resp = QueryObj.run(url_938, header_938)
    soup = BeautifulSoup(resp, "lxml")
    soup_obj = soup.findAll(
        "ul", attrs={"class": ["list-side"]})[0].findAll(
            "li", attrs={"class": ["list-side-li"]})
    with open("./list.txt", "a", encoding="utf-8") as fn:
        for obj in soup_obj:
            div_obj = obj.find(
                "div", attrs={
                    "class": ["list-side-li-tit"]
                }).find("a")
            href = div_obj["href"]
            text = div_obj.text.split("(")[-1].replace(")", "")
            fn.write(href)
            fn.write("\t")
            fn.write(text)
            fn.write("\n")


def read_id():
    with open("./list.txt", "r", encoding="utf-8") as fn:
        obj_list = fn.readlines()

    for obj in obj_list:
        url = obj.split("\t")[0]
        id_ = url.split("/")[-1].split(".")[0]
        pagenum = int(int(obj.split("\t")[-1]) / 30) + 1
        yield id_, pagenum


def get_detail(QueryObj):

    url = "https://list.szlcsc.com/products/list"
    header = {
        "Host":
        "list.szlcsc.com",
        "Accept":
        "application/json, text/javascript, */*; q=0.01",
        "Origin":
        "https://list.szlcsc.com",
        "X-Requested-With":
        "XMLHttpRequest",
        "User-Agent":
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.90 Safari/537.36",
        "Content-Type":
        "application/x-www-form-urlencoded; charset=UTF-8",
        "Referer":
        "https://list.szlcsc.com/catalog/{}.html",
        "Accept-Encoding":
        "gzip, deflate, br",
        "Accept-Language":
        "zh-CN,zh;q=0.9",
        "Cookie":
        "acw_tc=7ae4faa715625790510296745ec353020a5c696b1f7616876db64fed6a; noLoginCustomerFlag=1dd323bc171d152a9750; noLoginCustomerFlag2=3bdaaa62fa63d281d790; Hm_lvt_e2986f4b6753d376004696a1628713d2=1562579059; SID=e14a4ddd-81bb-46af-8d9d-182a574062ed; Qs_lvt_290854=1562579056%2C1562946980; Qs_pv_290854=2559049905854799000%2C798224791190914400%2C1241414071745198300%2C2405728068904306000%2C330806524241869440; Hm_lpvt_e2986f4b6753d376004696a1628713d2=1562947153; show_out_sock_product=1; JSESSIONID=1FD515BF7220A2B6DA79A6E704D2CA87.list"
    }

    data = "catalogNodeId={}&pageNumber={}&querySortBySign=0&showOutSockProduct=1&queryProductGradePlateId=&queryProductArrange=&keyword=&queryBeginPrice=&queryEndPrice=&queryProductStandard=&queryParameterValue=&lastParamName=&baseParameterCondition=&parameterCondition="
    yield_id = read_id()

    while True:
        try:
            obj = next(yield_id)
            id_ = obj[0]
            for pagenum in range(1, obj[1] + 1):
                header[
                    "Referer"] = "https://list.szlcsc.com/catalog/{}.html".format(
                        id_)
                resp = QueryObj.run(url, header, data.format(id_, pagenum))
                with open(
                        "./data/{}_{}.txt".format(id_, pagenum),
                        "w",
                        encoding="utf-8") as fn:
                    fn.write(resp)
                time.sleep(random.randint(1, 3))
        except StopIteration:
            yield_id.close()
            break


def data_clean():
    info_ = pd.DataFrame(columns=["品牌", "型号", "库存"])
    for file_ in os.listdir("./data/"):
        with open("./data/{}".format(file_), "r", encoding="utf-8") as fn:
            datas = json.loads(fn.read())["productRecordList"]
            for data in datas:
                good = {
                    "品牌": data["lightBrandName"],
                    "型号": data["productModel"],
                    "库存": data["stockNumber"]
                }
                info_ = info_.append(good, ignore_index=True)
        # info_.sort_values("品牌", inplace=True)
    info_.to_excel("./data.xlsx", index=False)


if __name__ == "__main__":
    import os
    os.chdir(os.path.dirname(os.path.abspath(__file__)))

    QueryObj = Query()
    # get_id(QueryObj)  # 获取列表 id & 商品数量
    # get_detail(QueryObj)  # 遍历 id, 按页获取商品信息
    data_clean()  # 提取数据

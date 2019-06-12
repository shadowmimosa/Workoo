import requests
import urllib3
import time
import logging
from logging.handlers import RotatingFileHandler
import os
import base64
import json
import re
from bs4 import BeautifulSoup


class Query(object):
    def __init__(self, bookid=None):
        self.init_log()
        self.proxies = False
        self.pattern = re.compile(r'"responseJson",.*}\);')
        self.headers = {
            "Host": "checkcoverage.apple.com",
            "Upgrade-Insecure-Requests": "1",
            "User-Agent":
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36",
            "Accept":
            "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "zh-CN,zh;q=0.9"
        }

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
            console.setLevel(logging.WARNING)

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

    def serch(self, content):
        csrf_re = re.compile(r"csrfToken:.*\"")
        return re.search(csrf_re, content).group().split(" ")[-1].replace(
            '"', "")

    def get_3023(self):
        data = self.deal_re(
            url="http://api.3023data.com/ocr/captcha",
            header={"key": "6a09c7c5a7419c00baa32242c9bf17f7"},
            data={
                "type": 1001,
                "image": "data:image/jpeg;base64,{}".format(self.imgdata)
            })
        return json.loads(data.text)["data"]["captcha"]

    def spider_main(self,imei):
        resp0 = self.deal_re(
            url="https://checkcoverage.apple.com", header=self.headers)

        cookies = resp0["Set-Cookie"].split(", ")

        self.headers["Cookie"] = "{}; {}; {}; {}".format(
            cookies[0].split(";")[0], cookies[1].split(";")[0],
            cookies[2].split(";")[0], cookies[3].split(";")[0])

        resp1 = self.deal_re(url=resp0["location"], header=self.headers)

        resp2 = self.deal_re(
            url=
            "https://www.apple.com/ac/globalnav/4/zh_CN/scripts/ac-globalnav.built.js",
            header={
                "Host": "www.apple.com",
                "User-Agent":
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36",
                "Accept": "*/*",
                "Referer": resp0["location"],
                "Accept-Encoding": "gzip, deflate, br",
                "Accept-Language": "zh-CN,zh;q=0.9",
                "Cookie": cookies[3].split(";")[0]  # POD=cn~zh
            })
        header = self.headers
        header["Accept"] = "application/json, text/javascript, */*; q=0.01"
        header["X-Requested-With"] = "XMLHttpRequest"
        header["Referer"] = resp0["location"]
        header["Cookie"] = "{}; {}; {}; {}; geo=CN; {}; POD=cn~zh".format(
            cookies[0].split(";")[0], cookies[1].split(";")[0],
            cookies[2].split(";")[0], cookies[3].split(";")[0],
            resp2.headers["Set-Cookie"].split(",")[-1].split(";")[0])

        resp3 = self.deal_re(
            url="https://checkcoverage.apple.com/gc?t=image&timestamp={}".
            format(int(time.time() * 1000)),
            header=header)

        with open("./img/{}.jpeg".format(int(time.time())), "wb") as fn:
            self.imgdata = json.loads(resp3.text)["binaryValue"]
            fn.write(base64.b64decode(self.imgdata))

        header = self.headers
        header[
            "Cookie"] = "{}; {}; {}; {}; geo=CN; {}; POD=cn~zh; s_cc=true; s_fid=39554724CF7C11CE-12C2686BF342DB88; s_pathLength=support%3D1%2C; s_invisit_n2_cn=4; s_vnum_n2_cn=4%7C1; s_vi=[CS]v1|2E7FD85F052E7480-40002C2D4001C7DE[CE]; s_sq=applesupportglobalprod%2Cappleglobal%3D%2526pid%253Dacs%25253A%25253Atools%25253A%25253Awck%25253A%25253Acheck%25253A%25253Azh_cn%2526pidt%253D1%2526oid%253D%2525E7%2525BB%2525A7%2525E7%2525BB%2525AD%2526oidt%253D3%2526ot%253DSUBMIT".format(
                cookies[0].split(";")[0], cookies[1].split(";")[0],
                cookies[2].split(";")[0], cookies[3].split(";")[0],
                resp2.headers["Set-Cookie"].split(",")[-1].split(";")[0])
        resp4 = Query().deal_re(
            url="https://checkcoverage.apple.com/cn/zh/?sn={}".format(imei),
            header=header,
            data={
                "sno": imei,
                "ans": self.get_3023(),
                "captchaMode": "image",
                "CSRFToken": self.serch(resp1.text)
            })
        if resp4 == None:
            return
        result = json.loads(
            re.search(self.pattern, resp4.text).group().replace(
                "\"responseJson\",", "").replace(");", ""))["results"]
        json_ = {}

        for value in result:
            json_[value["resultId"]] = value["resultLabel"]
        
        print(json_)
        return json_


def get_judge():
    num = input("输入验证码")
    return num


def main(imei="353001091289737"):
    return Query().spider_main(imei)


if __name__ == "__main__":
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    main()

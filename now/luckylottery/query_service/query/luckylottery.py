import requests
import urllib3
import time
import random
import re
import logging
import sys
import json
from urllib import request


class LuckyLottery(object):
    def __init__(self):
        self.url = "http://api.luckylottery.me/history2?p=1"
        self.header = {
            "Host": "api.luckylottery.me",
            "Accept": "application/json, text/plain, */*",
            "Origin": "http://www.luckylottery.me",
            "User-Agent":
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36",
            "Referer": "http://www.luckylottery.me/",
            "Accept-Encoding": "gzip, deflate",
            "Accept-Language": "zh-CN,zh;q=0.9"
        }
        self.init_log()
        if sys.platform == "win32":
            self.proxies = False
            # self.init_pool()
        else:
            self.init_pool()

    def init_log(self):

        logger = logging.getLogger(__name__)
        logger.setLevel(level=logging.INFO)
        # try:

        #     handler = RotatingFileHandler(
        #         "./log/run_info.log", maxBytes=1024 * 1024, backupCount=3)
        #     # handler = loggingFileHandler("./log/run_info.log")
        # except FileNotFoundError as exc:
        #     os.makedirs("./log/")
        #     self.init_log()
        #     return
        # handler.setLevel(logging.INFO)
        # formatter = logging.Formatter(
        #     '%(asctime)s - %(funcName)s - %(levelname)s - %(message)s')
        # handler.setFormatter(formatter)

        console = logging.StreamHandler()
        console.setLevel(logging.INFO)

        # logger.addHandler(handler)
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
        requests.adapters.DEFAULT_RETRIES = 10
        # 设置连接活跃状态为False
        session = requests.session()
        session.keep_alive = False
        session.verify = False

        adapter = requests.adapters.HTTPAdapter(max_retries=3)
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
                                url, headers=header, timeout=(1.2, 4))
                        else:
                            resp = sesscion_a.post(
                                url,
                                headers=header,
                                data=data,
                                timeout=(1.2, 4))
                    except Exception as exc:
                        self.logger.error(
                            "---> The error is {}, and the website is {}. Now try again just one time."
                            .format(exc, url))
                        self.deal_re(url=url, header=header, data=data)
            else:
                try:
                    if not data:
                        resp = sesscion_a.get(
                            url, headers=header, timeout=(1.2, 4))
                    else:
                        resp = sesscion_a.post(
                            url, headers=header, data=data, timeout=(1.2, 4))
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
                gb_encode = [
                    "gb2312", "GB2312", "gb18030", "GB18030", "GBK", "gbk"
                ]
                if resp.apparent_encoding in gb_encode:
                    resp.encoding = "gbk"

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

    def data_clean(self):
        newest = self.data["data"]["info"][0]
        # newest = ''.join(self.data["data"]["info"][0]["open_arr"])
        # newest = [] x for x in self.data["data"]["info"][0]["open_arr"]]
        # print(newest)
        needed = {
            "number": newest["number"],
            "open_time": newest["open_time"],
            "open_no": newest["open_no"]
        }
        return needed

    def run(self):
        resp = self.deal_re(url=self.url, header=self.header)
        self.data = json.loads(resp)
        return self.data_clean()
        print(resp)


def main():
    return (LuckyLottery().run())


if __name__ == "__main__":
    import os
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    print(main())
import requests
import urllib3
import time
import logging
from logging.handlers import RotatingFileHandler
import os
import json
import urllib
import hashlib


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

    def deal_re(self, byte=False, need_header=False, **kwargs):
        """requests of get"""

        url = kwargs.get("url")
        header = kwargs.get("header")
        try:
            data = kwargs.get("data")
        except:
            data = None
        files = kwargs.get("files")

        sesscion_a = self.get_session()

        # print("---> 开始请求网址：{}".format(url))
        self.logger.info("---> 开始请求网址：{}".format(url))
        start_time = time.time()
        retry_count = 5
        while retry_count > 0:
            try:

                if isinstance(data, dict):
                    resp = sesscion_a.post(
                        url,
                        headers=header,
                        data=json.dumps(data),
                        timeout=(10, 60))
                elif isinstance(files, dict):
                    resp = sesscion_a.post(url, files=files, timeout=(10, 60))
                elif data:
                    resp = sesscion_a.post(
                        url, headers=header, data=data, timeout=(10, 60))
                else:
                    resp = sesscion_a.get(
                        url,
                        headers=header,
                        allow_redirects=False,
                        timeout=(10, 60))
                retry_count = 0
            except Exception as exc:
                retry_count -= 1
                self.logger.error(
                    "---> The error is {}, and the website is {}. Now try again just one time."
                    .format(exc, url))
                # self.deal_re(url=url, header=header, data=data)

        end_time = time.time()

        try:
            if resp.status_code == 200:
                gb_encode = [
                    "gb2312", "GB2312", "gb18030", "GB18030", "GBK", "gbk"
                ]
                
                if resp.apparent_encoding in gb_encode:
                    resp.encoding = "gbk"

                magic_time = end_time - start_time
                self.logger.info(
                    "--->Info: Request successful. It takes {:.3} seconds".
                    format(magic_time))
                time.sleep(1.5)
                return resp
            else:
                self.logger.error("--->Info {} 请求失败！状态码为{}，共耗时{:.3}秒".format(
                    url, resp.status_code, end_time - start_time))
        except UnboundLocalError as exc:
            self.logger.error(
                "--->Error: deal re is error, the error is {}".format(exc))
            return None

    def run(self, path, sign=None, header={}, **kwargs):
        resp = self.deal_re(url=path, header=header, **kwargs)
        if sign:
            return resp.content
        else:
            return resp.text

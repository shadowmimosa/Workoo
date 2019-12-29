import os
import json
import time
import datetime
import brotli
import urllib
import hashlib
import urllib3
import requests
from config import logger, CookieList, mongo, get_cookie


class Query(object):
    def __init__(self):
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
                    resp = sesscion_a.post(url,
                                           headers=header,
                                           data=json.dumps(data),
                                           timeout=(2, 6))
                elif isinstance(files, dict):
                    resp = sesscion_a.post(url, files=files, timeout=(2, 6))
                elif data:
                    resp = sesscion_a.post(url,
                                           headers=header,
                                           data=data,
                                           timeout=(2, 6))
                else:
                    resp = sesscion_a.get(url,
                                          headers=header,
                                          allow_redirects=False,
                                          timeout=(2, 6))
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
                return resp
            elif resp.status_code == 302:
                gb_encode = [
                    "gb2312", "GB2312", "gb18030", "GB18030", "GBK", "gbk"
                ]

                if resp.apparent_encoding in gb_encode:
                    resp.encoding = "gbk"

                magic_time = end_time - start_time
                self.logger.info(
                    "--->Info: Request is 302. It takes {:.3} seconds".format(
                        magic_time))
                return resp.headers["Location"]
            elif resp.status_code >= 500:
                return 502
            elif resp.status_code >= 400 and resp.status_code < 500:
                return 400
            else:
                self.logger.error("--->Info {} 请求失败！状态码为{}，共耗时{:.3}秒".format(
                    url, resp.status_code, end_time - start_time))
        except UnboundLocalError as exc:
            self.logger.error(
                "--->Error: deal re is error, the error is {}".format(exc))
            return None

    def run(self, path, sign=None, header={}, **kwargs):
        resp = self.deal_re(url=path, header=header, **kwargs)
        if resp is None:
            return ""
        elif resp == 'https://static-ag.ymcdn.cn/common/429.html':
            while True:
                # index = CookieList.index(header['Cookie'])
                # header['Cookie'] = CookieList[[1, 0].index(index)]
                cookie = get_cookie()
                if cookie:
                    resp = self.deal_re(url=path, header=header, **kwargs)
                    if resp == 'https://static-ag.ymcdn.cn/common/429.html':
                        mongo['cookie'].update_one({'cookie': cookie}, {
                            "$set": {
                                "time":
                                datetime.datetime.utcnow() +
                                datetime.timedelta(minutes=59)
                            }
                        })
                        logger.warning('---> Access restricted, reget cookie.')
                    else:
                        return resp.text
                else:
                    logger.warning('---> No cookie, sleep now.')
                    time.sleep(600)
        elif isinstance(resp, str):
            return resp
        elif isinstance(resp, int):
            return resp
        elif sign:
            return resp.content
        else:
            return resp.text

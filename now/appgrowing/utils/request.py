import os
import json
import time
import brotli
import urllib
import hashlib
import urllib3
import requests
from config import logger


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
        # header = {
        #     # 'Host': 'ds.appgrowing.cn',
        #     # 'Accept': 'application/json, text/plain, */*',
        #     # 'User-Agent':
        #     #     'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.79 Safari/537.36',
        #     # 'Sec-Fetch-Site': 'same-origin',
        #     # 'Sec-Fetch-Mode': 'cors',
        #     # # 'Referer':
        #     # # 'https://ds.appgrowing.cn/leaflet?category=1210101&channel=102&startDate=2019-06-25&endDate=2019-12-21&order=-updatedAt&isExact=false&page=1',
        #     # 'Accept-Encoding': 'gzip, deflate, br',
        #     # 'Accept-Language': 'zh-CN,zh;q=0.9',
        #     'Cookie': '_ga=GA1.2.371741522.1576915056; _gid=GA1.2.1371933288.1577031516; _gat_gtag_UA_4002880_19=1; sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%2216f277635b23f7-0206d8da8dfeb4-6701434-2073600-16f277635b35d4%22%2C%22%24device_id%22%3A%2216f277635b23f7-0206d8da8dfeb4-6701434-2073600-16f277635b35d4%22%2C%22props%22%3A%7B%22%24latest_referrer%22%3A%22https%3A%2F%2Fyoucloud.com%2Flogin%2Fappgrowing%2F%22%2C%22%24latest_referrer_host%22%3A%22youcloud.com%22%2C%22%24latest_traffic_source_type%22%3A%22%E5%BC%95%E8%8D%90%E6%B5%81%E9%87%8F%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC%22%7D%7D; AG_Token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6ImJhZjVlN2U2LTdmOWMtMzY3YS05N2FjLTUxZjI1YzlhYjFhZSIsImlhdCI6MTU3NzA3MjI3NywiZXhwIjoxNTc5NjY0Mjc2LCJhY2MiOjIyNjg0NH0.744BVt_e9H44ayXcQb-S_LTzWly9UjMWbnq-2WdBTWc'
        # }        
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
                        timeout=(2, 6))
                elif isinstance(files, dict):
                    resp = sesscion_a.post(url, files=files, timeout=(2, 6))
                elif data:
                    resp = sesscion_a.post(
                        url, headers=header, data=data, timeout=(2, 6))
                else:
                    resp = sesscion_a.get(
                        url,
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
                # key = 'Content-Encoding'
                # if(key in resp.headers and resp.headers['Content-Encoding'] == 'br'):
                #     data = brotli.decompress(resp.content)
                #     data1 = data.decode('utf-8')
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
        elif isinstance(resp, str):
            return resp
        elif isinstance(resp, int):
            return resp
        elif sign:
            return resp.content
        else:
            if resp != 'https://static-ag.ymcdn.cn/common/429.html':
                return resp.text
            else:
                while True:
                    resp = self.deal_re(url=path, header=header, **kwargs)

                    if resp == 'https://static-ag.ymcdn.cn/common/429.html':
                        logger.warning('---> Access restricted, sleep now.')
                        time.sleep(3600)
                    else:
                        return resp.text
import os
import json
import time
import datetime
import brotli
import urllib
import hashlib
import urllib3
import requests
from bson import ObjectId
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
                                           timeout=(5, 20))
                elif isinstance(files, dict):
                    resp = sesscion_a.post(url, files=files, timeout=(5, 20))
                elif data:
                    resp = sesscion_a.post(url,
                                           headers=header,
                                           data=data,
                                           timeout=(5, 20))
                else:
                    resp = sesscion_a.get(url,
                                          headers=header,
                                          allow_redirects=False,
                                          timeout=(5, 20))
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
                if resp.apparent_encoding in 'utf-8':
                    resp.encoding = "utf-8"

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

    def run(self, path, sign=None, header={}, raw=None, **kwargs):
        resp = self.deal_re(url=path, header=header, **kwargs)
        # magic_time()
        if resp is None:
            return ""
        elif isinstance(resp, str):
            return resp
        elif isinstance(resp, int):
            return resp
        elif sign:
            return resp.content
        elif raw:
            return resp
        else:
            text = resp.text
            if '你已超过今天请求限制' in text:
                mongo['cookie'].update_one({'cookie': header['Cookie']}, {
                    "$set": {
                        "time":
                        datetime.datetime.utcnow() +
                        datetime.timedelta(minutes=59)
                    }
                })
                cookie = get_cookie()
                header['Cookie'] = cookie
                return self.run(path, header=header)
            elif '请重新登录' in text:
                logger.warning('---> Wrong cookie, sleep now.')
                header['Cookie'] = reget_cookie(header)
                return self.run(path, header=header)
            else:
                return resp.text


def reget_cookie(header):
    req = Query().run
    old_cookie = header['Cookie']
    resp = req('https://bkbs.baokuanbushou.com/s.stp?action=dyhome_pc',
               headers=header,
               raw=True)
    new_session = resp.headers['Set-Cookie'].split(';')[0].split('=')[-1]
    header['Cookie'] = f'dysessionid={new_session}; proxyid=unknown'
    resp = req(
        'https://bkbs.baokuanbushou.com/s.stp?action=dy_login&proxyid=13320814955&pass=fallinlove900&stcallback=stcallback',
        header=header)
    new_cookie = f'dysessionid={new_session}; proxyid=13320814955'
    mongo['cookie'].update_one({'cookie': old_cookie},
                               {"$set": {
                                   "cookie": new_cookie
                               }})
    return new_cookie

def magic_time():
    second = mongo['cookie'].find_one(
        {'_id': ObjectId('5e16d4b7c0000000850049b4')})['waiting']
    time.sleep(second)
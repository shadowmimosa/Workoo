import os
import time
import json
import urllib
import urllib3
import requests
import random

import pandas as pd


class Query(object):
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

        print("---> 开始请求网址：{}".format(url))
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

        end_time = time.time()

        try:
            if resp.status_code == 200:
                magic_time = end_time - start_time
                return resp
            else:
                print("--->Info {} 请求失败！状态码为{}，共耗时{:.3}秒".format(
                    url, resp.status_code, end_time - start_time))
        except UnboundLocalError as exc:
            print("--->Error: deal re is error, the error is {}".format(exc))
            return None

    def run(self, path, sign=None, header={}, **kwargs):
        resp = self.deal_re(url=path, header=header, **kwargs)
        if sign:
            return resp.content
        else:
            return resp.text


class DealGhzrzyw(object):
    def __init__(self):
        self.url = "http://ghzrzyw.beijing.gov.cn/sjzy/front/landsold/oprcadastral.do?iid={}"
        self.header = {
            "Host": "ghzrzyw.beijing.gov.cn",
            "Upgrade-Insecure-Requests": "1",
            "User-Agent":
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.90 Safari/537.36",
            "Accept":
            "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3",
            "Accept-Encoding": "gzip, deflate",
            "Accept-Language": "zh-CN,zh;q=0.9"
        }
        self.info = pd.DataFrame()
        self.request = Query()
        self.run()

    def main(self, path):
        resp = self.request.run(path, header=self.header)
        info_ = {}
        for data in pd.read_html(resp)[-1].values:
            key = data[0].replace("：", "")
            value = data[-1]
            if "浏览次数" in key:
                key = "浏览次数"
                value = value.replace("浏览次数：", "")
            elif key == "返回":
                continue
            info_[key] = value
        self.info = self.info.append(info_, ignore_index=True)

    def run(self):
        try:
            for page in range(9000):
                self.main(self.url.format(page + 1))
                time.sleep(random.randint(0, 5))

            self.info.to_excel("./data.xlsx", index=False)
        except Exception as exc:
            print("---> Error: the error is {}, the page is {}".format(exc, ))
            pass


if __name__ == "__main__":
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    DealGhzrzyw()
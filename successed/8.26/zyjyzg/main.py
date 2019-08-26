import os
import time
import json
import urllib
import urllib3
import requests
import random
from requests.exceptions import ReadTimeout

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

        # print("---> 开始请求网址：{}".format(url))
        start_time = time.time()
        retry_count = 1
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
            except ReadTimeout:
                return False
            except Exception as exc:
                print(exc)
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
        if resp:
            if sign:
                if resp.encoding != None:
                    return resp.content
                else:
                    return None
            else:
                return resp.text


class DealPdf(object):
    def __init__(self):
        self.path = "http://zgpt.zyjyzg.org/dms/upl/download/{}.json?isNoDown=true"
        self.request = Query()

        self.filename = None

    def get_name(self):
        header = {
            "Host": "zgpt.zyjyzg.org",
            "Accept": "application/json, text/javascript, */*; q=0.01",
            "Origin": "http://zgpt.zyjyzg.org",
            "X-Requested-With": "XMLHttpRequest",
            "User-Agent":
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.90 Safari/537.36",
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
            "Referer": "http://zgpt.zyjyzg.org/dms/ztjg/index.page",
            "Accept-Encoding": "gzip, deflate",
            "Accept-Language": "zh-CN,zh;q=0.9",
            "Cookie": "JSESSIONID=80E5C7457C1D6C28DE3D1FFF2C848CC5"
        }
        # data = {
        #     "pageNum": "1",
        #     "pageSize": "50",
        #     "filetype": "file",
        #     "parent": str(self.page),
        # }
        data = "pageNum=1&pageSize=50&filetype=file&parent={}".format(
            self.page)
        resp = self.request.run(
            "http://zgpt.zyjyzg.org/dms/file/list.json",
            header=header,
            data=data)
        try:
            info = json.loads(resp)
        except Exception as exc:
            print("---> Error is {}, id is {}".format(exc, self.page))
        for value in info["data"]["list"]:
            if "测试学校" not in value["filepath"]:
                with open("./data/dirty.txt", "a", encoding="utf-8") as fn:
                    fn.write("{}\n".format(value["filepath"]))
            else:
                self.filename = value["filename"]
                self.down_pdf(value["id"])
                

    def down_pdf(self, page):
        if self.filename == None:
            self.filename = page
        header = {
            "Host":
            "zgpt.zyjyzg.org",
            "User-Agent":
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.90 Safari/537.36",
            "Accept":
            "*/*",
            "Referer":
            "http://zgpt.zyjyzg.org/dms/pdf/index.page?fileurl=/dms/upl/download/{}.json?isNoDown=true"
            .format(page),
            "Accept-Encoding":
            "gzip, deflate",
            "Accept-Language":
            "zh-CN,zh;q=0.9",
            "Cookie":
            "JSESSIONID=80E5C7457C1D6C28DE3D1FFF2C848CC5"
        }
        try:
            resp = self.request.run(
                self.path.format(page), header=header, sign=True)
        except Exception as exc:
            print("---> Error is {}, file is {}".format(exc, page))

        if resp and len(resp) > 4096:
            with open("./data/{}".format(self.filename), "wb") as fn:
                fn.write(resp)
        else:
            print("---> Error: the {} is None".format(page))

        # time.sleep(2)

    def run(self):
        # for self.page in range(1200, 5000):
        #     self.get_name()
        self.page = 1361
        self.get_name()

def rename():
    path = "C:/Users/ShadowMimosa/Documents/GitRepository/Workoo/now/zyjyzg/data/"
    for value in os.listdir(path):
        if value[-4:] != ".pdf":
            os.rename(
                os.path.join(path, value),
                os.path.join(path, "{}.pdf".format(value)))


if __name__ == "__main__":
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    DealPdf().run()
    # rename()
    # dirty_list = [
    #     2760, 2762, 2763, 2765, 2766, 2767, 2768, 2769, 2770, 2771, 2772, 2773,
    #     2774, 2775, 2776, 2777, 2778, 2780, 2781, 2782, 2783, 2784, 2785, 2786,
    #     2788, 2789, 2790, 2791, 2793, 2795, 2796, 2798, 2799, 2800, 2801, 2802,
    #     2803, 192, 2870, 2871, 2872, 2874, 2887, 2888, 2889, 2890, 2891, 2892,
    #     2893, 2894, 2895, 2896, 2909, 2910, 2911, 2912, 2913, 2914, 2915, 2916,
    #     2917, 2820, 2827, 2833, 2834, 2835, 2838, 2839, 2841, 2843, 2844, 2845,
    #     2846, 2854, 2856, 2857, 2858, 2859, 2860, 2861, 2862, 174, 2710, 132,
    #     133, 134, 135, 136
    # ]
    # for index in dirty_list:
    #     DealPdf().down_pdf(index)
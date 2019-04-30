import requests
import urllib3
import time
import random
import re
import logging


def get_proxy():
    return requests.get("http://127.0.0.1:5010/get/").content


def delete_proxy(proxy):
    requests.get("http://127.0.0.1:5010/delete/?proxy={}".format(proxy))


class RepairSalt(object):
    def __init__(self):
        self.url = "http://repair.salt.ch/CaseWizard/StepSerialNumberPreregisteredOrange/GetFmiPInfos?imei={}&productId={}"
        self.header = {
            "Host":
            "repair.salt.ch",
            "Accept":
            "application/json, text/javascript, */*; q=0.01",
            "X-Requested-With":
            "XMLHttpRequest",
            # "Connection": "keep-alive",
            "User-Agent":
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36",
            "Referer":
            "http://repair.salt.ch/CaseWizard/Wizard/27427839-ade1-46ad-ab14-e03bcdf4b5b4/Salt/RepairAtHome",
            "Accept-Encoding":
            "gzip, deflate",
            "Accept-Language":
            "zh-CN,zh;q=0.9",
            "Cookie":
            "session.repairline=4pdwfw0xn1lxi4ezmz3wbokv; settings.repairline=pu4IokItfq5LEWk70NhlOQ==; __lfcc=1"
        }

    def get_session(self):
        """创建 session 示例，以应对多线程"""

        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

        #设置重连次数
        requests.adapters.DEFAULT_RETRIES = 5
        # 设置连接活跃状态为False
        session = requests.session()
        session.keep_alive = False
        session.verify = False

        adapter = requests.adapters.HTTPAdapter(max_retries=3)
        #将重试规则挂载到http和https请求
        session.mount('http://', adapter)
        session.mount('https://', adapter)

        return session

    def deal_re(self, byte=False, **kwargs):
        """requests of get"""

        url = kwargs["url"]
        # url = kwargs.get("url")
        header = kwargs.get("header")
        try:
            data = kwargs.get("data")
        except:
            data = None

        sesscion_a = self.get_session()

        print("---> 开始请求网址：{}".format(url))
        start_time = time.time()
        # try:
        #     if not data:
        #         resp = sesscion_a.get(url, headers=header, timeout=(3.2, 30))
        #     else:
        #         resp = sesscion_a.post(
        #             url, headers=header, data=data, timeout=(3.2, 30))
        # except Exception as exc:
        #     print(
        #         "---> The error is {}, and the website is {}. Now try again just one time."
        #         .format(exc, url))
        #     self.deal_re(url=url, header=header, data=data)
        retry_count = 5
        proxy = str(get_proxy(), encoding='utf-8')
        print(proxy)
        while retry_count > 0:
            try:
                if not data:
                    resp = sesscion_a.get(
                        url,
                        headers=header,
                        timeout=(3.2, 10),
                        proxies={"http": "http://{}".format(proxy)})
                else:
                    resp = sesscion_a.post(
                        url,
                        headers=header,
                        data=data,
                        timeout=(3.2, 10),
                        proxies={"http": "http://{}".format(proxy)})
                retry_count = 0
                print(resp)
            except Exception as exc:
                print(
                    "---> The error is {}, and the website is {}. Now try again just one time."
                    .format(exc, url))
                self.deal_re(url=url, header=header, data=data)
                retry_count -= 1

                if retry_count == 0:
                    delete_proxy(proxy)

        end_time = time.time()
        if resp.status_code == 200:
            print("---> {} 请求成功！共耗时{:.3}秒\n".format(url,
                                                    end_time - start_time))
            random_time = random.randint(1, 3)
            print("---> 现在开始睡眠 {} 秒\n".format(random_time))
            time.sleep(random_time)
            if byte:
                return resp.content
            else:
                return resp.text
        else:
            print("---> {} 请求失败！状态码为{}，共耗时{:.3}秒\n".format(
                url, resp.status_code, end_time - start_time))

    def data_clean(self, content):
        pattern = re.compile(
            r"\\u003cbr /\\u003e=\\u003e \w* \\u003c=\\u003cbr /\\u003e\\u003cbr /\\u003e"
        )
        filter_list = []
        judge_list = re.findall(pattern, content)
        for value in judge_list:
            value = value.replace('\\', '').replace('/', '').replace(
                'u003e', '').replace('u003c', '').replace('=', '').replace(
                    'br', '').replace(' ', '')
            filter_list.append(value)

        return filter_list

    def run(self, imei="356719084092134"):
        url = self.url.format("356719084092134", "1849673")

        resp = self.deal_re(bype=True, url=url, header=self.header)
        if resp:
            query_list = self.data_clean(resp)
            string = "{}\t{}\t{}\t{}\n"
            print(query_list)
            # with open("./log/query_log.log", "a+") as fn:
            #     fn.write(
            #         string.format(imei, query_list[0], query_list[-1], resp))

            return query_list[0], query_list[-1]


def main():
    return (RepairSalt().run())


if __name__ == "__main__":
    import os
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    main()

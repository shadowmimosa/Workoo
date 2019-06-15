import requests
import urllib3
import time
import random
import re
import logging
import sys
from urllib import request


class GetProxy(object):
    def __init__(self):
        self.json_url = "http://ged.ip3366.net/api/?key=20190511142815685&getnum=30&filter=1&area=1&formats=2"
        self.text_url = "http://ged.ip3366.net/api/?key=20190511142815685&getnum={}&filter=1"
        self.json_url_backup = "http://dec.ip3366.net/api/?key=20190511142815685&getnum=30&filter=1&area=1&formats=2"
        self.text_url_backup = "http://dec.ip3366.net/api/?key=20190511142815685&getnum=30&filter=1&area=1"
        self.abuyun_url = "http-dyn.abuyun.com"
        self.zhima_url = "http://webapi.http.zhimacangku.com/getip?num=1&type=2&pro=&city=0&yys=0&port=1&pack=55163&ts=0&ys=0&cs=0&lb=1&sb=0&pb=45&mr=1&regions="

    def get_proxy(self):
        resp = requests.get(
            url=self.text_url.format('1'), verify=False).text.replace(
                '\r', '').replace('\n', '')
        return resp

    def deal_re(self):
        resp = requests.get(url=self.text_url, verify=False)

    def abuyun(self, url):

        # 要访问的目标页面
        # targetUrl = "http://test.abuyun.com"
        targetUrl = url

        # 代理服务器
        proxyHost = self.abuyun_url
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

        proxy_handler = request.ProxyHandler({
            "http": proxyMeta,
            "https": proxyMeta,
        })

        auth = request.HTTPBasicAuthHandler()
        opener = request.build_opener(proxy_handler, auth, request.HTTPHandler)

        opener = request.build_opener(proxy_handler)

        request.install_opener(opener)
        resp = request.urlopen(targetUrl).read()

        print(resp)

    def zhima(self):
        #请求地址
        targetUrl = "http://baidu.com"

        #代理服务器
        proxyHost = "ip"
        proxyPort = "port"

        proxyMeta = "http://%(host)s:%(port)s" % {
            "host": proxyHost,
            "port": proxyPort,
        }

        #pip install -U requests[socks]  socks5代理
        # proxyMeta = "socks5://%(host)s:%(port)s" % {

        #     "host" : proxyHost,

        #     "port" : proxyPort,

        # }

        proxies = {
            "http": proxyMeta,
            "https": proxyMeta,
        }

        resp = requests.get(targetUrl, proxies=self.proxies)


def get_proxy():
    # return requests.get("http://127.0.0.1:5010/get/").content
    # return GetProxy().get_proxy()
    # return GetProxy().abuyun()
    pass


def delete_proxy(proxy):
    # requests.get("http://127.0.0.1:5010/delete/?proxy={}".format(proxy))
    pass


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
        self.zhima_url = "http://webapi.http.zhimacangku.com/getip?num=1&type=1&pro=&city=0&yys=0&port=1&pack=55163&ts=0&ys=0&cs=0&lb=1&sb=0&pb=45&mr=1&regions="

        # self.proxies=False
        # self.init_abuyun()
        self.init_zhima()

    def init_abuyun(self):
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

    def init_zhima(self):
        resp = requests.get(self.zhima_url).text

        proxyMeta = "http://%(host)s:%(port)s" % {
            "host": resp.split(":")[0],
            "port": resp.split(":")[-1].replace("\r\n", ""),
        }

        self.proxies = {
            "http": proxyMeta,
            "https": proxyMeta,
        }
        print(self.proxies)

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

        if self.proxies:
            try:
                retry_count = 3
                # proxy = get_proxy()
                # if type(proxy) != str:
                #     proxy = str(get_proxy(), encoding='utf-8')
                # if proxy == "no proxy!":
                #     raise ValueError("no proxy")
                # else:
                #     print("the proxy is {}".format(proxy))
                while retry_count > 0:
                    try:
                        if not data:
                            resp = sesscion_a.get(
                                url,
                                headers=header,
                                timeout=(3.2, 10),
                                proxies=self.proxies)
                            # proxies={"http": "http://{}".format(proxy)})
                        else:
                            resp = sesscion_a.post(
                                url,
                                headers=header,
                                data=data,
                                timeout=(3.2, 10),
                                proxies=self.proxies)
                            # proxies={"http": "http://{}".format(proxy)})
                        retry_count = 0
                        print(resp)
                    except Exception as exc:
                        print(
                            "---> The error is {}, and the website is {}. Now try again just one time."
                            .format(exc, url))
                        # self.deal_re(url=url, header=header, data=data)
                        retry_count -= 1

                        # if retry_count == 0:
                        #     delete_proxy(proxy)
            except ValueError as exc:
                if exc.args[0] == "no proxy":
                    print("no proxy now, run deal re without proxy")

                    try:
                        if not data:
                            resp = sesscion_a.get(
                                url, headers=header, timeout=(3.2, 30))
                        else:
                            resp = sesscion_a.post(
                                url,
                                headers=header,
                                data=data,
                                timeout=(3.2, 30))
                    except Exception as exc:
                        print(
                            "---> The error is {}, and the website is {}. Now try again just one time."
                            .format(exc, url))
                        self.deal_re(url=url, header=header, data=data)
        else:
            try:
                if not data:
                    resp = sesscion_a.get(
                        url, headers=header, timeout=(3.2, 30))
                else:
                    resp = sesscion_a.post(
                        url, headers=header, data=data, timeout=(3.2, 30))
            except Exception as exc:
                print(
                    "---> The error is {}, and the website is {}. Now try again just one time."
                    .format(exc, url))
                self.deal_re(url=url, header=header, data=data)

        end_time = time.time()
        try:
            if resp.status_code == 200:
                magic_time = end_time - start_time
                print("---> {} 请求成功！共耗时{:.3}秒\n".format(url, magic_time))
                if magic_time <= 6:
                    random_time = random.randint(1, 3)
                    # print("---> 现在开始睡眠 {} 秒\n".format(random_time))
                    time.sleep(random_time)
                if byte:
                    return resp.content
                else:
                    return resp.text
            elif resp.status_code == 401:
                print("---> Retrying because 401")
                self.init_request()
                resp = self.deal_re(
                    byte=byte, url=url, header=header, data=data)
            elif resp.status_code == 503:
                print(resp.text)
            else:
                print("---> {} 请求失败！状态码为{}，共耗时{:.3}秒\n".format(
                    url, resp.status_code, end_time - start_time))
        except UnboundLocalError as exc:
            print("deal re is error, the error is {}".format(exc))
            return None

    def data_clean(self, content):
        pattern = re.compile(
            r"\\u003cbr /\\u003e=\\u003e \w* \\u003c=\\u003cbr /\\u003e\\u003cbr /\\u003e"
        )
        filter_list = []
        judge_list = re.findall(pattern, content)
        if len(judge_list) == 0 and "FMiPText" in content:
            return None

        for value in judge_list:
            value = value.replace('\\', '').replace('/', '').replace(
                'u003e', '').replace('u003c', '').replace('=', '').replace(
                    'br', '').replace(' ', '')
            filter_list.append(value)
        print("filter list is {}".format(filter_list))
        return filter_list

    def init_request(self):
        url = "http://repair.salt.ch/CaseWizard/Wizard/27427839-ade1-46ad-ab14-e03bcdf4b5b4/Salt/RepairAtHome/New"
        header = {
            "Host":
            "repair.salt.ch",
            "Upgrade-Insecure-ReUpgradequests":
            "1",
            "User-Agent":
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36",
            "Accept":
            "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
            "Accept-Encoding":
            "gzip, deflate",
            "Accept-Language":
            "zh-CN,zh;q=0.9",
            "Cookie":
            "session.repairline=4pdwfw0xn1lxi4ezmz3wbokv; settings.repairline=pu4IokItfq5LEWk70NhlOQ=="
        }
        resp = self.deal_re(url=url, header=header)

    def check_imei(self, imei="356726086774842"):
        url = "http://repair.salt.ch/CaseWizard/StepSerialNumberPreregisteredOrange/EditStep"
        header = self.header
        # header["Connection"] = "keep-alive"
        header["Accept"] = "text/html, */*; q=0.01"
        header["Origin"] = "http://repair.salt.ch"
        header[
            "Content-Type"] = "application/x-www-form-urlencoded; charset=UTF-8"
        header[
            "Cookie"] = "session.repairline=4pdwfw0xn1lxi4ezmz3wbokv; settings.repairline=pu4IokItfq5LEWk70NhlOQ=="
        data = {
            "SerialNumber": imei,
            "ProductName": "10062301+-+Apple+-+iPhone+6s+128GB+sr",
            "ProductId": "1849694",
            "ManufacturerBusinessunitId": "0"
        }
        try:
            resp = self.deal_re(url=url, header=header, data=data)
            pattern = re.compile(r".*Invalid serial number.*")
            # with open("./check.html", 'w') as fn:
            #     fn.write(resp)
            if resp:
                judge_ = re.search(pattern, resp)
                if judge_:
                    return False
                else:
                    return True
            else:
                return True

        except Exception as exc:
            if exc == "expected string or bytes-like object":
                print("check imei is error, the error is {}".format(Exception))
            else:
                print("check imei is error, the error is {}".format(exc))

    def judge_imei(self, imei):
        json_ = {"status": "error", "msg": "IMEI 错误"}
        if imei.isdigit():
            if len(imei) == 15:
                return True
            else:
                json_["msg"] = "IMEI 长度不符，请输入 15 位数字"
        else:
            json_["msg"] = "IMEI 字符类型不符，请输入 15 位数字"

        print("judge imei is no pass, the reason is {}".format(json_["msg"]))
        return json_

    def run(self, imei):
        imei_status = self.judge_imei(imei)
        if imei_status == True:
            # url = self.url.format(imei, "1849673")
            url = self.url.format(imei, "1849694")
            if self.check_imei(imei):
                resp = self.deal_re(bype=True, url=url, header=self.header)
            else:
                return "Invalid serial number"

            if resp:
                query_list = self.data_clean(resp)
                string = "{}\t{}\t{}\t{}\n"
                print("query list is {}".format(query_list))
                # with open("./log/query_log.log", "a+") as fn:
                #     fn.write(
                #         string.format(imei, query_list[0], query_list[-1], resp))

                if query_list:
                    return query_list[0], query_list[-1]
                else:
                    return "off"

        elif type(imei_status) == dict:
            return imei_status


def main(imei="356726086774842"):
    print("imei is {}".format(imei))
    return (RepairSalt().run(imei))


def test():
    while True:
        re = main()
        if re == None:
            break


if __name__ == "__main__":
    import os
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    # a = main()
    # RepairSalt().init_request()
    # judge_ = RepairSalt().check_imei("014738000094457")
    # print(judge_)
    # GetProxy().get_proxy()
    # GetProxy().abuyun()
    test()

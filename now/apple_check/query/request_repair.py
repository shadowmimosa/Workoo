import requests
import urllib3
import time
import logging
from logging.handlers import RotatingFileHandler
import os
import base64
import json
import re
# from bs4 import BeautifulSoup
import datetime


class Query(object):
    def __init__(self, bookid=None):
        self.init_log()
        self.proxies = False
        self.proxies = self.init_abuyun()
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
        self.tel_pattern = re.compile(r"预计到期日.*日<br")
        # self.tel_extend = re.compile(r"AppleCare+")

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
        print(json.loads(data.text)["data"]["captcha"])
        return json.loads(data.text)["data"]["captcha"]

    def spider_main(self, imei):
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
        self.result = json.loads(
            re.search(self.pattern, resp4.text).group().replace(
                "\"responseJson\",", "").replace(");", ""))
        # print(self.result)

        # for value in result:
        #     json_[value["resultId"]] = value["resultLabel"]
        self.data_clean()

        # print(self.json_)
        return self.json_

    #计算两个日期相差天数，自定义函数名，和两个日期的变量名。
    def caltime(self, date1, date2=time.strftime("%Y-%m-%d")):
        #%Y-%m-%d为日期格式，其中的-可以用其他代替或者不写，但是要统一，同理后面的时分秒也一样；可以只计算日期，不计算时间。
        #date1=time.strptime(date1,"%Y-%m-%d %H:%M:%S")
        #date2=time.strptime(date2,"%Y-%m-%d %H:%M:%S")
        date1 = time.strptime(date1, "%Y-%m-%d")
        date2 = time.strptime(date2, "%Y-%m-%d")
        #根据上面需要计算日期还是日期时间，来确定需要几个数组段。下标0表示年，小标1表示月，依次类推...
        #date1=datetime.datetime(date1[0],date1[1],date1[2],date1[3],date1[4],date1[5])
        #date2=datetime.datetime(date2[0],date2[1],date2[2],date2[3],date2[4],date2[5])
        date1 = datetime.datetime(date1[0], date1[1], date1[2])
        date2 = datetime.datetime(date2[0], date2[1], date2[2])
        #返回两个变量相差的值，就是相差天数
        return date1 - date2

    def tel_support(self):
        print(4)
        if self.result["results"][1]["status"] == "yellow":
            self.json_["电话支持"] = "已过期"
        else:
            result_text = self.result["results"][1]["resultText"]
            tel_support = re.search(self.tel_pattern, result_text)

            if tel_support:
                tel_date = tel_support.group().split("：")[-1].replace(
                    "年", "-").replace("月", "-").replace("日", "").replace(
                        "<br", "")
                self.json_["电话支持"] = "{}（{}）".format(
                    tel_date,
                    self.caltime(tel_date).days)
            elif result_text.find("AppleCare") != -1:
                self.json_["电话支持"] = "延长保修"

    def hardware(self):
        print(3)
        result_hard_text = self.result["results"][2]["resultText"]
        if self.result["results"][2]["status"] == "green":
            if self.result["results"][2]["resultLabel"].find("有次数限制") == -1:
                hard_date = re.search(self.tel_pattern, result_hard_text)
                if hard_date:
                    hard_date_num = hard_date.group().split("：")[-1].replace(
                        "年", "-").replace("月", "-").replace("日", "").replace(
                            "<br", "")
                    self.json_["硬件保修"] = "{}（{}）".format(
                        hard_date_num,
                        self.caltime(hard_date_num).days)
            else:
                self.json_["硬件保修"] = "延长保修"
        else:
            self.json_["硬件保修"] = "已过期"

        if result_hard_text.find("您的产品存在相关的服务历史记录") == -1:
            self.json_["是否官换"] = "否"
        else:
            self.json_["是否官换"] = "是"

    def info_base(self):
        print("1")
        info = self.result["productInfo"]
        print(2)
        if "IMEI" in info["PRODUCT_LABEL"]:
            self.json_["IMEI"] = info["SERIAL_ID"]
            self.json_["SN"] = "********{}".format(
                info["PROD_IMAGE_URL"].split("=")[1].split("&")[0])
        else:
            self.json_["SN"] = info["SERIAL_ID"]

        self.json_["设备名称"] = info["PROD_DESCR"]
        self.json_["颜色内存"] = "稍等"

    def get_day(self, day=datetime.date.today(), year=1):
        # a = type(day)
        # b = type(datetime.timedelta(days=year))
        if isinstance(day, str):
            day = datetime.datetime.strptime(day, "%Y-%m-%d")

        return (day - datetime.timedelta(days=365)).strftime('%Y-%m-%d')

    def activation(self):
        print(6)
        if "-" in self.json_["硬件保修"]:
            day = self.json_["硬件保修"]
            if "iPhone" in self.json_["设备名称"]:
                self.json_["激活时间"] = self.get_day(day, 1)
                print(7)
            elif "iPad" in self.json_["设备名称"]:
                self.json_["激活时间"] = self.get_day(day, 1)
                print(8)
            elif "Mac" in self.json_["设备名称"]:
                self.json_["激活时间"] = self.get_day(day, 2)
                print(9)
        else:
            self.json_.pop("激活时间")
        # else:
        #     self.json_["激活时间"] = "666"
    def data_clean(self):
        self.json_ = {}
        self.info_base()
        print(5)
        if self.result["IS_REGISTERED"] == "Y":
            self.json_["是否激活"] = "已激活"
            # self.json_["激活时间"] = ""

            self.tel_support()
            self.hardware()

            if len(self.result["results"]) == 4:
                self.json_["是否延保"] = "是"
            else:
                self.json_["是否延保"] = "否"

            self.activation()

        elif self.result["IS_REGISTERED"] == "N":
            self.json_["是否激活"] = self.result["results"][0]["resultLabel"]


def get_judge():
    num = input("输入验证码")
    return num


def main(imei="353001091289737"):
    a = Query().get_day("2019-06-09", 1)
    b = type(a)
    print(a)
    return Query().spider_main(imei)


if __name__ == "__main__":
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    main()

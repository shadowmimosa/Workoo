import json
import time
import random
import requests
from bs4 import BeautifulSoup

# from utils.request import Query
# from utils import email_opea
from request import Query
import email_opea


class CheckImei(object):
    def __init__(self):
        self.header = {
            "Host": "api.itechshark.com",
            "Accept": "application/json, text/plain, */*",
            "Origin": "https://itechshark.com",
            "User-Agent":
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.90 Safari/537.36",
            "Content-Type": "application/json;charset=UTF-8",
            "Referer": "https://itechshark.com/activation-lock",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "zh-CN,zh;q=0.9",
        }
        self.check_path = "https://api.itechshark.com/api/check-imei"
        self.request = Query()

    def get_email(self):
        with open("./emails.json", "r", encoding="utf-8") as fn:
            data = json.loads(fn.read())
        # self.email = data[random.randint(0, len(data) - 1)]
        self.email = data[0]

    def judge_type(self, content):
        if "Please refer to the article below on how to remove the linked account" in content:
            iemi_status = "Find My iPhone: on (开启)"
        elif "This device is ready to be sold or purchased" in content:
            iemi_status = "Find My iPhone: off (关闭)"
        elif "Duplicate Order. Retry in 2 minutes" in content:
            iemi_status = "重复的订单。2分钟后重试!"
        elif "IMEI is Wrong!" in content:
            iemi_status = "IMEI是错误的!"
        elif "ERROR" in content:
            iemi_status = "序列号错误"

        return iemi_status

    def deal_html(self):
        time.sleep(2)
        emailObj = email_opea.ReadEmail(
            self.email.get("email"),
            self.email.get("password"),
            pop_host=self.email.get("pop_host"))
        email_content = emailObj.run()

        for html in email_content:
            soup = BeautifulSoup(html, 'lxml')
            strObj = soup.find(attrs={"class": "mb-3"})
            if strObj == None:
                strObj = soup.find(attrs={"class": "my-3"})
                if strObj == None:
                    strObj = soup.find(attrs={"class": "my-3"})
            return_text = strObj.text

            return self.judge_type(return_text)

    def run(self, imei):
        self.get_email()
        body = {"imei": imei, "email": self.email.get("email")}
        # header = {
        #     "Host": "api.itechshark.com",
        #     "Access-Control-Request-Method": "POST",
        #     "Origin": "https://itechshark.com",
        #     "User-Agent":
        #     "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.90 Safari/537.36",
        #     "Access-Control-Request-Headers": "content-type",
        #     "Accept": "*/*",
        #     "Referer": "https://itechshark.com/activation-lock",
        #     "Accept-Encoding": "gzip, deflate, br",
        #     "Accept-Language": "zh-CN,zh;q=0.9"
        # }
        # resp = requests.options(
        #     url="https://api.itechshark.com/api/check-imei", headers=header)

        resp = self.request.run(self.check_path, header=self.header, data=body)

        if eval(resp) == "success":
            return {"status": "success", "msg": self.deal_html()}
        else:
            pass


if __name__ == "__main__":
    import os
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    print(CheckImei().run("359237067458583"))
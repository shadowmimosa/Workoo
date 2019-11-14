import json
import time
import redis
import random
import requests
from bs4 import BeautifulSoup

# from request import Query
# import email_opea  as email_opea
from itechshark.utils.request import Query
from itechshark.utils import email_opea


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
        self.email_string = None

    # def get_email(self):
    #     with open(
    #             "./itechshark/data/emails.json", "r", encoding="utf-8") as fn:
    #         data = json.loads(fn.read())
    #     self.email = data[0]

    def get_email(self):
        # while True:
        # emails.watch("emails")
        # try:
        #     email_list = emails.get("emails")
        if self.email_string is None:
            while True:
                self.email_string = emails.lpop("emails")
                if self.email_string is not None:
                    self.email_string = self.email_string.decode("utf-8")
                    self.email = {
                        "email": self.email_string.split(" ")[0],
                        "password": self.email_string.split(" ")[1],
                        "pop_host": self.email_string.split(" ")[2]
                    }
                    self.emailObj = email_opea.ReadEmail(
                        self.email.get("email"),
                        self.email.get("password"),
                        pop_host=self.email.get("pop_host"))
                    # print(self.email)
                    # print(self.email_string)
                    return
                else:
                    print("--->Info: the emails is None. Retrying...")
        else:
            print("--->Info: insert email Now.")
            emails.rpush("emails", self.email_string)

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
        # time.sleep(2)
        # a = time.time()
        # print("333")

        email_content = self.emailObj.run()
        # print(time.time() - a)
        for html in email_content:
            soup = BeautifulSoup(html, 'lxml')
            strObj = soup.find(attrs={"class": "mb-3"})
            if strObj == None:
                strObj = soup.find(attrs={"class": "my-3"})
                if strObj == None:
                    strObj = soup.find(attrs={"class": "my-3"})
            return_text = strObj.text
        # print(time.time() - a)

        return self.judge_type(return_text)

    def run(self, imei):
        self.get_email()
        self.emailObj.dele_mails()
        # self.get_email()
        # return {"code": "success", "msg": {"IMEI": imei, "status": "status"}}

        body = {"imei": imei, "email": self.email.get("email")}
        header = {
            "Host": "api.itechshark.com",
            "Access-Control-Request-Method": "POST",
            "Origin": "https://itechshark.com",
            "User-Agent":
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.90 Safari/537.36",
            "Access-Control-Request-Headers": "content-type",
            "Accept": "*/*",
            "Referer": "https://itechshark.com/activation-lock",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "zh-CN,zh;q=0.9"
        }
        resp = requests.options(
            url="https://api.itechshark.com/api/check-imei", headers=header)
        resp = self.request.run(self.check_path, header=self.header, data=body)

        if eval(resp) == "success":
            status = self.deal_html()
            self.get_email()
            return {"code": "success", "msg": {"IMEI": imei, "status": status}}
        else:
            print("222")
            self.get_email()


pool = redis.ConnectionPool(host='127.0.0.1', port='6379')
# pool = redis.ConnectionPool(host='127.0.0.1', port='6379', db=0, password="")
emails = redis.Redis(connection_pool=pool)

# print("1234")
if __name__ == "__main__":
    import os
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    print(CheckImei().run("359237067458583"))
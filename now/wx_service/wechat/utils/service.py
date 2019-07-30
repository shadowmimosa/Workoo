from .request import Query
import os
import time
import json
import hashlib
import random
import string
from decimal import Decimal
from django.shortcuts import render
from bs4 import BeautifulSoup

from wechat.models import UserInfo, TransactionInfo
# from now.wx_service.wechat.managers import UserInfo, TransactionInfo
from wechat.utils.common import get_event


class DealService(object):
    def __init__(self, **kwargs):
        self.openid = kwargs.get("openid")
        self.current = kwargs.get("current")
        self.imei = kwargs.get("imei")
        self.event_key = kwargs.get("event_key")
        self.click_list = get_event()
        self.appkey = "6a09c7c5a7419c00baa32242c9bf17f7"
        self.requests = Query()

    def guarantee(self):
        resp = self.requests.run(
            "http://39.105.2.213:80/query/?imei={}".format(self.imei),
            header={})

        return True, json.loads(resp)

    def id_activate(self):
        resp = self.requests.run(
            "http://132.232.235.229:39005/query/?imei={}".format(self.imei),
            header={})

        return True, json.loads(resp)

    def id_black_white(self):
        resp = self.requests.run(
            "http://132.232.235.229:39005/query/?imei={}".format(self.imei),
            header={})

        return True, json.loads(resp)

    def id_with_imei(self):
        resp = self.requests.run(
            "http://132.232.235.229:39005/query/?imei={}".format(self.imei),
            header={})

        return True, json.loads(resp)

    def mac_machine(self):
        resp = self.requests.run(
            "http://api.3023data.com/apple/details?source=carrier&lang=zh&sn={}"
            .format(self.imei),
            header={"key": self.appkey})
        data = json.loads(resp)

        if data["code"] == 0:
            return True, data["data"]
        else:
            return False, "请联系客服"

    def network_lock(self):

        resp = self.requests.run(
            "http://applecheck.info/api_processor.php?api_key=QUI53155ACETT&service_id=102&imei={}"
            .format(self.imei),
            header={})

        if "SUCCESS" in resp or "ERROR" in resp:
            data = resp.split("Result:")[-1]
            return True, data
        else:
            return False, "请联系客服"

    def service_provide(self):
        resp = self.requests.run(
            "http://applecheck.info/api_processor.php?api_key=QUI53155ACETT&service_id=101&imei={}"
            .format(self.imei),
            header={})
        if "SUCCESS" in resp or "ERROR" in resp:
            data = resp.split("Result:")[-1]
            return True, data
        else:
            return False, "请联系客服"

    def official_change(self):
        resp = self.requests.run(
            "http://api.3023data.com/apple/appraisal?sn={}".format(self.imei),
            header={"key": self.appkey})
        data = json.loads(resp)

        if data["code"] == 0:
            return True, data["data"]
        else:
            return False, "请联系客服"

    def mac_repair(self):
        resp = self.requests.run(
            "http://api.3023data.com/apple/repair?sn={}".format(self.imei),
            header={"key": self.appkey})
        data = json.loads(resp)

        if data["code"] == 0:
            return True, data["data"]
        else:
            return False, "请联系客服"

    def over_protection(self):
        resp = self.requests.run(
            "https://api.ifreeicloud.co.uk/?key=TGR-GEB-PQ2-474-BXO-986-6V7-PSK&imei={}&service=140"
            .format(self.imei),
            header={})
        data = json.loads(resp)

        if data["success"] == True and data["status"] == "Successful":
            return True, data["response"]
        elif data["success"] == False:
            return False, data["error"]
        else:
            return False, "请联系客服"

    def imei_each(self):
        resp = self.requests.run(
            "https://imeicheck.info/user/api/getdata?IMEI={}&ACCESS_KEY=qpo9wb1a5g&SERVICE_ID=3"
            .format(self.imei),
            header={})

        return True, resp

    def extended_information(self):
        return False, "请稍后"

    def recharge(self):
        print("RECHARGE")

    def move_services(self):
        return False, "请稍后"

    def bulid_order_id(self):
        raw_str = "{}{}{}".format(self.openid, time.time(),
                                  random.randint(0, 100))
        md5 = hashlib.md5()
        md5.update(raw_str.encode("utf-8"))
        return md5.hexdigest().upper()

    def insert_order(self,
                     out_trade_no=None,
                     fee=None,
                     order_type=-1,
                     status=1):
        if fee == None:
            fee = self.fee
        if out_trade_no == None:
            out_trade_no = self.bulid_order_id()
        TransactionInfo.objects.insert_transaction(
            out_trade_no=out_trade_no,
            openid=self.openid,
            amount=fee,
            type=order_type,
            status=status)

    def deduction_fee(self, fee=None):
        if fee == None:
            fee = self.fee

        UserInfo.objects.update_balance(self.openid, "{:.2f}".format(
            Decimal(0 - fee)))

    def main(self):
        # a = "self." + self.current
        # print(a)
        # globals()[a]()
        # locals()[a]()
        if self.event_key == None:
            self.fee = float(self.click_list[self.current]["count"])
            self.balance = float(UserInfo.objects.query_balance(self.openid))
            if self.balance < self.fee:
                return "余额不足，请充值"
            else:
                status, info_ = eval("self.{}".format(self.current.lower()))()
                if status:
                    if isinstance(info_, str):
                        final = info_.replace("<br>", "\n").replace(
                            "<font color=FF0000>",
                            "").replace("</font>}",
                                        "").replace("[", "").replace("]", "")
                    elif isinstance(info_, dict):
                        final = ""
                        for key, value in info_.items():
                            final += "{}: {}\n".format(key, value)

                    self.insert_order()
                    self.deduction_fee()
                else:
                    final = info_
                    self.insert_order(status=0)

                return final

        else:
            return eval("self.{}".format(self.event_key.lower()))()


class WxPay(object):
    def __init__(self, openid="omFm91TlajGX2aYF9mDptN623vPM", fee=1):
        self.key = "AifengchaxunWeiXinzhifumishi6691"
        self.openid = openid
        self.fee = fee
        self.requests = Query()
        self.DS = DealService(openid=openid)

    def trans_dict_to_xml(self, data_dict):  # 定义字典转XML的函数
        data_xml = []
        for k in sorted(data_dict.keys()):  # 遍历字典排序后的key
            v = data_dict.get(k)  # 取出字典中key对应的value
            if k == 'detail' and not v.startswith('<![CDATA['):  # 添加XML标记
                v = '<![CDATA[{}]]>'.format(v)
            data_xml.append('<{key}>{value}</{key}>'.format(key=k, value=v))
        return '<xml>{}</xml>'.format(''.join(data_xml)).encode(
            'utf-8')  # 返回XML，并转成utf-8，解决中文的问题

    def trans_xml_to_dict(self, data_xml):
        soup = BeautifulSoup(data_xml, features='xml')
        xml = soup.find('xml')  # 解析XML
        if not xml:
            return {}
        data_dict = dict([(item.name, item.text) for item in xml.find_all()])
        return data_dict

    def get_sign(self, data_dict, key=None):
        # 签名函数，参数为签名的数据和密钥
        if key == None:
            key = self.key
        params_list = sorted(
            data_dict.items(), key=lambda e: e[0], reverse=False)  # 参数字典倒排序为列表
        params_str = "&".join(u"{}={}".format(k, v)
                              for k, v in params_list) + '&key=' + key
        # 组织参数字符串并在末尾添加商户交易密钥
        md5 = hashlib.md5()  # 使用MD5加密模式
        md5.update(params_str.encode('utf-8'))  # 将参数字符串传入
        sign = md5.hexdigest().upper()  # 完成加密并转为大写
        return sign

    def random_str(self, length=32):
        return ''.join(
            random.choices(string.ascii_letters + string.digits, k=length))

    def update_order(self, out_trade_no, openid, fee, status=1):
        TransactionInfo.objects.update_status(out_trade_no, status)
        UserInfo.objects.update_balance(openid, fee / 100)

    def unified_order(self):
        out_trade_no = self.DS.bulid_order_id()
        data = {
            "appid": "wxb3c3f15d73d9c9b8",
            "mch_id": "1542583141",
            "nonce_str": self.random_str(),
            "body": "爱锋查询充值",
            "out_trade_no": out_trade_no,
            "total_fee": int(self.fee) * 100,
            "spbill_create_ip": "39.105.2.213",
            "notify_url": "39.105.2.213/wx/pay/result/",
            "trade_type": "JSAPI",
            "openid": self.openid
        }
        data["sign"] = self.get_sign(data)
        data = self.trans_dict_to_xml(data).decode('utf-8')
        resp = self.requests.run(
            "https://api.mch.weixin.qq.com/pay/unifiedorder",
            header={'Content-Type': 'text/xml'},
            data=data.encode("utf-8"))
        result = self.trans_xml_to_dict(resp)
        if result["return_code"] == "SUCCESS":
            package = "prepay_id={}".format(result["prepay_id"])
            params = {
                "appId": "wxb3c3f15d73d9c9b8",
                "timeStamp": int(time.time()),
                "nonceStr": self.random_str(),
                "package": package,
                "signType": "MD5"
            }
            params["paySign"] = self.get_sign(params)
            params["resultCode"] = "SUCCESS"

            self.DS.insert_order(
                out_trade_no=out_trade_no,
                fee=self.fee,
                order_type=1,
                status=0)
        else:
            params = {"resultCode": "FAIL"}
        return params


def oauth_wx(code):
    token_url = "https://api.weixin.qq.com/sns/oauth2/access_token?appid=wxb3c3f15d73d9c9b8&secret=9a25d8f131d23c3ccfeb650618118d46&code={}&grant_type=authorization_code".format(
        code)
    resp = Query().run(token_url, header={})
    data = json.loads(resp)
    return data["openid"]


if __name__ == "__main__":
    os.chdir(os.path.dirname(os.path.abspath(__file__)))

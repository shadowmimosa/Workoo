import os
from .request import Query
from .common import AccessToken
from urllib.parse import urlencode
import json
import requests
import urllib3


class SetButton(object):
    def __init__(self):
        pass

    def button(self):
        url = "https://api.weixin.qq.com/cgi-bin/menu/create?access_token={}".format(
            AccessToken().judge_token())
        data = {
            "button": [{
                "name":
                "鉴定查询",
                "sub_button": [{
                    "type": "click",
                    "name": "保修信息查询",
                    "key": "GUARANTEE"
                }, {
                    "type": "click",
                    "name": "Id激活锁查询",
                    "key": "ID_ACTIVATE"
                }, {
                    "type": "click",
                    "name": "Id黑白查询",
                    "key": "ID_BLACK_WHITE"
                },
                               {
                                   "type": "click",
                                   "name": "id无限查询（imei）",
                                   "key": "ID_WITH_IMEI"
                               },
                               {
                                   "type": "click",
                                   "name": "苹果验机报告查询",
                                   "key": "MAC_MACHINE"
                               }]
            },
                       {
                           "name":
                           "网络锁查询",
                           "sub_button": [{
                               "type": "click",
                               "name": "网络锁查询",
                               "key": "NETWORK_LOCK"
                           },
                                          {
                                              "type": "click",
                                              "name": "运营商查询",
                                              "key": "SERVICE_PROVIDE"
                                          },
                                          {
                                              "type": "click",
                                              "name": "官换机查询",
                                              "key": "OFFICIAL_CHANGE"
                                          },
                                          {
                                              "type": "click",
                                              "name": "苹果维修查询",
                                              "key": "MAC_REPAIR"
                                          },
                                          {
                                              "type": "click",
                                              "name": "过保激活时间查询",
                                              "key": "OVER_PROTECTION"
                                          }]
                       },
                       {
                           "name":
                           "会员充值",
                           "sub_button": [{
                               "type": "click",
                               "name": "序列号/imei互查",
                               "key": "IMEI_EACH"
                           },
                                          {
                                              "type": "click",
                                              "name": "推广二维码/送金额",
                                              "key": "EXTENDED_QR_CODE"
                                          },
                                          {
                                              "type": "click",
                                              "name": "我的账户信息",
                                              "key": "ACCOUNT_INFORMATION"
                                          },
                                          {
                                              "type": "view",
                                              "name": "在线充值",
                                              "url": r"https://open.weixin.qq.com/connect/oauth2/authorize?appid=wxb3c3f15d73d9c9b8&redirect_uri=http://wx.guojichaxun.cn/wx/pay&response_type=code&scope=snsapi_base&state=321#wechat_redirect"
                                            #   "url": r"https%3a%2f%2fopen.weixin.qq.com%2fconnect%2foauth2%2fauthorize%3fappid%3dwxb3c3f15d73d9c9b8%26redirect_uri%3dhttp%3a%2f%2fwx.guojichaxun.cn%2fwx%2fpay%26response_type%3dcode%26scope%3dsnsapi_base%26state%3d321%23wechat_redirect"
                                            #   "url": "http://wx.guojichaxun.cn/wx/pay"
                                          },
                                          {
                                              "type": "click",
                                              "name": "更多查询服务",
                                              "key": "MOVE_SERVICES"
                                          }]
                       }]
        }
        data_gb2312 = urlencode(data, encoding='gb2312')
        # response = requests.post(
        #     url=url,
        #     data=bytes(json.dumps(data, ensure_ascii=False), encoding='utf-8'))
        resp = Query().run(
            path=url,
            header={},  #"Content-Type": "application/x-www-form-urlencoded"},
            data=bytes(json.dumps(data, ensure_ascii=False), encoding='utf-8'))
        print(resp)


if __name__ == "__main__":
    # os.chdir(os.path.dirname(os.path.abspath(__file__)))
    SetButton().button()
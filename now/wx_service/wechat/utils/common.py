import os
import json
import time
from json.decoder import JSONDecodeError

from wechat.utils.request import Query
from wechat.models import ConfigInfo


class AccessToken(object):
    def __init__(self):
        pass

    def get_token(self):
        url = "https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid=wxb3c3f15d73d9c9b8&secret=9a25d8f131d23c3ccfeb650618118d46"
        timestamp = int(time.time())
        resp = Query().run(path=url, header={})
        data = json.loads(resp)
        # data["timestamp"] = timestamp + data["expires_in"]
        data["timestamp"] = timestamp + 7000

        # with open("./data/token.txt", "w", encoding="utf-8") as fn:
        #     fn.write(json.dumps(data))
        ConfigInfo.objects.update_token(data)

        return data

    def judge_token(self):
        # try:
        #     with open("./data/token.txt", "r", encoding="utf-8") as fn:
        #         data = json.loads(fn.read())
        # except FileNotFoundError:
        #     return self.get_token()["access_token"]

        data = ConfigInfo.objects.get_token()
        try:
            data = json.loads(data)
        except JSONDecodeError:
            data = self.get_token()
        else:
            if int(time.time()) > data["timestamp"]:
                data = self.get_token()
        finally:
            return data["access_token"]


def get_event(item=None, price=None):
    # with open("wechat/data/event_list.json", "r", encoding="utf-8") as fn:
    #     raw_data = json.loads(fn.read())
    raw_data = json.loads(ConfigInfo.objects.get_event())

    if item == None:
        return raw_data

    else:
        try:
            # with open("wechat/data/monthly.json", "w", encoding="utf-8") as fn:
            #     raw_data[sign]["count"] = int(price)
            # fn.write(json.dumps(raw_data))
            raw_data[item.upper()]["count"] = round(float(price), 2)
            ConfigInfo.objects.update_event(raw_data)
        except Exception as exc:
            print(exc)
            return {"status": "failed"}
        else:
            return {"status": "success"}


def monthly_price(item=None, price=None):
    # with open("wechat/data/monthly.json", "r", encoding="utf-8") as fn:
    #     raw_data = json.loads(fn.read())
    raw_data = json.loads(ConfigInfo.objects.get_monthly())

    if price == None:
        if item == None:
            return raw_data
        else:
            return raw_data[item]
    else:
        try:
            # with open("wechat/data/monthly.json", "w", encoding="utf-8") as fn:
            #     raw_data[item] = int(price)
            #     fn.write(json.dumps(raw_data))
            raw_data[item] = int(price)
            ConfigInfo.objects.update_monthly(raw_data)
        except Exception as exc:
            print(exc)
            return {"status": "failed"}
        else:
            return {"status": "success"}


def free_time(sign=None):
    if sign == None:
        # with open("wechat/data/free.txt", "r", encoding="utf-8") as fn:
        #     times = fn.readline().replace("\n", "")
        times = int(ConfigInfo.objects.get_free())

        return times
    else:
        try:
            # with open("wechat/data/free.txt", "w", encoding="utf-8") as fn:
            #     fn.write(sign)
            sign = int(sign)
            ConfigInfo.objects.update_free(sign)
        except:
            return {"status": "failed"}
        else:
            return {"status": "success"}


if __name__ == "__main__":
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    print(AccessToken())

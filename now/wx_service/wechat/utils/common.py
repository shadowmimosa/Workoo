import os
import json
import time

from wechat.utils.request import Query


class AccessToken(object):
    def __init__(self):
        pass

    def get_token(self):
        url = "https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid=wxb3c3f15d73d9c9b8&secret=9a25d8f131d23c3ccfeb650618118d46"
        timestamp = int(time.time())
        resp = Query().run(path=url, header={})
        data = json.loads(resp)
        data["timestamp"] = timestamp + data["expires_in"]

        with open("./data/token.txt", "w", encoding="utf-8") as fn:
            fn.write(json.dumps(data))

        return data

    def judge_token(self):
        try:
            with open("./data/token.txt", "r", encoding="utf-8") as fn:
                data = json.loads(fn.read())
        except FileNotFoundError:
            return self.get_token()["access_token"]

        if int(time.time()) < data["timestamp"]:
            return data["access_token"]
        else:
            data = self.get_token()
            return data["access_token"]


def get_event():
    with open("wechat/data/event_list.json", "r", encoding="utf-8") as fn:
        return json.loads(fn.read())


if __name__ == "__main__":
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    print(AccessToken())
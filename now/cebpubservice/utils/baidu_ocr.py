import os
import json
import time
import base64
import traceback

from utils.request import Query

req = Query().run

class BaiduToken(object):
    def __init__(self):
        pass

    def get_current_time(self):
        return int(time.time())

    def save_token(self, token):
        with open("./access_token.json", "w", encoding="utf-8") as fn:
            fn.write(
                json.dumps({
                    "token":
                    token,
                    "unavailable_time":
                    self.get_current_time() + 2592000
                }))

    def judge_token(self):
        try:
            with open("./access_token.json", "r", encoding="utf-8") as fn:
                data = json.loads(fn.read())
                if data["unavailable_time"] > self.get_current_time() + 60:
                    return data["token"]
                else:
                    return False
        except FileNotFoundError:
            return False

    def get_token(self):
        from config import BAIDUOCR
        token = self.judge_token()
        if token is False:
            host = 'https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id={client_id}&client_secret={client_secret}'.format(
                **BAIDUOCR)
            resp = req(
                host,
                header={'Content-Type': 'application/json; charset=UTF-8'},
                data={})

            if resp:
                token = json.loads(resp)["access_token"]
                self.save_token(token)
                return token
        else:
            return token


class BaiduOCR(object):
    def __init__(self):
        self.token = BaiduToken().get_token()

    def bytes2base64(self, pic):
        # with open(path, "rb") as fn:
        #     base64_data = base64.b64encode(fn.read())

        return base64.b64encode(pic)

    def get_word(self, image_base64):
        host = "https://aip.baidubce.com/rest/2.0/ocr/v1/general_basic?access_token={}".format(
            self.token)

        data = {
            "image": image_base64,
            "url": "",
            "language_type": "CHN_ENG",
            "detect_direction": "false",
            "detect_language": "false",
            "probability": "false",
        }
        resp = req(
            host,
            headers={"Content-Type": "application/x-www-form-urlencoded"},
            data=data)

        return json.loads(resp)

    def pic2word(self, pic):
        # base_obj = self.bytes2base64(pic)

        if isinstance(pic, bytes):
            base_obj = self.bytes2base64(pic)

        try:
            return self.get_word(base_obj)
        except:
            print("--->Error: the error is {}".format(traceback.format_exc()))
        else:
            pass
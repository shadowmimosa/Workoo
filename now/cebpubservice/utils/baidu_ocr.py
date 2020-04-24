import os
import json
import time
import base64
import traceback

from utils.log import logger
from utils.request import Query

req = Query().run


class BaiduToken(object):
    def __init__(self, config):
        self.config = config

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
        token = self.judge_token()
        if token is False:
            host = 'https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id={id}&client_secret={secret}'.format(
                **self.config)
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
    def __init__(self, config):
        self.config = config
        self.token = BaiduToken(config).get_token()

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

        result = json.loads(resp)
        if 'error_code' in result:
            error_code = result.get('error_code')

            if error_code == 110 or error_code == 111:
                self.__init__()
            elif error_code == 18:
                logger.info(f'QPS 超额, 等待0.5')
                time.sleep(0.5)
                return self.get_word(image_base64)
            else:
                logger.error('BaiduOcr is error: {}'.format(
                    result.get('error_msg')))
        else:
            return result

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
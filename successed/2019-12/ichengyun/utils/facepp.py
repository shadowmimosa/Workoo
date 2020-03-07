import os
import json
import time
import base64
import traceback

from utils.request import Query

requests = Query().run


class FaceOcr(object):
    def __init__(self):
        from config import FACEPP
        self.api_key = FACEPP["api_key"]
        self.api_secret = FACEPP["api_secret"]

    def bytes2base64(self, pic):
        # with open(path, "rb") as fn:
        #     base64_data = base64.b64encode(fn.read())

        return base64.b64encode(pic)

    def get_word(self, image_base64):
        host = "https://api-cn.faceplusplus.com/imagepp/v1/recognizetext"

        data = {
            "api_key": self.api_key,
            "api_secret": self.api_secret,
            "image_base64": image_base64,
        }
        resp = requests(
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
import json
from wechat.utils.request import Query
from wechat.utils.common import AccessToken


class QrCode(object):
    def __init__(self, openid):
        self.openid = openid
        self.ticket_path = "https://api.weixin.qq.com/cgi-bin/qrcode/create?access_token={}"
        self.qr_path = "https://mp.weixin.qq.com/cgi-bin/showqrcode?ticket={}"
        self.upload_path = "https://api.weixin.qq.com/cgi-bin/media/upload?access_token={}&type={}"
        self.request = Query()
        self.token = AccessToken().judge_token

    def get_ticket(self):
        data = {
            "expire_seconds": 2592000,
            "action_name": "QR_STR_SCENE",
            "action_info": {
                "scene": {
                    "scene_str": self.openid
                }
            }
        }

        resp = self.request.run(
            path=self.ticket_path.format(self.token()),
            header={},
            data=data)
        response = json.loads(resp)
        if "errcode" in data.keys():
            if response["errcode"] == 40001:
                AccessToken().get_token()
                response = json.loads(
                    self.request.run(
                        path=self.ticket_path.format(
                            self.token()),
                        header={},
                        data=data))

        print(response)
        self.ticket = response["ticket"]

    def get_qrcode(self):
        resp = self.request.run(
            path=self.qr_path.format(self.ticket), header={}, sign=1)

        self.qrcode = resp

    def upload_media(self):
        # params = (
        #     ('access_token', self.token()),
        #     ('type', 'image'),
        # )

        files = {
            'media': ('qrcode.jpg', self.qrcode),
            # 'media': ('qrcode.jpg', open('qrcode.jpg', 'rb')),
        }

        # resp = requests.post(
        #     url=self.upload_path.format(self.token(), "image"),
        #     # 'https://api.weixin.qq.com/cgi-bin/media/upload',
        #     # params=params,
        #     files=files)
        resp = self.request.run(
            path=self.upload_path.format(self.token(), "image"),
            files=files)
        print(resp)

        return json.loads(resp)["media_id"]

    def run(self):
        self.get_ticket()
        self.get_qrcode()
        return self.upload_media()
        # print(
        #     self.request.run(
        #         "https://api.weixin.qq.com/cgi-bin/material/batchget_material?access_token={}"
        #         .format(self.token()),
        #         data={
        #             "type": "image",
        #             "offset": 0,
        #             "count": 20
        #         }))


if __name__ == "__main__":
    QrCode().get_ticket()

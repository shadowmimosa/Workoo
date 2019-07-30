# Create your tasks here
from __future__ import absolute_import, unicode_literals
import time
import json
from celery import shared_task

from wechat.utils.common import AccessToken
from wechat.utils.service import DealService
from wechat.utils.request import Query

# from wechat.utils.analysis import TextMsg
# from now.wx_service.wechat.utils.analysis import TextMsg
# from now.wx_service.wechat.utils.service import DealService


@shared_task
def main(weid, openid, current, imei):
    reply_content = DealService(
        openid=openid, current=current, imei=imei).main()

    url = "https://api.weixin.qq.com/cgi-bin/message/custom/send?access_token={}".format(
        AccessToken().judge_token())
    print(url)
    data = {
        "touser": openid,
        "msgtype": "text",
        "text": {
            "content": str(reply_content)
        }
    }
    print(data)
    resp = Query().run(
        path=url,
        header={},
        data=bytes(json.dumps(data, ensure_ascii=False), encoding='utf-8'))

    print(resp)
    # if json.loads(resp)["errcode"]==0:
    #     pass
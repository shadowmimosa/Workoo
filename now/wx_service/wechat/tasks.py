# Create your tasks here
from __future__ import absolute_import, unicode_literals
import time
import json
from celery import shared_task

from wechat.utils.common import AccessToken
from wechat.utils.service import DealService, AccountInfo
from wechat.utils.request import Query
from wechat.utils.qr_code import QrCode

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
        data=bytes(
            "\n\n".join((json.dumps(data, ensure_ascii=False),
                         AccountInfo(openid).money_info())),
            encoding='utf-8'))

    print(resp)


@shared_task
def qr_code(openid):
    media_id = QrCode(openid).run()
    data = {
        "touser": openid,
        "msgtype": "image",
        "image": {
            "media_id": media_id
        }
    }
    resp = Query().run(
        path=
        "https://api.weixin.qq.com/cgi-bin/message/custom/send?access_token={}"
        .format(AccessToken().judge_token()),
        header={},
        data=bytes(
            "\n\n".join((json.dumps(data, ensure_ascii=False),
                         AccountInfo(openid).money_info())),
            encoding='utf-8'))


# nohup celery -A query_service.mycelery worker -l info &
# celery worker -A tasks --loglevel=info -P gevent -c 100
# uwsgi --ini uwsgi/uwsgi.ini
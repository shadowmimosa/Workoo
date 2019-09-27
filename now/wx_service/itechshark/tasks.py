# Create your tasks here
from __future__ import absolute_import, unicode_literals
import time
import json
from celery import shared_task

from itechshark.utils.request import Query


@shared_task
def qr_code(openid):
    resp = Query().run(
        path=
        "https://api.weixin.qq.com/cgi-bin/message/custom/send?access_token={}"
        .format(AccessToken().judge_token()),
        header={},
        data=bytes(json.dumps(data, ensure_ascii=False), encoding='utf-8'))


# nohup celery -A wx_service.mycelery worker -l info &
# celery worker -A tasks --loglevel=info -P gevent -c 100
# celery multi start w1 -A wx_service.mycelery -l info  -c 10 --logfile=./log/celerylog.log --pidfile=./celery/celerypid.pid

# uwsgi --ini uwsgi/uwsgi.ini
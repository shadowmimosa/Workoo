import time
import datetime
import json
import dateutil.relativedelta
from decimal import Decimal

from django.db import models
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned

# import wechat.utils.common as common
# from wechat.utils.common import free_time


class UserInfoManager(models.Manager):
    def insert_user(self, openid, balance=0, current="null"):
        self.create(openid=openid, balance=balance, current=current)

    def query_current(self, openid):
        try:
            obj = self.get(openid__exact=openid)
        except ObjectDoesNotExist:
            return False
        else:
            return obj.current

    def query_balance(self, openid):
        return self.get(openid__exact=openid).balance

    def query_count(self, openid, sign):
        from wechat.utils.common import free_time
        obj = self.get(openid__exact=openid)
        sign = sign.lower()
        times = int(free_time())
        # times = ConfigInfoManager.get_free()

        today = int(time.strftime("%d"))
        data = eval("obj.{}".format(sign)).split("-")
        if int(data[-1]) != today:
            exec(("obj.{}='0-{}'".format(sign, today)))
            obj.save()
            return times
        elif int(data[0]) <= times:
            return times - int(data[0])
        else:
            return False

    def update_count(self, openid, sign):
        obj = self.get(openid__exact=openid)
        sign = sign.lower()
        date = time.strftime('%d')
        count = int(eval("obj.{}".format(sign)).split("-")[0]) + 1
        exec("obj.{} = '{}-{}'".format(sign, count, date))
        obj.save()

    def update_current(self, openid, current):
        obj = self.get(openid__exact=openid)
        obj.current = current
        obj.save()

    def update_balance(self, openid, balance):
        obj = self.get(openid__exact=openid)
        obj.balance = "{:.2f}".format(
            Decimal(float(obj.balance) + float(balance)))
        obj.save()

    def insert_promoter(self, openid, promoter):
        self.create(openid=openid, promoter=promoter)

    def query_promotions(self, openid):
        return self.get(openid__exact=openid).promotions

    def update_promotions(self, openid):
        obj = self.get(openid__exact=openid)
        obj.promotions = int(obj.promotions) + 1
        obj.save()
        self.update_balance(openid, "1.99")


class TransactionInfoManager(models.Manager):
    def query_type(self, out_trade_no):
        return self.get(out_trade_no__exact=out_trade_no).type

    def insert_transaction(self, out_trade_no, openid, amount, type, status):
        self.create(
            out_trade_no=out_trade_no,
            openid=openid,
            amount=amount,
            type=type,
            status=status)

    def update_status(self, out_trade_no, status):
        obj = self.get(out_trade_no__exact=out_trade_no)
        obj.status = status
        obj.save()


class MonthInfoManager(models.Manager):
    def judge_time(self):
        """判断包月是否过期

        ``return``
        
            0: 已过期
            1: 未过期
        """
        create_time = self.obj.create_time
        months = self.obj.months

        expiration_time = create_time + dateutil.relativedelta.relativedelta(
            months=int(months))
        if datetime.datetime.now() > expiration_time:
            return None
        else:
            return expiration_time.strftime("%Y-%m-%d")

    def judge_type(self, openid):
        try:
            self.obj = self.get(openid__exact=openid, type__exact="1")

        except ObjectDoesNotExist:
            try:
                self.obj = self.get(openid__exact=openid, type__exact="2")
            except ObjectDoesNotExist:
                return 0
            else:
                self.type = 2
                return 1
        except MultipleObjectsReturned:
            print("MultipleObjectsReturned")
        else:
            self.type = 1
            return 1

    def insert_user(self, openid, months=1, _type=1):
        # obj = self.get(openid__exact=openid, type__exact="1")
        # obj.months = int(obj.months) + int(months)
        # obj.save()
        try:
            obj = self.get(openid__exact=openid, type__exact="1")
        except ObjectDoesNotExist:
            self.create(openid=openid, months=months, type=_type)
        else:
            obj.months = int(obj.months) + int(months)
            obj.save()

    def add_count(self, openid):
        obj = self.get(openid__exact=openid, type__exact="1")
        obj.count = int(obj.count) + 1
        obj.save()

    def query_user(self, openid, sign=None):
        """查询用户是否包月

        `return`

            0: 非包月用户
            1: 包月且次数足够
            2: imei 包月
            -1: 包月且次数不足
            -2: 包月已过期
        """
        from wechat.utils.common import get_count
        if self.judge_type(openid) == 1:
            return_code = self.judge_time()
            if return_code == None:
                self.obj.type = "-1"
                self.obj.save()
                return 0
            else:
                if sign == None:
                    if self.type == 1:
                        if int(self.obj.count) < get_count():
                            return 1
                        else:
                            return -1
                    elif self.type == 2:
                        return 2
                else:
                    if self.type == 1:
                        if int(self.obj.count) < get_count():
                            return 1, return_code
                        else:
                            return -1, return_code
                    elif self.type == 2:
                        return 2, return_code
        else:
            return 0

        # except PermissionError as exc:
        #     print(exc)
        #     print(exc.args[0])
        #     print(exc.args[1])


class ConfigInfoManager(models.Manager):
    def init(self):
        try:
            self.get(id__exact=1)
        except ObjectDoesNotExist:
            self.create(
                token="None",
                free="1",
                count="50",
                monthly=
                '{"month_1": 50, "month_3": 100, "month_6": 200, "month_imei": 80}',
                event=json.dumps({
                    'GUARANTEE': {
                        'name': '保修信息查询',
                        'count': '0.1'
                    },
                    'ID_ACTIVATE': {
                        'name': 'Id激活锁查询',
                        'count': '0.1'
                    },
                    'ID_BLACK_WHITE': {
                        'name': 'Id黑白查询',
                        'count': '0.2'
                    },
                    'ID_WITH_IMEI': {
                        'name': 'id无限查询（imei）',
                        'count': '0.2'
                    },
                    'MAC_MACHINE': {
                        'name': '苹果验机报告查询',
                        'count': '1.99'
                    },
                    'NETWORK_LOCK': {
                        'name': '网络锁查询',
                        'count': '0.49'
                    },
                    'SERVICE_PROVIDE': {
                        'name': '运营商查询',
                        'count': '0.95'
                    },
                    'OFFICIAL_CHANGE': {
                        'name': '官换机查询',
                        'count': '0.2'
                    },
                    'MAC_REPAIR': {
                        'name': '苹果维修查询',
                        'count': '0.2'
                    },
                    'OVER_PROTECTION': {
                        'name': '过保激活时间查询',
                        'count': '1.5'
                    },
                    'IMEI_EACH': {
                        'name': '序列号/imei互查',
                        'count': '0.45'
                    },
                    'EXTENDED_QR_CODE': {
                        'name': '推广二维码/送金额'
                    },
                    'ACCOUNT_INFORMATION': {
                        'name': '我的账户信息'
                    },
                    'RECHARGE': {
                        'name': '在线充值'
                    },
                    'MOVE_SERVICES': {
                        'name': '更多查询服务'
                    },
                    'GUARANTEE_QUERY': {
                        'name': '保修查询',
                        'count': '0.1'
                    },
                    'ID_QUERY': {
                        'name': 'ID查询',
                        'count': '0.15'
                    },
                    'ID_BLACK_WHITE_': {
                        'name': 'ID黑白查询',
                        'count': '0.35'
                    },
                    'TYPE_CHECK': {
                        'name': '型号检查',
                        'count': '0.15'
                    }
                },
                                 ensure_ascii=False))

    def get_token(self):
        return self.get(id__exact=1).token

    def update_token(self, content):
        obj = self.get(id__exact=1)
        obj.token = json.dumps(content)
        obj.save()

    def get_free(self):
        return self.get(id__exact=1).free

    def update_free(self, content):
        obj = self.get(id__exact=1)
        obj.free = content
        obj.save()

    def get_monthly(self):
        return self.get(id__exact=1).monthly

    def update_monthly(self, content):
        obj = self.get(id__exact=1)
        obj.monthly = json.dumps(content)
        obj.save()

    def get_event(self):
        return self.get(id__exact=1).event

    def update_event(self, content):
        obj = self.get(id__exact=1)
        obj.event = json.dumps(content, ensure_ascii=False)
        obj.save()

    def query_count(self):
        return int(self.get(id__exact=1).count)

    def update_count(self, count):
        obj = self.get(id__exact=1)
        obj.count = int(count)
        obj.save()

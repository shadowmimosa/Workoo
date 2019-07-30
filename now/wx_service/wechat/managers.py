from decimal import Decimal
from django.db import models


class UserInfoManager(models.Manager):
    def insert_user(self, openid, balance=0, current="null"):
        self.create(openid=openid, balance=balance, current=current)

    def query_current(self, openid):
        return self.get(openid__exact=openid).current

    def query_balance(self, openid):
        return self.get(openid__exact=openid).balance

    def update_current(self, openid, current):
        obj = self.get(openid__exact=openid)
        obj.current = current
        obj.save()

    def update_balance(self, openid, balance):
        obj = self.get(openid__exact=openid)
        obj.balance = "{:.2f}".format(
            Decimal(float(obj.balance) + float(balance)))
        obj.save()


class TransactionInfoManager(models.Manager):
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

from django.db import models

from .managers import UserInfoManager, TransactionInfoManager


class BaseTable(models.Model):
    create_time = models.DateTimeField(verbose_name='创建时间', auto_now_add=True)
    update_time = models.DateTimeField('更新时间', auto_now=True)

    class Meta:
        abstract = True
        verbose_name = "公共字段表"
        db_table = "BaseTable"


class UserInfo(BaseTable):
    class Meta:
        verbose_name = '用户信息'
        db_table = 'user_info'

    openid = models.CharField(
        verbose_name='用户名', max_length=50, unique=True, null=False)
    balance = models.CharField(
        verbose_name='余额', max_length=10, null=False, default=0)
    current = models.CharField(
        verbose_name='当前查询项目', max_length=50, default="null")

    objects = UserInfoManager()


class TransactionInfo(BaseTable):
    class Meta:
        verbose_name = '交易信息'
        db_table = 'transaction_info'

    out_trade_no = models.CharField(
        verbose_name='商户订单号', max_length=32, unique=True, null=False)
    openid = models.CharField(verbose_name='用户名', max_length=50, null=False)
    amount = models.CharField(verbose_name='金额', max_length=10, null=False)
    type = models.CharField(verbose_name='交易类型', max_length=10, null=False)
    status = models.CharField(verbose_name='交易状态', max_length=10, null=False)

    objects = TransactionInfoManager()
from django.db import models

from .managers import UserInfoManager, TransactionInfoManager, MonthInfoManager, ConfigInfoManager


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
    guarantee = models.CharField(verbose_name='保修查询', max_length=10, default=0)
    id_activate = models.CharField(
        verbose_name='ID 锁', max_length=10, default=0)
    id_black_white = models.CharField(
        verbose_name='ID 黑白', max_length=10, default=0)

    objects = UserInfoManager()


class TransactionInfo(BaseTable):
    class Meta:
        """
        `type`

            -1: 扣费
            1: 充值
            2: 扣包月次数
        """
        verbose_name = '交易信息'
        db_table = 'transaction_info'

    out_trade_no = models.CharField(
        verbose_name='商户订单号', max_length=32, unique=True, null=False)
    openid = models.CharField(verbose_name='用户名', max_length=50, null=False)
    amount = models.CharField(verbose_name='金额', max_length=10, null=False)
    type = models.CharField(verbose_name='交易类型', max_length=10, null=False)
    status = models.CharField(verbose_name='交易状态', max_length=10, null=False)

    objects = TransactionInfoManager()


class MonthInfo(BaseTable):
    class Meta:
        """
        `type`

            1: 包月中
            -1: 包月过期
        """
        verbose_name = '包月信息'
        db_table = 'month_info'

    openid = models.CharField(verbose_name='用户名', max_length=50, null=False)
    count = models.CharField(
        verbose_name='已查询次数', max_length=10, null=False, default=0)
    type = models.CharField(
        verbose_name='类型', max_length=10, null=False, default=0)
    months = models.CharField(
        verbose_name='包月', max_length=10, null=False, default=0)

    objects = MonthInfoManager()


class ConfigInfo(BaseTable):
    class Meta:
        """
        """
        verbose_name = '配置表'
        db_table = 'config'

    token = models.CharField(
        verbose_name='token', max_length=2048, null=False, default=None)
    free = models.CharField(
        verbose_name='每日免费次数', max_length=10, null=False, default=1)
    monthly = models.CharField(
        verbose_name='包月配置', max_length=2048, null=False, default=None)
    event = models.CharField(
        verbose_name='事件配置', max_length=2048, null=False, default=None)

    objects = ConfigInfoManager()

ConfigInfo.objects.init()

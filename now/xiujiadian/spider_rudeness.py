import csv
from loguru import logger
from jsonpath import jsonpath

from utils import request, mongo
from config import TOKEN


class SpiderMan():
    def __init__(self) -> None:
        self.login_header = {
            'User-Agent':
            'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36 MicroMessenger/7.0.9.501 NetType/WIFI MiniProgramEnv/Windows WindowsWechat',
            'cityId': '320600',
            'cityName': '%E5%8D%97%E9%80%9A%E5%B8%82',
            'content-type': 'application/json',
            'orderChannelId': '',
            'provinceId': '320000',
            'provinceName': '%E6%B1%9F%E8%8B%8F%E7%9C%81',
            'token': TOKEN,
            'shopId': '10005',
            'Accept-Encoding': 'gzip, deflate, br'
        }

    def detail(self):
        uri = f'https://api-saas.xiujiadian.com/quotation/getQuotationDetailV2?quotationId={self.quotation_id}&show=2'

        resp = request(uri, self.login_header, json=True)

        self.detail_item = resp.get('data')

        self.writer()

    def get_price(self, obj=None, key=None):
        obj = obj if obj else self.detail_item

        value = jsonpath(obj, f'$..{key}')[0]

        if not value:
            return None
        elif isinstance(value, int):
            return value / 100
        else:
            return value

    def writer(self):
        mongo.insert(self.detail_item, 'xiujiadian')

        needed = {
            '产品名': self.detail_item.get('productName'),
            '已选择': self.detail_item.get('selectedInfo'),
            '总价': self.detail_item.get('totalPrice') / 100,
            '配件包干费': self.get_price(key='accessoryFee'),
            '技术服务费': self.get_price(key='serviceFee'),
            '路费往返费': self.get_price(key='transportationFee'),
            '检测费': self.get_price(key='checkFee'),
            '保修费': self.get_price(key='guaranteeFee'),
            '工时费': self.get_price(key='hourlyWage'),
            '技术费': self.get_price(key='technologyFee'),
            '价格说明': self.get_price(key='specialInstruction'),
        }
        writer(needed)
        logger.info('已插入')

    def run(self):
        writer(init=True)

        for self.quotation_id in range(2920000, 2930000):
            self.detail()


def writer(obj=None, init=False):
    header = [
        '产品名', '已选择', '总价', '配件包干费', '技术服务费', '路费往返费', '检测费', '保修费', '工时费',
        '技术费', '价格说明'
    ]
    with open('./detail.csv', 'a', newline='', encoding='utf-8') as fn:
        writer = csv.DictWriter(fn, header)
        writer.writeheader() if init else writer.writerow(obj)


if __name__ == '__main__':
    spider = SpiderMan()
    spider.run()

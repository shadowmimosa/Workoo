import csv
from loguru import logger
from jsonpath import jsonpath

from utils import request, mongo
from config import TOKEN


class SpiderMan():
    def __init__(self) -> None:
        self.header = {
            'User-Agent':
            'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36 MicroMessenger/7.0.9.501 NetType/WIFI MiniProgramEnv/Windows WindowsWechat',
            'cityId': '320600',
            'cityName': '%E5%8D%97%E9%80%9A%E5%B8%82',
            'content-type': 'application/json',
            'orderChannelId': '',
            'provinceId': '320000',
            'provinceName': '%E6%B1%9F%E8%8B%8F%E7%9C%81',
            'shopId': '10005',
            'Accept-Encoding': 'gzip, deflate, br'
        }
        self.login_header = {
            'User-Agent':
            'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36 MicroMessenger/7.0.9.501 NetType/WIFI MiniProgramEnv/Windows WindowsWechat',
            'cityId': '320600',
            'cityName': '%E5%8D%97%E9%80%9A%E5%B8%82',
            'content-type': 'application/json',
            'orderChannelId': '',
            'provinceId': '320000',
            'provinceName': '%E6%B1%9F%E8%8B%8F%E7%9C%81',
            'shopId': '10005',
            'token': TOKEN,
            'Accept-Encoding': 'gzip, deflate, br'
        }

        self.first = {}
        self.second = {}
        self.third = {}
        self.fourth = {}
        self.fifth = {}
        self.sixth = {}
        self.seventh = {}
        self.eighth = {}

        self.select_list = ['', '', '', '', '']
        self.quotation_uri = 'https://api-saas.xiujiadian.com/quotation/productQuotationProcessV3'
        super().__init__()

    def get_token(self):
        uri = ''
        resp = request()

    def deal_step(self, item: dict):
        for data in item.get('data'):
            if data.get('step') == 1:
                self.first.update(data)
            elif data.get('step') == 2:
                self.second.update(data)
            elif data.get('step') == 3:
                self.third.update(data)
            elif data.get('step') == 4:
                self.fourth.update(data)
            elif data.get('step') == 5:
                self.fifth.update(data)
            elif data.get('step') == 6:
                self.sixth.update(data)
            elif data.get('step') == 7:
                self.seventh.update(data)
            elif data.get('step') == 8:
                self.eighth.update(data)

            self.current = data.get('step')

        if self.current == 2:
            self.step_3()
        elif self.current == 3:
            second_item = self.second.get('dataList')[0].get('item')
            self.one_category_id = second_item.get('categOneId')
            self.product_id = second_item.get('productId')
            self.select_list[1] = second_item.get('name')

            logger.warning(
                f'second length is {len(self.second.get("dataList"))}')
            self.step_4()
        elif self.current == 4:
            self.step_5()
        elif self.current == 8:
            self.clear()

        # if self.current < 8:
        #     eval(f'self.step_{self.current+1}()')
        # else:
        #     self.clear()


    def step_1(self):
        data = {
            'step': 1,
            'orderId': '',
            'pageSize': 50,
            'showProductLevelTwoCategoryId': self.category_id
        }

        resp = request(self.quotation_uri, self.header, data, json=True)
        if resp.get('status') != 200:
            return

        self.deal_step(resp)

    def step_3(self):
        self.select_list[0] = jsonpath(self.first, '$..showTariffName')[0]

        for item in self.second.get('dataList'):
            item = item.get('item')
            category_id = jsonpath(self.first, '$..showServCategId')[0]
            self.one_category_id = item.get('categOneId')
            self.product_id = item.get('productId')
            self.select_list[1] = item.get('name')

            data = {
                'step': 3,
                'orderId': '',
                'pageSize': 50,
                'showProductLevelTwoCategoryId': self.category_id,
                'showProductServiceCategoryId': category_id,
                'showProductLevelOneCategoryId': self.one_category_id,
                'showProductId': self.product_id
            }

            resp = request(self.quotation_uri, self.header, data, json=True)

            self.deal_step(resp)

    def step_4(self):
        for item in self.third.get('dataList'):
            item = item.get('item')
            self.brand_id = item.get('brandId')
            self.select_list[2] = item.get('name')

            data = {
                'step': 4,
                'orderId': '',
                'pageSize': 50,
                'showProductId': self.product_id,
                'itemIds': [],
                'brandId': self.brand_id
            }

            resp = request(self.quotation_uri, self.header, data, json=True)

            self.deal_step(resp)

    def step_5(self):
        for item in self.fourth.get('dataList'):
            item = item.get('item')
            self.item_id = item.get('itemId')
            self.select_list[3] = item.get('itemName')
            self.fourth_item = item

            data = {
                'step': 5,
                'orderId': '',
                'pageSize': 50,
                'showProductId': self.product_id,
                'itemIds': [self.item_id],
                'brandId': self.brand_id
            }

            resp = request(self.quotation_uri, self.header, data, json=True)

            self.deal_step(resp)

    # def step_8(self):
    #     uri = 'https://api-saas.xiujiadian.com/quotation/productNotClearV2'
    #     data = {
    #         'step': 5,
    #         'orderId': '',
    #         'pageSize': 50,
    #         'showProductId': 11283,
    #         'itemIds': [1709],
    #         'brandId': 1024
    #     }

    #     resp = request(uri, self.header, data, json=True)
    #     print(resp)

    def build_select(self):
        result = ' > '.join(filter(None, self.select_list)) + ' '

        return result

    def clear(self):
        uri = 'https://api-saas.xiujiadian.com/quotation/productNotClearV2'
        for item in self.eighth.get('dataList'):
            item = item.get('item')
            serv_categ_id = item.get('servCategId')
            two_catagory_id = item.get('categId')
            serv_categ_name = jsonpath(self.first, '$..showTariffName')[0]
            self.select_list[4] = self.select_list[1]

            data = {
                'selectedInfo':
                self.build_select(),
                'step':
                8,
                'productServiceCategoryId':
                serv_categ_id,
                'showProductLevelTwoCategoryId':
                self.category_id,
                'showProductId':
                self.product_id,
                'orderId':
                '',
                'itemIds': [self.item_id],
                'showProductServiceCategoryId':
                serv_categ_id,
                'showServCategName':
                serv_categ_name,
                'showTariffName':
                serv_categ_name,
                'showProductLevelOneCategoryId':
                self.one_category_id,
                'productLevelTwoCategoryId':
                two_catagory_id,
                'productLevelServCategId':
                serv_categ_id,
                'productQuotationDetailList': [{
                    'typeId':
                    self.fourth_item.get('faultCategId'),
                    'typeName':
                    self.fourth_item.get('faultCategName'),
                    'itemId':
                    self.fourth_item.get('itemId'),
                    'itemName':
                    self.fourth_item.get('itemName'),
                    'quantity':
                    1,
                    'price':
                    None
                }],
                'showProductName':
                self.select_list[1],
                'brandId':
                self.brand_id
            }

            resp = request(uri, self.login_header, data, json=True)

            for self.clear_item in resp.get('data'):
                self.detail()

    def detail(self):
        quotation_id = self.clear_item.get('quotationId')
        uri = f'https://api-saas.xiujiadian.com/quotation/getQuotationDetailV2?quotationId={quotation_id}&show=2'

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
        row = {
            'step_1': self.first,
            'step_2': self.second,
            'step_3': self.third,
            'step_4': self.fourth,
            'step_5': self.fifth,
            'step_6': self.sixth,
            'step_7': self.seventh,
            'step_8': self.eighth,
            'clear': self.clear_item,
            'detail': self.detail_item,
        }
        # mongo.insert(row, 'xiujiadian')

        needed = {
            '产品名': self.clear_item.get('productName'),
            '已选择': self.clear_item.get('selectedInfo'),
            '总价': self.clear_item.get('totalPrice')/100,
            '配件包干费': self.get_price(key='accessoryFee'),
            '技术服务费': self.get_price(key='serviceFee'),
            '路费往返费': self.get_price(key='transportationFee'),
            '检测费': self.get_price(key='checkFee'),
            '保修费': self.get_price(key='guaranteeFee'),
            '工时费': self.get_price(key='hourlyWage'),
            '技术费': self.get_price(key='technologyFee'),
            '价格说明': self.get_price(key='specialInstruction'),

            # "afterDiscountCheckFee": null,
            # "afterDiscountGuaranteeFee": null,
            # "afterDiscountHourlyWage": null,
            # "afterDiscountTotalPrice": null,
            # "afterDiscountTransportationFee": null,

            # "discountCheckFee": null,
            # "discountGuaranteeFee": null,
            # "discountHourlyWage": null,
            # "discountTotalPrice": null,
            # "discountTransportationFee": null,
        }
        writer(needed)
        logger.info('已插入')

    def run(self):
        writer(init=True)
        for category_id in range(2696, 10000):
        # for category_id in range(2699, 10000):
            self.first = {}
            self.second = {}
            self.third = {}
            self.fourth = {}
            self.fifth = {}
            self.sixth = {}
            self.seventh = {}
            self.eighth = {}
            self.select_list = ['', '', '', '', '']

            self.category_id = f'{category_id}'
            self.step_1()


def writer(obj=None, init=False):
    header = [
        '产品名', '已选择', '总价', '配件包干费', '技术服务费', '路费往返费', '检测费', '保修费', '工时费',
        '技术费', '价格说明'
    ]
    with open('./detail.csv', 'a', newline='', encoding='utf-8') as fn:
        writer = csv.DictWriter(fn, header)
        writer.writeheader() if init else writer.writerow(obj)


if __name__ == '__main__':
    # writer({
    #     '产品名': '定频挂机空调维修（1-1.5P）',
    #     '价格说明':
    #     '1.路途往返费：工程师到用户家以及返回途中，时间和交通工具的成本\n2.检测费：机器检测或确认故障的费用\n3.工时费：在维修服务中所需的维修时间成本\n4.保修费：机器保修所收取的费用\n5.技术服务费：在维修服务中处理故障的技术费用\n6.配件包干费：维修中使用材料、更换或维修配件的包干费用（含损耗、问题新件更换，除需求产品）\n7.工艺费：维修特殊故障中因维修难度、辅材使用及维修后复原、排查危害所产生的费用',
    #     '保修费': None,
    #     '工时费': 6000,
    #     '已选择': '维修 > 定频挂机 > 格力 > 不制热/效果不好 > 定频挂机 ',
    #     '总价': 37500,
    #     '技术服务费': 12800,
    #     '技术费': None,
    #     '检测费': None,
    #     '路费往返费': 2500,
    #     '配件包干费': 13100
    # })
    spider = SpiderMan()
    spider.run()

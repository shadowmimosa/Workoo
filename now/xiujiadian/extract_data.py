import csv
from loguru import logger
from jsonpath import jsonpath

from utils import mongo


def get_price(obj=None, key=None):
    value = jsonpath(obj, f'$..{key}')[0]

    if not value:
        return None
    elif isinstance(value, int):
        return value / 100
    else:
        return value


def main():
    writer(init=True)

    result = mongo.select('xiujiadian', {}, limit=200)

    while result:
        neededs = []

        for detail in result:
            needed = {
                '产品名': detail.get('productName'),
                '已选择': detail.get('selectedInfo'),
                '总价': detail.get('totalPrice') / 100,
                '配件包干费': get_price(detail, key='accessoryFee'),
                '技术服务费': get_price(detail, key='serviceFee'),
                '路费往返费': get_price(detail, key='transportationFee'),
                '检测费': get_price(detail, key='checkFee'),
                '保修费': get_price(detail, key='guaranteeFee'),
                '工时费': get_price(detail, key='hourlyWage'),
                '技术费': get_price(detail, key='technologyFee'),
                '价格说明': get_price(detail, key='specialInstruction'),

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
            neededs.append(needed)

        writer(neededs)
        result = mongo.select('xiujiadian',
                              {'_id': {
                                  '$gt': result[-1].get('_id')
                              }},
                              limit=200)


def writer(obj=None, init=False):
    header = [
        '产品名', '已选择', '总价', '配件包干费', '技术服务费', '路费往返费', '检测费', '保修费', '工时费',
        '技术费', '价格说明'
    ]
    with open('./detail.csv', 'a', newline='', encoding='utf-8') as fn:
        writer = csv.DictWriter(fn, header)
        if isinstance(obj, list):
            writer.writerows(obj)
        else:
            writer.writeheader() if init else writer.writerow(obj)


if __name__ == '__main__':
    main()

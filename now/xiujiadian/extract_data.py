from loguru import logger
from jsonpath import jsonpath

from utils import mongo, excel

header = [
    '产品名', '已选择', '总价', '其它产品名', '配件包干费', '技术服务费', '路费往返费', '检测费', '保修费',
    '工时费', '技术费', '零件费', '价格', '服务费', '交通费', '更新时间'
]

excel.init_sheet(header)


def get_price(obj=None, key=None):
    value = jsonpath(obj, f'$..{key}')[0]

    if not value:
        return None
    elif isinstance(value, int):
        return value / 100
    else:
        return value


def main():
    count = 0
    result = mongo.select('xiujiadian', {}, limit=200)

    while result:
        count += 200
        for detail in result:
            extract(detail.get('productQuotationDetailList'),
                    detail.get('selectedInfo'), detail.get('updateTime'))
            extract(detail.get('commonProductQuotationDetailList'), )
            extract(detail.get('incrementProductQuotationDetailList'))
            extract(detail.get('otherServiceQuotationDetailList'))
            extract(detail.get('specialProductQuotationDetailList'))

        result = mongo.select('xiujiadian',
                              {'_id': {
                                  '$gt': result[-1].get('_id')
                              }},
                              limit=200)
        logger.info(f'完成 {count} 条')

    excel.save()


def deal_price(content):
    if isinstance(content, int):
        return content / 100

    return content


def extract(obj, selected=None, update=None):
    for item in obj:
        temp = item.get('productQuotationFee')
        if temp:
            needed = {
                '配件包干费': temp.get('accessoryFee'),
                '技术服务费': temp.get('serviceFee'),
                '路费往返费': temp.get('transportationFee'),
                '检测费': temp.get('checkFee'),
                '保修费': temp.get('guaranteeFee'),
                '工时费': temp.get('hourlyWage'),
                '技术费': temp.get('technologyFee'),
                '总价': temp.get('totalPrice'),
                '已选择': selected,
                '产品名': item.get('itemName'),
                '更新时间': update,
            }
        else:
            needed = {
                '检测费': item.get('checkFee'),
                '工时费': item.get('hourFee'),
                '零件费': item.get('partPrice'),
                '价格': item.get('price'),
                '服务费': item.get('servicePrice'),
                '技术费': item.get('technologyFee'),
                # '总价': item.get('totalPrice') / 100,
                '交通费': item.get('trafficFee'),
                '其它产品名': item.get('itemName')
            }

        needed = {x: deal_price(needed[x]) for x in needed}
        needed.update({'类型': item.get('typeName')})

        # neededs.append(needed)

        excel.write(needed)


if __name__ == '__main__':
    main()

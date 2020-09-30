import csv
from loguru import logger
from concurrent.futures.thread import ThreadPoolExecutor, threading

from utils import request, run_func, mongo
from config import ACCESS_TOKEN, RUN_SIGN, DEBUG


def remove_charater(content: str):
    return content.replace('\n', '').replace('\t',
                                             '').replace('\r',
                                                         '').replace(' ', '')


@run_func()
def get_shop_phone(shop_id):
    uri = f'https://luban.snssdk.com/shop/info?id={shop_id}'
    header = {
        'User-Agent':
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.102 Safari/537.36',
        'Accept': '*/*',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.9'
    }
    resp = request(uri, header, json=True)
    return resp.get('data').get('company_name'), resp.get('data').get('mobile')


@run_func()
def get_good_phone(good_id):
    uri = f'https://ec.snssdk.com/product/lubanajaxstaticitem?id={good_id}'
    header = {
        'User-Agent':
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.102 Safari/537.36',
        'Accept': 'application/json, text/plain, */*',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.9'
    }
    resp = request(uri, header, json=True)
    return resp.get('data').get('mobile'), resp.get('data').get(
        'shop_id'), resp.get('data').get('pay_type')


@run_func()
def deal_price(_min, _max):
    return '-'.join(set((_min, _max)))


@run_func()
def detail(data: dict, sort_type):

    info = {}
    good_id = data.get('code')
    info['产品价格'] = deal_price(data.get('price_min'), data.get('price_max'))
    info['24小时销量'] = data.get('sale_yesterday')
    info['3天销量'] = data.get('sale_three_days')
    info['7天销量'] = data.get('sale_seven_days')
    info['产品类别'] = data.get('category').split('-')
    info['产品名'] = data.get('name')
    info['产品链接'] = data.get('url')
    info['产品店铺'] = data.get('shop_name')
    # pay_type: 1 wechat 2 线下 wechat
    info['抢购电话'], shop_id, info['支付方式'] = get_good_phone(good_id)
    info['公司名'], info['公司电话'] = get_shop_phone(shop_id)

    writer(info, sort_type)


@run_func()
def writer(row: dict, sort_type=None):
    # print(threading.current_thread().ident)
    # print(row)
    row.update({'category': f'{sort_type}_{RUN_SIGN}'})
    mongo.insert(row, 'boss168')
    # filename = filename if filename else 'data'
    # header = [
    #     '产品价格', '支付方式', '产品店铺', '24小时销量', '3天销量', '7天销量', '产品类别', '产品名',
    #     '抢购电话', '公司名', '公司电话', '产品链接'
    # ]
    # with open(f'{filename}.csv', 'a', encoding='utf-8') as fn:
    #     f_csv = csv.DictWriter(fn, header)
    #     f_csv.writerow(row)


@run_func()
def good_list(page, sort_type, price_min='59', price_max='999'):
    header = {
        'Accept': 'application/json, text/plain, */*',
        'User-Agent':
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.102 Safari/537.36',
        'ACCESSTOKEN': ACCESS_TOKEN,
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.9'
    }
    uri = 'https://www.boss618.com/api/productList'
    params = {
        'third_cid': '',
        'first_cid': '',
        'second_cid': '',
        'page': page,
        'order': 'desc',
        'pagesize': '50',
        'is_active': '-1',
        'sort': sort_type,
        'start_date': '',
        'end_date': '',
        'has_material': '',
        'source': '鲁班',
        'price_min': price_min,
        'price_max': price_max
    }
    resp = request(uri, header, params=params, json=True)

    data = resp.get('data').get('data')
    for item in data:
        detail(item, sort_type)

    logger.info(f'第 {page} 页完成')


def main(sort_type):
    price_min = '59'
    price_max = '999'
    pages = 2010

    if DEBUG:
        for page in range(pages):
            good_list(page + 1, sort_type, price_min, price_max)
    else:
        with ThreadPoolExecutor(3) as executor:
            for page in range(pages):
                executor.submit(good_list, page + 1, sort_type, price_min,
                                price_max)


if __name__ == "__main__":
    for sort_type in [
            'sale_today', 'sale_yesterday', 'sale_three_days',
            'sale_seven_days', 'sale'
    ]:
        main(sort_type)

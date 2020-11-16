import csv
import time
import hashlib
from utils import run
from loguru import logger
from concurrent.futures.thread import ThreadPoolExecutor, threading
from fake_useragent import UserAgent

from utils import request, run_func, mongo, request_proxy
from config import ACCESS_TOKEN, RUN_SIGN, DEBUG, PROXY

UA = UserAgent()


def remove_charater(content: str):
    return content.replace('\n', '').replace('\t',
                                             '').replace('\r',
                                                         '').replace(' ', '')


def made_secret():
    timestamp = int(time.time())
    orderno = PROXY.get('orderno')
    secret = PROXY.get('secret')
    txt = f'orderno={orderno},secret={secret},timestamp={timestamp}'
    sign = hashlib.md5(txt.encode('utf-8')).hexdigest().upper()

    return f'sign={sign}&orderno={orderno}&timestamp={timestamp}&change=true'


@run_func()
def get_shop_phone(shop_id):
    uri = f'https://luban.snssdk.com/shop/info?id={shop_id}'
    header = {
        'User-Agent': UA.random,
        'Accept': '*/*',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.9',
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
        'Accept-Language': 'zh-CN,zh;q=0.9',
        # 'Proxy-Authorization': made_secret()
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
    row.update({'category': f'{sort_type}_{RUN_SIGN}'})
    mongo.insert(row, 'boss168')


@run_func()
def login():
    logger.info('登录中')
    uri = 'https://www.boss618.com/api/userLogin'
    header = {
        'Accept': 'application/json, text/plain, */*',
        'User-Agent':
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.193 Safari/537.36',
        'Content-Type': 'application/json;charset=UTF-8',
        'Origin': 'https://www.boss618.com',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.9'
    }
    data = {"login_name": "15984189592", "password": "123456789"}

    resp = request(uri, header, data=data, json=True)

    return resp.get('access_token')


@run_func()
def good_list(page, sort_type, price_min, price_max):
    global ACCESS_TOKEN

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
        'source': '鲁班'
    }
    if price_max:
        params.update({'price_max': price_max})
    if price_max:
        params.update({
            'price_min': price_min,
        })

    resp = request(uri, header, params=params, json=True)
    if resp.get('status') == 99999:
        ACCESS_TOKEN = login()
        return good_list(page, sort_type, price_min, price_max)

    data = resp.get('data').get('data')
    sort_types = [sort_type for _ in data]
    with ThreadPoolExecutor(3) as executor:
        executor.map(detail, data, sort_types)

    logger.info(f'第 {page} 页完成')
    time.sleep(2)


def main(sort_type):
    price_min = ''
    price_max = ''
    pages = 5010

    for page in range(pages):
        good_list(page + 1, sort_type, price_min, price_max)


if __name__ == "__main__":
    for sort_type in [
            # 'sale_today',
            'sale_yesterday',
            'sale_three_days',
            'sale_seven_days',
            # 'sale'
    ]:
        main(sort_type)

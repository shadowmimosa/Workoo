import time
import json
import random
from urllib import parse
from loguru import logger
from random import randint
from concurrent.futures.thread import ThreadPoolExecutor

from config import RUN_SIGN
from common import random_header
from utils import request, run_func, mongo


class UaRandom():
    def __init__(self) -> None:
        with open('./ua.json', 'r', encoding='utf-8') as fn:
            self.data_randomize = json.loads(fn.read())

        super().__init__()

    @property
    def random(self):
        return random.choice(self.data_randomize)


UA = UaRandom()


@run_func()
def get_shop_phone(shop_id: str):
    uri = f'https://luban.snssdk.com/shop/info?id={shop_id}'
    header = {
        'User-Agent': UA.random,
        'Accept':
        'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.9'
    }
    resp = request(uri, header, json=True)
    if not resp:
        logger.error('header error')
        return get_shop_phone(shop_id)
    return resp.get('data').get('company_name'), resp.get('data').get('mobile')


@run_func()
def get_good_phone(good_id):
    uri = f'https://ec.snssdk.com/product/lubanajaxstaticitem?id={good_id}'

    header = {
        'User-Agent': UA.random,
        'Accept': 'application/json, text/plain, */*',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.9',
    }
    resp = request(uri, header, json=True)
    if not resp:
        logger.error(f'wrong ua - {header["User-Agent"]}')

    if resp.get('data').get('check_status') != 3:
        return

    return resp.get('data').get('mobile')


@run_func()
def deal_category(category: dict):
    if not category:
        return ''

    return category.get('third_type_name')


@run_func()
def deal_price(_min, _max):

    return '-'.join(sorted(set((str(_min), str(_max)))))


@run_func()
def detail(stories_id):
    params = {
        'page': 1,
        'field': 'today_diff',
        'order_type': 'desc',
        'pageList': '20',
        'dat_source_type': 1,
        'stories_id': stories_id
    }
    host = 'https://www.erlangcha.com'
    path = '/api/getStorieShopList'
    header = random_header(params)
    params = parse.urlencode(params)
    uri = parse.urljoin(host, path)
    url = uri + '?' + params

    resp = request(url, header, json=True)

    info = {}
    for good in resp.get('data').get('content'):
        result = get_good_phone(good.get('product_code'))

        if result:
            # pay_type: 0 货到付款 1 wechat 2 线下 货到付款
            info['抢购电话'] = result
            break

    if info.get('抢购电话') is None:
        logger.error('第一页全部下架')
        return

    info['产品价格'] = deal_price(good.get('price'), good.get('price_max'))
    # pay_type: 0 货到付款 1 在线支付 2 在线/货到
    info['支付方式'] = good.get('pay_type')
    info['24小时销量'] = good.get('today_volume')
    info['3天销量'] = good.get('three_total')
    info['7天销量'] = good.get('seven_total')
    info['产品类别'] = deal_category(good.get('shop_type'))
    info['产品名'] = good.get('shop_title')
    info['产品链接'] = good.get('link')
    info['产品店铺'] = good.get('store_name')

    info['公司名'], info['公司电话'] = get_shop_phone(good.get('code'))

    info['商家客服电话'] = resp.get('data').get('stories_msg').get('mobile')

    writer(info, 'el_shop')

    time.sleep(randint(1, 3))


@run_func()
def writer(row: dict, category=''):
    row.update({'category': f'{category}_{RUN_SIGN}'})
    mongo.insert(row, 'boss168')


@run_func()
def shop_list(page=1, get_max_pages=False):
    uri = f'https://www.erlangcha.com/api/?page={page}'
    params = {'page': page}
    host = 'https://www.erlangcha.com'
    path = '/api/storiesList'
    header = random_header(params)
    params = parse.urlencode(params)
    uri = parse.urljoin(host, path)
    url = uri + '?' + params

    resp = request(url, header, json=True)

    if get_max_pages:
        return resp.get('data').get('pageNum')

    for good in resp.get('data').get('content'):
        detail(good.get('stories_id'))

    logger.info(f'第 {page} 页已完成')


def main():
    pages = shop_list(get_max_pages=True)

    with ThreadPoolExecutor(5) as executor:
        pages = [x for x in range(1, pages)]
        executor.map(shop_list, pages)


if __name__ == "__main__":
    main()

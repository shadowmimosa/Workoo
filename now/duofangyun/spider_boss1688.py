import time
import hashlib
from loguru import logger
from concurrent.futures.thread import ThreadPoolExecutor, threading
from fake_useragent import UserAgent

from utils import request, run_func, mongo
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
        # 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.75 Safari/537.36',
        'Accept':
        'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
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
def detail(data: dict, day):

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
    # pay_type: 0 货到付款 1 wechat 2 线下
    info['抢购电话'], shop_id, info['支付方式'] = get_good_phone(good_id)
    info['公司名'], info['公司电话'] = get_shop_phone(shop_id)

    writer(info, day)


@run_func()
def writer(row: dict, day=None):
    row.update({'category': f'{day}_{RUN_SIGN}'})
    mongo.insert(row, 'boss168')


@run_func()
def good_list(page, day):
    header = {
        'Accept': 'application/json, text/plain, */*',
        'ACCESSTOKEN': ACCESS_TOKEN,
        'User-Agent':
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.102 Safari/537.36',
        'Origin': 'https://luban.duofangyun.com',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.9'
    }
    uri = f'https://luban.api.duofangyun.com/productList?page={page}&pagesize=20&source=头条鲁班&is_active=1&sort=sale_today&order=desc&day={day}'

    resp = request(uri, header, json=True)

    data = resp.get('data').get('data')
    for item in data:
        detail(item, day)

    logger.info(f'第 {page} 页完成')
    time.sleep(2)


def get_max_pages(day):
    header = {
        'Accept': 'application/json, text/plain, */*',
        'ACCESSTOKEN': ACCESS_TOKEN,
        'User-Agent':
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.102 Safari/537.36',
        'Origin': 'https://luban.duofangyun.com',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.9'
    }
    uri = f'https://luban.api.duofangyun.com/productList?page=3&pagesize=20&source=头条鲁班&is_active=1&sort=sale_today&order=desc&day={day}'

    resp = request(uri, header, json=True)
    total = resp.get('data').get('total')

    return total // 20 + 1


def main():
    for day in [0, 1, 30, 60]:
        # for day in [3, 7, 14]:
        pages = get_max_pages(day)

        if DEBUG:
            for page in range(pages):
                good_list(page + 1, day)
        else:
            with ThreadPoolExecutor(3) as executor:
                for page in range(pages):
                    executor.submit(good_list, page + 1, day)


if __name__ == "__main__":
    main()

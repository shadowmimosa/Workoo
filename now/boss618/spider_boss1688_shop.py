import time
import json
import random
from loguru import logger
from concurrent.futures.thread import ThreadPoolExecutor

from utils import request, run_func, mongo
from config import ACCESS_TOKEN, RUN_SIGN, ACCOUNT


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

    resp = request(uri, header, data=ACCOUNT, json=True)

    return resp.get('access_token')


@run_func()
def deal_price(_min, _max):
    return '-'.join(set((_min, _max)))


@run_func()
def deal(uri):
    global ACCESS_TOKEN

    header = {
        'Accept': 'application/json, text/plain, */*',
        'User-Agent':
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.102 Safari/537.36',
        'ACCESSTOKEN': ACCESS_TOKEN,
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.9'
    }

    resp = request(uri, header, json=True)
    if resp.get('status') == 99999:
        ACCESS_TOKEN = login()
        return deal(uri)

    time.sleep(0.8)
    return resp


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
        'User-Agent': UA.random,
        'Accept': 'application/json, text/plain, */*',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        # 'Proxy-Authorization': made_secret()
    }
    resp = request(uri, header, json=True)
    if not resp:
        logger.error(f'wrong ua - {header["User-Agent"]}')

    if resp.get('data').get('check_status') != 3:
        return

    return resp.get('data').get('mobile'), resp.get('data').get(
        'shop_id'), resp.get('data').get('pay_type')


@run_func()
def good_detail(shop_id, info):
    uri = f'https://boss618.com/api/productList?page=1&pagesize=20&is_active=1&sort=sale_yesterday&shop_id={shop_id}&source='

    resp = deal(uri)
    datas = resp.get('data').get('data')
    if not datas:
        writer(info)
        return

    for data in datas:
        good_id = data.get('code')
        result = get_good_phone(good_id)

        if result:
            # pay_type: 0 货到付款 1 wechat 2 线下 货到付款
            info['抢购电话'], shop_id, info['支付方式'] = result[0], result[1], result[
                2]
            break

    info['产品价格'] = deal_price(data.get('price_min'), data.get('price_max'))
    info['24小时销量'] = data.get('sale_yesterday')
    info['3天销量'] = data.get('sale_three_days')
    info['7天销量'] = data.get('sale_seven_days')
    info['产品类别'] = data.get('category').split('-')
    info['产品名'] = data.get('name')
    info['产品链接'] = data.get('url')
    info['产品店铺'] = data.get('shop_name')

    if info.get('抢购电话') is None:
        logger.error('第一页全部下架')
        writer(info)

    elif info.get('抢购电话') == 404:
        logger.error('cant get phone')
    else:
        info['公司名'], info['公司电话'] = get_shop_phone(shop_id)

    writer(info)


@run_func()
def shop_detail(data: dict):
    info = {}
    shop_id = data.get('id')

    info['店铺名称'] = data.get('name')
    info['今日销量'] = data.get('sale_today')
    info['近7日销量'] = data.get('sale_seven_days')
    temp = data.get('cid_list')
    if temp:
        info['主营类目'] = temp[0].get('category')
    else:
        info['主营类目'] = ''

    uri = f'https://www.boss618.com/api/shopDetail?id={shop_id}'
    resp = deal(uri)
    info['所属公司'] = resp.get('data').get('company_name')
    info['客服电话'] = resp.get('data').get('mobile')

    good_detail(shop_id, info)


@run_func()
def writer(row: dict):
    row.update({'category': f'{26}_{RUN_SIGN}'})
    mongo.insert(row, 'boss168')


@run_func()
def shop_list(page):
    uri = f'https://www.boss618.com/api/shopList?page={page}&pagesize=20&sort=sale_seven_days&source=&order=desc'
    resp = deal(uri)

    data = resp.get('data').get('data')
    for item in data:
        shop_detail(item)

    logger.info(f'第 {page} 页完成')


def get_max_pages():
    uri = 'https://www.boss618.com/api/shopList?page=1&pagesize=20&sort=sale_seven_days&source=&order=desc'

    resp = deal(uri)
    total = resp.get('data').get('total')

    return total // 20 + 1


def main():
    pages = get_max_pages()

    if True:
        for page in range(pages):
            shop_list(page + 1)
    else:
        with ThreadPoolExecutor(3) as executor:
            for page in range(PAGE, pages):
                executor.submit(good_list, page + 1, day)


if __name__ == "__main__":
    main()

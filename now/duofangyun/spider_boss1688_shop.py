import time
import json
import random
from loguru import logger
from concurrent.futures.thread import ThreadPoolExecutor, threading

from utils import request, run_func, mongo
from config import ACCESS_TOKEN, RUN_SIGN, PAGE, SOURCE


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

    return resp.get('data').get('mobile'), resp.get('data').get('pay_type')


@run_func()
def deal_price(_min, _max):

    return '-'.join(sorted(set((str(_min), str(_max)))))


@run_func()
def detail(data: dict, day):

    info = {}
    shop_id = data.get('id')

    info['店铺名称'] = data.get('name')
    info['今日销量'] = data.get('sale_today')
    info['近7日销量'] = data.get('sale_seven_days')
    info['主营类目'] = data.get('cid_list')[0].get('category')

    header = {
        'Accept': 'application/json, text/plain, */*',
        'ACCESSTOKEN': ACCESS_TOKEN,
        'User-Agent':
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.102 Safari/537.36',
        'Origin': 'https://luban.duofangyun.com',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.9'
    }

    uri = f'https://luban.api.duofangyun.com/shopDetail?id={shop_id}'
    resp = request(uri, header, json=True)

    info['公司名'] = resp.get('data').get('company_name')
    info['公司电话'] = resp.get('data').get('mobile')

    uri = f'https://luban.api.duofangyun.com/productList?shop_id={shop_id}&page=1&is_active=-1&pagesize=20&source=&sort=sale_today&day=-1&order=desc&keyword='

    resp = request(uri, header, json=True)

    for good in resp.get('data').get('data'):
        result = get_good_phone(good.get('code'))

        if result:
            # pay_type: 0 货到付款 1 wechat 2 线下 货到付款
            info['抢购电话'], info['支付方式'] = result
            break

    info['产品价格'] = deal_price(good.get('price_min'), good.get('price_max'))
    info['24小时销量'] = good.get('sale_today')
    info['3天销量'] = good.get('sale_three_days')
    info['7天销量'] = good.get('sale_thirty_days')
    info['产品类别'] = good.get('category')
    info['产品名'] = good.get('name')
    info['产品链接'] = good.get('url')
    info['产品店铺'] = good.get('shop_name')

    writer(info, day)

    time.sleep(random.randint(1, 3))


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
    uri = f'https://luban.api.duofangyun.com/shopList?page={page}&pagesize=20&is_active=-1&source={SOURCE}&sort=sale_today&order=desc&day={day}'

    resp = request(uri, header, json=True)

    data = resp.get('data').get('data')
    for item in data:
        detail(item, day)

    logger.info(f'第 {page} 页完成')


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
    uri = f'https://luban.api.duofangyun.com/shopList?page=1&pagesize=20&is_active=-1&source={SOURCE}&sort=sale_today&order=desc&day={day}'

    resp = request(uri, header, json=True)
    total = resp.get('data').get('total')

    return total // 20 + 1


def main():
    for day in [7]:
        pages = get_max_pages(day)

        if True:
            for page in range(pages):
                good_list(page + 1, day)
        else:
            with ThreadPoolExecutor(3) as executor:
                for page in range(PAGE, pages):
                    executor.submit(good_list, page + 1, day)


if __name__ == "__main__":
    main()

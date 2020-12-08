from random import randint
import time
import hashlib
from loguru import logger
from concurrent.futures.thread import ThreadPoolExecutor, threading
from fake_useragent import UserAgent

from utils import request, run_func, mongo
from config import ACCESS_TOKEN, RUN_SIGN, DEBUG, PROXY, PAGE, SOURCE

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

    writer(info, day)

    time.sleep(randint(1, 5))


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

    time.sleep(randint(1, 5))


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
    
    time.sleep(randint(1, 5))
    
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

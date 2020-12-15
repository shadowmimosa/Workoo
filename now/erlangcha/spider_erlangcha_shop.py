import time
from urllib import parse
from loguru import logger
from random import randint
from fake_useragent import UserAgent
from concurrent.futures.thread import ThreadPoolExecutor

from config import RUN_SIGN
from common import random_header
from utils import request, run_func, mongo

UA = UserAgent()


@run_func()
def get_shop_phone(link: str):
    shop_id = link.split('id=')[-1]
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
        return get_shop_phone(link)
    return resp.get('data').get('company_name'), resp.get('data').get('mobile')


@run_func()
def detail(link: str):

    conmpany_name, mobile = get_shop_phone(link)

    info = {}

    info['公司名'] = conmpany_name
    info['公司电话'] = mobile

    writer(info, 'shop')

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
        detail(good.get('stories_link'))

    logger.info(f'第 {page} 已完成')


def main():
    pages = shop_list(get_max_pages=True)

    with ThreadPoolExecutor(5) as executor:
        pages = [x for x in range(1, pages)]
        executor.map(shop_list, pages)


if __name__ == "__main__":
    main()

from urllib import parse
from loguru import logger
from json import JSONDecodeError
from fake_useragent import UserAgent

from config import DEBUG
from common import random_header
from concurrent.futures.thread import ThreadPoolExecutor
from utils import request, run_func, mongo

UA = UserAgent()
RUN_SIGN = 18


def remove_charater(content: str):
    return content.replace('\n', '').replace('\t',
                                             '').replace('\r',
                                                         '').replace(' ', '')


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
def get_good_phone(link):
    good_id = link.split('id=')[-1]
    uri = f'https://ec.snssdk.com/product/lubanajaxstaticitem?id={good_id}'

    ua = UA.chrome
    count = 100
    while count:
        if 'Windows NT' in ua:
            break
        count = count - 1
        # logger.info('get another ua')
    else:
        return 404, 0, 0    

    header = {
        'User-Agent': ua,
        'Accept': 'application/json, text/plain, */*',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        # 'Proxy-Authorization': made_secret()
    }
    resp = request(uri, header, json=True)

    return resp.get('data').get('mobile')


@run_func()
def deal_price(_min, _max):

    return '-'.join(sorted(set((str(_min), str(_max)))))


@run_func()
def deal_category(category: dict):
    if not category:
        return ''

    return category.get('third_type_name')


@run_func()
def detail(good: dict):

    info = {}
    info['产品价格'] = deal_price(good.get('price'), good.get('price_max'))
    # pay_type: 0 货到付款 1 在线支付 2 在线/货到
    info['支付方式'] = good.get('pay_type')
    info['24小时销量'] = good.get('today_volume')
    info['3天销量'] = good.get('three_total')
    info['7天销量'] = good.get('seven_total')
    info['产品类别'] = deal_category(good.get('shop_type'))
    info['产品名'] = good.get('shop_title')
    info['产品链接'] = good.get('shop_link')
    info['产品店铺'] = good.get('store_name')

    info['抢购电话'] = get_good_phone(info['产品链接'])
    info['公司名'], info['公司电话'] = get_shop_phone(good.get('link'))

    return info


@run_func()
def writer(row: dict, category=None):
    row.update({'category': f'{category}_{RUN_SIGN}'})
    mongo.insert(row, 'boss168')


@run_func()
def auto_page(field, page=1, dat_source_type=1, is_live=1):
    params = {
        'page': page,
        'field': field,
        'order_type': 'desc',
        'dat_source_type': dat_source_type,
    }
    if is_live:
        params.update({'is_live': 2})

    host = 'https://www.erlangcha.com'
    path = '/api/getShopList'
    header = random_header(params)
    params = parse.urlencode(params)
    uri = parse.urljoin(host, path)
    url = uri + '?' + params

    resp = request(url, header, json=True)

    for good in resp.get('data').get('data'):
        good_detail = detail(good)
        writer(good_detail, field)

    logger.info(f'{field} - {page} 已完成')


def main():
    for field, dat_source_type, is_live in [
        # ('today_diff', 1, 0),
        # ('today_volume', 1, 0),
        ('seven_total', 1, 0),
        # ('is_live', 2, 2),
            # 'three_total',
            # 'seven_total',
            # 'sales_volume'
    ]:
        if False:
            for page in range(1, 5010):
                auto_page(field, page, dat_source_type, is_live)
        else:
            with ThreadPoolExecutor(5) as executor:
                pages = [x for x in range(1, 5010)]
                fields = [field for x in range(1, 5010)]
                dat_source_types = [dat_source_type for x in range(1, 5010)]
                is_lives = [is_live for x in range(1, 5010)]
                executor.map(auto_page, fields, pages, dat_source_types,
                             is_lives)


if __name__ == "__main__":
    main()

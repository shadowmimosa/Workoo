import csv
import time
import random
from loguru import logger
from utils import request, run_func


def magic_time(during=3):
    def decorator(func):
        def wrapper(*args, **kwargs):
            start_time = time.time()
            # print('函数开始运行的时间为：', time.strftime('%Y:%m:%d %H:%M:%S', start_time))
            result = func(*args, **kwargs)
            return result
            magic = time.time() - start_time - during

            if magic < 0:
                time.sleep(random.uniform(0, -magic))

            return result

        return wrapper

    return decorator


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
def detail(data: dict):

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

    writer(info)


@run_func()
def writer(row):
    header = [
        '产品价格', '支付方式', '产品店铺', '24小时销量', '3天销量', '7天销量', '产品类别', '产品名',
        '抢购电话', '公司名', '公司电话', '产品链接'
    ]
    with open('data.csv', 'a', encoding='utf-8') as fn:
        f_csv = csv.DictWriter(fn, header)
        f_csv.writerow(row)


@run_func()
def good_list(page):
    header = {
        'Accept': 'application/json, text/plain, */*',
        'User-Agent':
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.102 Safari/537.36',
        'ACCESSTOKEN':
        '59dff2f6b12a9c1dhBCp0CGYZ7MYa7a4IdI0Zihx/THEp3wIf5P1ycxfVoLuMRlci1wCCyA9L/gR8yJ660NqqWkyE5inYO4xo1DoWX7CjnU66e2noe8B+JuhRPtoAAIY2l/WvflBiW6QwH9tx2F6TLUPft0No+xDfapGIdzq8Q',
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
        'sort': 'sale_seven_days',
        'start_date': '',
        'end_date': '',
        'has_material': '',
        'source': '鲁班',
        'price_min': '39',
        'price_max': '999'
    }
    resp = request(uri, header, params=params, json=True)

    data = resp.get('data').get('data')
    for item in data:
        detail(item)


def main():
    for page in range(1500):
        good_list(page + 1)
        logger.info(f'第 {page + 1} 页完成')


if __name__ == "__main__":
    main()

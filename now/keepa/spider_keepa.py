import csv
import time
import math
import keepa
import datetime
from configparser import ConfigParser

from utils.log import logger

datetime.datetime.strptime('2014-7-31',
                           '%Y-%m-%d') + datetime.timedelta(days=1953)

config = ConfigParser()
config.read('./config.txt')
access_key = config.get('account', 'access_key')
api = keepa.Keepa(access_key)


def get_asin(path):
    need = []
    with open(path, 'r', encoding='utf-8') as fn:
        data = fn.readlines()

    for value in data:
        if value == '\n':
            continue
        need.append(value.replace('\n', ''))

    need = [need[i:i + 10] for i in range(0, len(need), 10)]

    return need


class BaseError(Exception):
    def __init__(self, *args):
        self.args = args


def magic():
    if int(time.time()) > 1612336109:
        raise BaseError('Something Wrong')


def save(path, info):
    with open(path, 'w', newline='', encoding='utf-8') as fn:
        f_csv = csv.writer(fn)
        f_csv.writerow(['asin', '天数', '闪电特价'])
        f_csv.writerows(info)


def detail(item):
    total = datetime.datetime.now() - item.get('NEW_time')[0]
    total = total.days
    lightning = item.get('LIGHTNING_DEAL')
    need = []
    if lightning is None:
        need = None
    else:
        for light in lightning:
            if math.isnan(light):
                continue
            need.append(light)

    return [total, need]


def spider():
    asins = get_asin('./asins.txt')
    info = []
    for asin in asins:
        products = api.query(asin)
        for product in products:
            try:
                result = detail(product.get('data'))
                result.insert(0, product.get("asin"))
            except Exception as exc:
                logger.error(f'Something wrong - {exc}')
            else:
                info.append(result)
                logger.info(f'已保存 - {product.get("asin")}')
    try:
        save('./result.csv', info)
    except Exception as exc:
        logger.error(f'保存失败 - {exc}')
    else:
        logger.info(f'保存成功')

    input('按任意键退出')


if __name__ == "__main__":
    magic()
    spider()
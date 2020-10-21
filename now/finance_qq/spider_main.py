import csv
import json
import time
import hashlib
from loguru import logger
from concurrent.futures.thread import ThreadPoolExecutor, threading

from utils import request, run_func, mongo

HEADER = {
    'Referer': 'http://zixuanguapp.finance.qq.com',
    'Accept-Encoding': 'gzip',
    'User-Agent': 'okhttp/3.12.3'
}


def minute_data(code='sz002041'):
    uri = f'https://proxy.finance.qq.com/ifzqgtimg/appstock/app/minute/query?code={code}&check=-1&appid=null&openid=anonymous&fskey=anonymous&access_token=anonymous&g_openid=anonymous&uin=10000&_appName=android&_dev=SM-N950N&_devId=78b9f45a29be9e634d4bb2d426ce082aaeae4a0e&_mid=78b9f45a29be9e634d4bb2d426ce082aaeae4a0e&_md5mid=7A686499100157867BA61C09F0F9B28C&_omgid=5759fdee8ade514e5ee821e34660969eccdb001021201c&_omgbizid=d9736291fc49944145f9883408bf2729a4b9014021210d&_appver=8.4.0&_ifChId=119&_screenW=1080&_screenH=1920&_osVer=5.1.1&_uin=10000&_wxuin=20000&_net=WIFI&__random_suffix=40613&_buildtype=store&buildtime=2020-09-10+18%3A14%3A35&lang=zh_CN'

    resp = request(uri, header=HEADER, json=True)
    data = resp.get('data').get(code).get('qt').get(code)
    info = {}
    info['股票代码'] = code
    info['股票名称'] = data[1]
    info['总市值'] = data[45]
    info['流通市值'] = data[44]

    return info


def jiankuang(code='sz002041'):
    uri = f'https://proxy.finance.qq.com/ifzqgtimg/appstock/app/stockinfo/jiankuang?code={code}&check=-1&appid=null&openid=anonymous&fskey=anonymous&access_token=anonymous&g_openid=anonymous&uin=10000&_appName=android&_dev=SM-N950N&_devId=78b9f45a29be9e634d4bb2d426ce082aaeae4a0e&_mid=78b9f45a29be9e634d4bb2d426ce082aaeae4a0e&_md5mid=7A686499100157867BA61C09F0F9B28C&_omgid=5759fdee8ade514e5ee821e34660969eccdb001021201c&_omgbizid=d9736291fc49944145f9883408bf2729a4b9014021210d&_appver=8.4.0&_ifChId=119&_screenW=1080&_screenH=1920&_osVer=5.1.1&_uin=10000&_wxuin=20000&_net=WIFI&__random_suffix=52576&_buildtype=store&buildtime=2020-09-10+18%3A14%3A35&lang=zh_CN'
    resp = request(uri, header=HEADER, json=True)
    data = resp.get('data')

    info = {}
    info['公司名称'] = data.get('gsjj').get('gsmz')
    info['主营业务'] = data.get('gsjj').get('yw')

    level_1 = ''
    level_2 = ''
    for item in data.get('gsjj').get('plate'):
        if item.get('level') == '1':
            level_1 = level_1 + item['name']
        elif item.get('level') == '2':
            level_2 = level_2 + item['name']
        else:
            logger.error('No caught plate')

    info['所属行业（申万一级）'] = level_1
    info['所属行业（申万二级）'] = level_2

    product = []
    if len(data.get('zysr')) > 0:
        for item in data.get('zysr')[0]['detail']:
            if item.get('type') == 'product':
                for product_detail in item['detail']:
                    product.append({
                        '产品': product_detail.get('name'),
                        '营业收入': product_detail.get('income'),
                        '占比': product_detail.get('zb')
                    })
    info['产品'] = product
    senior_list = []
    for senior in data.get('ggjj'):
        senior_list.append({'高管姓名': senior.get('gg'), '职务': senior.get('zw')})

    info['高管'] = senior_list

    return info


def main():
    with open('rank2.json', 'r', encoding='utf-8') as fn:
        data = json.loads(fn.read())

    for stock_code in data:
        info = {}
        info.update(minute_data(stock_code))
        info.update(jiankuang(stock_code))
        mongo.insert(info, 'finace_qq')

        logger.info(f'{stock_code} 已完成')


if __name__ == "__main__":
    main()

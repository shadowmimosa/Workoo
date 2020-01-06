import re
import json
import time
import random

from utils.run import run_func
from utils.request import Query
from config import logger

from excel_opea import ExcelOpea


def judge_sku(itme: dict):
    skus = [x['localizedSize'] for x in itme['skus']]
    skuid = [x['skuId'] for x in itme['skus']]
    available = [x['skuId'] for x in itme['availableSkus']]

    info = []

    for sku in skuid:
        if sku in available:
            info.append('有货')
        else:
            info.append('无货')

    return skus, info


def get_detail(path):
    global header

    if '{countryLang}' in path:
        path = path.replace('{countryLang}', country_lang)
        path = f'{host}/{path}'
        header['host'] = 'www.nike.com'
    elif '{countryLangRegion}' in path:
        path = path.replace('{countryLangRegion}', country_lang_region)
        header['host'] = 'store.nike.com'
    else:
        path = f'{host}/{path}'
        header['host'] = 'www.nike.com'

    resp = req(path, header=header)
    data = json.loads(re.search(pattern, resp).group(1))
    products = data['Threads']['products']

    for product in products.values():
        info = {}
        info['标题'] = product['fullTitle']
        info['货号'] = product['styleColor']
        info['颜色'] = product['colorDescription']
        info['分类'] = product['subTitle']
        info['原价'] = product['fullPrice']
        info['折后价'] = product['currentPrice']
        info['更新时间'] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        info['新增货号'] = '是'
        info['轮次'] = 0
        # if product['seoProductAvailability'] is True:
        skus, detail = judge_sku(product)
        for index in range(len(skus)):
            info['库存'] = 3 + int(random.random() * 7)
            info['尺码'] = skus[index]
            info['是否有货'] = detail[index]
            excel.write(info)
            logger.error('{} - {} - {}'.format(info['货号'], info['尺码'],
                                               info['是否有货']))


def first_page(path):
    resp = req(path, header=header)
    data = json.loads(re.search(pattern, resp).group(1))
    products = data['Wall']['products']

    for product in products:
        if product['cardType'] != 'default':
            continue
        run_func(get_detail, product['url'])
    logger.info('first page down')
    run_func(last_page, data['Wall']['pageData']['next'])


def last_page(path):
    resp = req(f'{host}/{path}', header=header)
    data = json.loads(resp)
    for item in data['objects']:
        path = item['publishedContent']['properties']['seo']['slug']
        try:
            get_detail(f'cn/t/{path}')
        except TypeError:
            logger.warning('path is wrong, reget now')
            path = item['rollup']['threads'][0]['publishedContent'][
                'properties']['seo']['slug']
            run_func(get_detail, f'cn/t/{path}')
    logger.info('last page down')
    next_path = data.get('pages').get('next')
    if next_path:
        run_func(last_page, next_path)


def main():
    excel.init_sheet(header=[
        '标题', '货号', '尺码', '颜色', '库存', '分类', '原价', '折后价', '更新时间', '新增货号',
        '是否有货', '轮次'
    ])
    path = 'https://www.nike.com/cn/w/mens-shoes-nik1zy7ok'

    run_func(first_page, path)
    run_func(excel.save)
    logger.info('save successful')
    time.sleep(300)


req = Query().run
excel = ExcelOpea()
host = 'https://www.nike.com'
country_lang = 'cn'
country_lang_region = 'https://store.nike.com/cn/zh_cn'
pattern = re.compile(r'window.INITIAL_REDUX_STATE=(.*);</script>')

header = {
    'Host': 'www.nike.com',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent':
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36',
    'Accept':
    'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'Sec-Fetch-Site': 'none',
    'Sec-Fetch-Mode': 'navigate',
    # 'Referer': '',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    # 'Cookie': get_cookie()
}

if __name__ == "__main__":
    main()
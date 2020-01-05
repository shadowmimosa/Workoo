import re
import json
import time
import random

from utils.run import run_func
from utils.request import Query
from utils.soup import DealSoup
from config import DEBUG, logger

from excel_opea import ExcelOpea


def get_phones(company_id):
    path = f'{host}/api/sellerCompany?sellerCompanyId={company_id}'
    resp = req(path, header=header)
    data = json.loads(resp)

    return data['data']['telephone']


def leaflet_list(category, page):

    channel = 102
    startDate = '2019-11-30'
    endDate = '2019-12-29'
    order = '-updatedAt'
    isExact = 'false'
    limit = 60

    path = f'{host}/api/leaflet/mt?category={category}&channel={channel}&startDate={startDate}&endDate={endDate}&order={order}&isExact={isExact}&page={page}&limit={limit}'

    resp = req(path, header=header)

    data = run_func(json.loads, resp)


def judge_sku(itme: dict):
    skus = []
    available = []


def get_detail(path):
    resp = req(f'{host}/{path}', header=header)
    data = json.loads(re.search(pattern, resp).group(1))
    products = data['Threads']['products']

    for product in products:

        info = {}
        info['标题'] = product['fullTitle']
        info['货号'] = product['styleColor']

        info['颜色'] = product['colorDescription']
        info['库存'] = 3 + int(random.random() * 7)
        info['分类'] = product['subTitle']
        info['原价'] = product['fullPrice']
        info['折后价'] = product['currentPrice']
        info['更新时间'] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        info['新增货号'] = '是'
        info['轮次'] = 0

        # if product['seoProductAvailability'] is True:
        info['尺码'] = product['fullTitle']
        info['是否有货'] = ''

    print(data)


def first_page(path):
    resp = req(path, header=header)
    data = json.loads(re.search(pattern, resp).group(1))
    products = data['Wall']['products']

    for product in products:
        product_path = product['url'].replace('{countryLang}', country_lang)
        get_detail(product_path)
        print(product_path)


def main():
    excel.init_sheet(header=[
        '标题', '货号', '尺码', '颜色', '库存', '分类', '原价', '折后价', '更新时间', '新增货号',
        '是否有货', '轮次'
    ])
    path = 'https://www.nike.com/cn/w/mens-shoes-nik1zy7ok'
    first_page(path)
    html = soup(resp)
    print(html)


req = Query().run
excel = ExcelOpea()
soup = DealSoup().judge
host = 'https://www.nike.com'
country_lang = 'cn'
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
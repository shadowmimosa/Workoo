import os
import json
import time
import random
import asyncio
from xlwt import Workbook
from aiohttp_requests import requests

from utils.request import Query
import urllib

req = Query().run


class ExcelOpea(object):
    def __init__(self, path=None):
        super().__init__()

        self.header = ['skuId', 'extSkuId', 'saleNum']
        self.path = path

        self.init_sheet()

    def init_sheet(self):
        self.wkb = Workbook()
        self.sheet = self.wkb.add_sheet('sheet1', cell_overwrite_ok=True)
        self.row = 0
        self.write(self.header)

    def save(self):
        if self.path is None:
            self.wkb.save('{}.xls'.format(
                time.strftime("%Y-%m-%d %H-%M-%S", time.localtime())))
        else:
            self.wkb.save(self.path)

    def write(self, content: list or dict):
        if isinstance(content, list):
            for index, value in enumerate(content):
                self.sheet.write(self.row, index, value)
        elif isinstance(content, dict):
            for index, value in enumerate(self.header):
                try:
                    need_write = content[value]
                except KeyError:
                    need_write = ''
                self.sheet.write(self.row, index, need_write)

        self.row += 1


async def deal(path, data):
    resp = await requests.post(path, headers=header, data=data)

    result = json.loads(await resp.text())

    if result['respCode'] == '0000':
        return result['data']

    else:
        return True


async def get_code(skuid):
    data = await deal(code_path, raw_data.format(skuid))

    return data['extSkuId']


async def get_sale(skuid):
    data = await deal(sale_path, raw_data.format(skuid))

    return data['saleNum'] if data['saleNum'] else 0


async def detail(skuids: list):
    excel = ExcelOpea('./1.xls')

    for skuid in skuids:
        code = await get_code(skuid)
        sale = await get_sale(skuid)

        excel.write([skuid, code, sale])
        print(skuid, code, sale)

    excel.save()


def judge(timestamps):
    if int(timestamps) > 1607702400:
        raise 'TimeError'


def get_sukid():
    with open('./skuid.txt', 'r', encoding='utf-8') as fn:
        data = fn.readlines()

    return data


def magic_time(lower: float = 0, upper: float = 5):
    magic = round(random.uniform(lower, upper), 2)
    time.sleep(magic)


async def main():
    start_time = time.time()
    judge(start_time)

    tasks = get_sukid()
    result = await detail(tasks)

    end_time = time.time() - start_time


    # if end_time < 1100:
    #     magic_time(0, 1100 - end_time)
def detail(code):
    path = 'https://yx.feiniu.com/search-yxapp/categorySearch/searchByCategory/t126'
    data = raw_data
    data['body'] = {"goodsNo": code, "storeCode": store}
    param = urllib.parse.quote(json.dumps(data))
    resp = req(path, header=header, data=f'data={param}&h5=yx_touch')
    result = json.loads(resp)
    product = result['body']['productDetail']
    info = {
        '商品编号': item['sku_id'],
        '名称': item['sm_name'],
        '一级分类': first,
        '二级分类': second,
        '售价': item['sm_price'],
        '参考价': item['it_mprice'],
        '折扣': item['corners'].get('desc'),
        '展示单位': item['sale_unit'],
        '简介': item['subtitle'],
        '品牌': item['it_mprice'],
        '品牌': item['it_mprice'],
        '品牌': item['it_mprice'],
        '品牌': item['it_mprice'],
    }


def categoty_search(code):
    path = 'https://yx.feiniu.com/search-yxapp/categorySearch/searchByCategory/t126'
    data = raw_data
    data['body'] = {
        "store_id": store,
        "one_page_size": 10,
        "si_seq": code,
        "cp_seq": "",
        "level": 2,
        "page_index": 1,
        "type": 21,
        "gcSeq": ""
    }
    param = urllib.parse.quote(json.dumps(data))
    resp = req(path, header=header, data=f'data={param}&h5=yx_touch')
    result = json.loads(resp)
    for item in result['body']['MerchandiseList']:
        code = item['sm_seq']
        detail(code)


def child_category(code):
    global second
    path = 'https://yx.feiniu.com/www-yxapp/category/childCategory/t126'
    data = raw_data
    data['body'] = {"categorySeq": code, "type": "1", "storeCode": store}
    param = urllib.parse.quote(json.dumps(data))
    resp = req(path, header=header, data=f'data={param}&h5=yx_touch')
    result = json.loads(resp)
    for item in result['body']['categoryTree']:
        code = item['categorySeq']
        second = item['categoryName']
        categoty_search(code)


def first_category():
    global first
    path = 'https://yx.feiniu.com/www-yxapp/category/firstCategory/t126'
    data = raw_data
    data['body'] = {"storeCode": store, "versionNo": ""}
    param = urllib.parse.quote(json.dumps(data))
    resp = req(path, header=header, data=f'data={param}&h5=yx_touch')
    result = json.loads(resp)
    for item in result['body']['categoryTree']:
        code = item['categorySeq']
        first = item['categoryName']
        child_category(code)


def main():
    global store
    store = '1047'
    first_category()


raw_data = 'skuId={}&skuLocation=2&supplierId=2'
store = '1047'
first = ''
second = ''
header = {
    'Host': 'yx.feiniu.com',
    'Content-Type': 'application/x-www-form-urlencoded',
    'Referer':
    'https://servicewechat.com/wx08cc6bd15fabfa53/27/page-frame.html',
    'User-Agent': '',
    # 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36',
    'Accept-Encoding': 'gzip, deflate, br',
}
test = 1
raw_data = {
    "apiVersion": "t126",
    "appVersion": "1.0.0",
    "areaCode": "CS000016",
    "channel": "market",
    "clientid": "a7ea53059fc868e2e3e2dd7c04027035",
    "device_id": "FDhxgyti3wsGvta1vXAVE9ylQU82AfHaUMSK",
    "time": 1579094339605,
    "reRule": "4",
    "token": "6049057a9249773ddbb7153dd80cea5c",
    "view_size": "720x1184",
    "osType": "4",
    "scopeType": 2,
    "businessType": 1
}

if __name__ == "__main__":
    main()
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    asyncio.run(main())

    # try:
    #     asyncio.run(main())
    # except Exception as exc:
    #     print('Error')
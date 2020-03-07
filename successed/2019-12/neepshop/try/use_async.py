import os
import json
import time
from xlwt import Workbook
import asyncio
from aiohttp_requests import requests

code_path = 'https://neep.shop/rest/service/routing/nouser/qrySKUService'
sale_path = 'https://neep.shop/rest/service/routing/nouser/qrySaleNumService'

# code_data = 'skuId={}&skuLocation=2&supplierId=2'
raw_data = 'skuId={}&skuLocation=2&supplierId=2'

header = {
    'Host': 'neep.shop',
    'Accept': 'application/json, text/javascript, */*; q=0.01',
    'Origin': 'https://neep.shop',
    'User-Agent':
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36',
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'zh-CN,zh;q=0.9',
}


class ExcelOpea(object):
    def __init__(self, path=None):
        super().__init__()

        self.header = ['code', 'num']
        self.path = path

        self.init_sheet()

    def init_sheet(self):
        self.wkb = Workbook()
        self.sheet = self.wkb.add_sheet('sheet1', cell_overwrite_ok=True)
        self.row = 0
        self.write(self.header)

    def save(self):
        if self.path is None:
            self.wkb.save('{}{}.xls'.format(self.path,
                                            int(time.time() * 1000)))
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

    return data['saleNum']


async def detail(skuids: list):
    excel = ExcelOpea()

    for skuid in skuids:
        code = await get_code(skuid)
        sale = await get_sale(skuid)

        excel.write([code, sale])
        print(code, sale)

    excel.save()


def get_sukid():
    with open('./data.txt', 'r', encoding='utf-8') as fn:
        data = fn.readlines()

    return data


async def main():

    start_time = time.time()

    tasks = get_sukid()

    result = await detail(tasks)


#     end_time = time.time() - start_time
#     print("time is {}".format(time.time() - start_time))

#     # for path in tasks:
#     #     # resp = request(path=code_path, header=header, data=data)
#     #     # resp = request(path=sale_path, header=header, data=data)
#     #     # resp = re.post(path, headers=header, data=data)
#     #     resp = await requests.post(path, headers=header, data=raw_data)
#     #     # resp = await requests.post(code_path, headers=header, data=data)
#     #     # resp = await requests.post(sale_path, headers=header, data=data)
#     #     result = json.loads(await resp.text())
#     #     # result =  json.loads(resp.text)
#     #     if result['respCode'] != '0000':
#     #         end_time = time.time() - start_time
#     #         break
#     #     print(1)
#     # end_time = time.time() - start_time
#     # print("time is {}".format(time.time() - start_time))

if __name__ == "__main__":

    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    print(111)
    asyncio.run(main())
    # main()
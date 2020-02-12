import os
import re
import time
import json
import requests
from bs4 import BeautifulSoup
from openpyxl import Workbook as init_workbook


class DealZdscxx(object):
    def __init__(self):
        super().__init__()

    def init_sheet(self):
        self.write_wkb = init_workbook()
        self.write_sheet = self.write_wkb.create_sheet('sheet1', 0)
        self.row = 1
        self.write(['时间', '农产品名称', '价格', '单位'])

    def write(self, content):
        for index, value in enumerate(content):
            self.write_sheet.cell(self.row, index + 1, value)
        self.row += 1

    def save(self):
        self.write_wkb.save(
            time.strftime('{}.xlsx'.format("%Y-%m-%d %H-%M-%S",
                                           time.localtime())))

    def extarcting(self, data: dict):
        if not data.get('realChannel') == '分析报告日报':
            return

        self.init_sheet()
        title = data.get('title')
        sign = ':' if ':' in title else '：'

        publish_time = title.split(sign)[0]

        content = BeautifulSoup(data.get('content'), "lxml").text

        for field in ['猪肉', '牛肉', '羊肉', '鸡蛋', '白条鸡', '鲫鱼', '鲤鱼', '白鲢鱼', '大带鱼']:
            info = [publish_time, field, '公斤']
            pattern = field + r'(平均价格为)?([1-9]\d*\.\d*|0\.\d*[1-9]\d*)'
            price = re.search(pattern, content)
            if price:
                info.insert(2, price.group(2))
                self.write(info)

        self.write_wkb.save('{}.xlsx'.format(
            title.replace(sign, ' ').replace('"', '').replace('”', '')))

    def obtaining(self, page):
        page = 77
        path = f'http://zdscxx.moa.gov.cn:8080/misportal/echartReport/webData/最新发布/page{page}.json'
        header = {
            'Host': 'zdscxx.moa.gov.cn:8080',
            'User-Agent':
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36',
            'Accept':
            'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,zh;q=0.9',
        }
        resp = requests.get(path, headers=header)
        if resp.status_code == 200:
            data = json.loads(resp.text)
            return data

    def main(self):
        for page in range(66):
            data = self.obtaining(page + 1)
            if not data:
                break
            for item in data:
                self.extarcting(item)


if __name__ == "__main__":
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    spider = DealZdscxx()
    spider.main()
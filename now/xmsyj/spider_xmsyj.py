import os
import re
import time
import json
import requests
from bs4 import BeautifulSoup
from openpyxl import Workbook as init_workbook


class ExcelOpea(object):
    def __init__(self, header):
        self.init_sheet(header)
        super().__init__()

    def write(self, content):
        for index, value in enumerate(content):
            self.write_sheet.cell(self.row, index + 1, value)
        self.row += 1

    def init_sheet(self, header):
        self.wkb = init_workbook()
        self.sheet = self.write_wkb.create_sheet('sheet1', 0)
        self.row = 1

        self.write(header)

    def save(self, name):
        self.write_wkb.save(f'{name}.xlsx')


class DealXmsyj(object):
    def __init__(self):
        self.sheet1 = ExcelOpea([
            '发布日期', '监测日期', '全国规模以上生猪定点屠宰企业生猪平均收购价格', '环比', '同比', '白条肉平均出厂价格',
            '环比', '同比', '周数'
        ])
        self.sheet2 = ExcelOpea(
            ['发布日期', '监测日期', '全国500个农村集贸市场仔猪平均价格', '比去年同期涨跌'])
        self.sheet3 = ExcelOpea(['发布日期', '监测日期', '名称', '价格', '环比', '同比'])
        self.header = {
            'User-Agent':
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36',
            'Accept':
            'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'Referer': 'http://www.xmsyj.moa.gov.cn/',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,zh;q=0.9',
        }
        super().__init__()

    def extarcting(self, data: dict):
        if not data.get('realChannel') == '分析报告日报':
            return

        self.init_sheet()
        title = data.get('title')
        sign = ':' if ':' in title else '：'
        title = title.split(sign)[-1]

        # publish_time = title.split(sign)[0]
        publish_time = data.get('publishTime').split(' ')[0]

        content = BeautifulSoup(data.get('content'), "lxml").text

        for field in ['猪肉', '牛肉', '羊肉', '鸡蛋', '白条鸡', '鲫鱼', '鲤鱼', '白鲢鱼', '大带鱼']:
            info = [publish_time, field, '公斤']
            pattern = field + r'(平均价格为)?([1-9]\d*\.\d*|0\.\d*[1-9]\d*)'
            price = re.search(pattern, content)
            if price:
                info.insert(2, price.group(2))
                self.write(info)

        self.write_wkb.save('{} {}.xlsx'.format(
            publish_time,
            title.replace(sign, ' ').replace('"',
                                             '').replace('”',
                                                         '').replace('“', '')))

    def info_1(self, href):
        resp = requests.get(href, header=self.header)
        soup = BeautifulSoup(resp, 'lxml')
        info = []
        info.append(
            soup.find(attrs={
                'class': 'TRS_Editor'
            }).text.split('：')[-1])
        temp = soup.find(attrs={'align': 'justify'}).text
        temp = temp.split('。')
        pork = temp[0]
        meat = temp[1]
        temp = pork.split('，')
        info.append(temp[1])
        info.append(temp[2].replace('全国规模以上生猪定点屠宰企业生猪平均收购价格为', ''))
        info.append(temp[3].replace('环比', ''))
        info.append(temp[4].replace('同比', ''))
        temp = meat.split('，')
        info.append(temp[0].replace('白条肉平均出厂价格为', ''))
        info.append(temp[1].replace('环比', ''))
        info.append(temp[2].replace('同比', ''))

        self.sheet1.write(info)

    def info_2(self, href):
        resp = requests.get(href, header=self.header)
        soup = BeautifulSoup(resp, 'lxml')
        info = []
        info.append(
            soup.find(attrs={
                'class': 'TRS_Editor'
            }).text.split('：')[-1])
        temp = soup.find(attrs={'align': 'justify'}).text
        temp = temp.split('。')
        pork = temp[0]
        meat = temp[1]
        temp = pork.split('，')
        info.append(temp[1])
        info.append(temp[2].replace('全国规模以上生猪定点屠宰企业生猪平均收购价格为', ''))
        info.append(temp[3].replace('环比', ''))
        info.append(temp[4].replace('同比', ''))
        temp = meat.split('，')
        info.append(temp[0].replace('白条肉平均出厂价格为', ''))
        info.append(temp[1].replace('环比', ''))
        info.append(temp[2].replace('同比', ''))

        self.sheet1.write(info)

    def obtaining(self, page):
        path = f'http://www.xmsyj.moa.gov.cn/jcyj/' if page == 0 else f'http://www.xmsyj.moa.gov.cn/jcyj/index_{page}.htm'
        resp = requests.get(path, headers=self.header)
        if resp.status_code != 200:
            return
        resp.encoding = 'utf-8'
        soup = BeautifulSoup(resp.text, 'lxml')
        lis = soup.find(attrs={'id': 'div'}).find_all('li')
        hrefs = [{
            'title':
            x.a.get("title"),
            'href':
            f'http://www.xmsyj.moa.gov.cn/jcyj/{x.a.get("href").replace("./", "")}'
        } for x in lis]

        return hrefs

    def main(self):
        for page in range(25):
            data = self.obtaining(page)

            if not data:
                break

            for title in data:
                if '生猪及猪肉价格' in title:
                    pass
                elif '农村集贸市场仔猪平均价格' in title:
                    pass
                elif '畜产品和饲料集贸市场价格情况' in title:
                    pass

                self.extarcting(item)


if __name__ == "__main__":
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    spider = DealXmsyj()
    spider.main()
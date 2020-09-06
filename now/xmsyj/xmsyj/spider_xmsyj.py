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

    def write(self, content, status=1):
        for index, value in enumerate(content):
            value = remove(value) if status else value
            self.sheet.cell(self.row, index + 1, value)
        self.row += 1

    def init_sheet(self, header):
        self.wkb = init_workbook()
        self.sheet = self.wkb.create_sheet('sheet1', 0)
        self.row = 1

        self.write(header, status=0)

    def save(self, name):
        self.wkb.save(f'{name}.xlsx')


def remove(content):
    return content.replace('比前一周', '').replace('较去年同期', '').replace(
        '全国规模以上生猪定点屠宰企业生猪平均收购价格为',
        '').replace('环比',
                    '').replace('较前一周',
                                '').replace('同比',
                                            '').replace('白条肉平均出厂价格为', '')


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

    def detail(self, href):
        resp = requests.get(href, headers=self.header)
        if resp.status_code != 200:
            return
        resp.encoding = 'utf-8'
        soup = BeautifulSoup(resp.text, 'lxml')
        return soup

    def info_1(self, href):
        soup = self.detail(href)
        if not soup:
            return
        info = []
        week = soup.find(attrs={
            'class': 'sj_xiang_biaoti'
        }).text.split('周')[0] + '周'
        info.append(soup.find(attrs={'class': 'sj_dc_2'}).text.split('：')[-1])
        temp = soup.find(attrs={'class': 'TRS_Editor'})
        if not temp:
            temp = soup.find(attrs={'id': 'TRS_AUTOADD'}).p
        temp = temp.text
        temp = temp.split('。')
        pork = temp[0]
        meat = temp[1]
        temp = pork.replace(',', '，').split('，')
        info.append(temp[1])
        info.append(temp[2])
        info.append(temp[3])
        info.append(temp[4])
        temp = meat.split('，')
        info.append(temp[0])
        info.append(temp[1])
        info.append(temp[2])
        info.append(week)

        self.sheet1.write(info)

    def info_2(self, href):
        soup = self.detail(href)
        if not soup:
            return
        info = []
        info.append(soup.find(attrs={'class': 'sj_dc_2'}).text.split('：')[-1])
        temps = soup.find(attrs={'class': 'MsoNormalTable'})
        if not temps:
            temps = soup.find('table').find_all(attrs={'align': 'center'})
        else:
            temps = soup.find('table').find_all(attrs={'class': 'MsoNormal'})

        info.append(temps[2].text)
        info.append(temps[3].text)
        info.append(temps[-1].text)

        self.sheet2.write(info)

    def info_3(self, href):
        soup = self.detail(href)
        if not soup:
            return
        publish_time = soup.find(attrs={
            'class': 'sj_dc_2'
        }).text.split('：')[-1]
        content = soup.find(attrs={'class': 'TRS_Editor'})
        if not content:
            content = soup.find(attrs={'id': 'TRS_AUTOADD'})
        content = content.text.replace('与去年同期相比（以下简称同比）', '同比')
        collect_time = re.search(r'[0-9]*月份.*周（采集日为[0-9]*月[0-9]*日）',
                                 content).group()

        for field in [
                '全国活猪', '全国猪肉', '全国仔猪', '主产省份鸡蛋', '活鸡', '白条鸡', '商品代蛋雏鸡',
                '商品代肉雏鸡', '全国牛肉', '主产省份牛肉', '全国羊肉', '主产省份羊肉', '奶牛主产省（区）生鲜乳',
                '全国玉米', '主产区东北三省玉米', '主销区广东省玉米', '全国豆粕', '肉鸡配合饲料', '蛋鸡配合饲料'
        ]:

            info = [publish_time, collect_time, field.replace('全国', '')]
            pattern = field + r'(平均价格)?(\d+\.?\d*元/(只|公斤))[，。；]?比前一周((下降|上涨)\d+\.?\d*\%)[，。；]?同比((下降|上涨)\d+\.?\d*\%)'
            result = re.search(pattern, content)
            if result:
                info.append(result.group(2))
                info.append(result.group(4))
                info.append(result.group(6))
                self.sheet3.write(info)

    def obtaining(self, page):
        path = f'http://www.xmsyj.moa.gov.cn/jcyj/' if page == 0 else f'http://www.xmsyj.moa.gov.cn/jcyj/index_{page}.htm'
        soup = self.detail(path)
        if not soup:
            return
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

            for item in data:
                if '生猪及猪肉价格' in item.get('title'):
                    self.info_1(item.get('href'))
                elif '农村集贸市场仔猪平均价格' in item.get('title'):
                    self.info_2(item.get('href'))
                elif '畜产品和饲料集贸市场价格情况' in item.get('title'):
                    self.info_3(item.get('href'))

        self.sheet1.save('生猪及猪肉价格')
        self.sheet2.save('农村集贸市场仔猪平均价格')
        self.sheet3.save('畜产品和饲料集贸市场价格情况')


def main():
    spider = DealXmsyj()
    try:
        spider.main()
    except Exception as exc:
        print(f'Something Wrong, error is {exc}')


if __name__ == "__main__":
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    main()
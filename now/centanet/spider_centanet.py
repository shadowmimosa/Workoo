import csv
import json
import threading
import xmltodict
from loguru import logger
from concurrent.futures.process import ProcessPoolExecutor
from concurrent.futures.thread import ThreadPoolExecutor
from multiprocessing import freeze_support

from region import region
from utils import request, soup, run_func, mongo


@run_func()
def remove_charater(content: str):
    return content.replace('\n', '').replace('\t',
                                             '').replace('\r', '').replace(
                                                 ' ', '').replace(':', '')


class SpiderMan(object):
    def __init__(self) -> None:
        self.info = {}
        self.region_id = 0
        self.build_id = ''

        # self.writer(init=True)
        super().__init__()

    @run_func()
    def writer(self):
        if len(self.records) < 1:
            row = {
                '地区': self.info['地区'],
                '楼苑': self.info['楼苑'],
                '期数': self.info.get('期数'),
                '座数': self.info['座数'].strip('\n'),
                '地址': self.address.get('地址'),
                '入伙日期': self.address.get('入伙日期'),
                '單位數目': self.address.get('單位數目'),
                '層數': self.address.get('層數'),
                '每層伙數': self.address.get('每層伙數'),
                '所屬校網': self.address.get('所屬校網'),
                '發展商': self.address.get('發展商'),
                '管理公司': self.address.get('管理公司'),
                '物業設施': self.address.get('物業設施'),
                '單位地址': ' '.join(self.title.split()),
                '面積建': self.area.split('・')[-1].split(' ')[-1],
                '面積实': self.area.split('・')[0].split(' ')[-1],
            }
            mongo.insert(row, 'centanet')
            logger.info('插入一条')

        for record in self.records:
            row = {
                '地区': self.info['地区'],
                '楼苑': self.info['楼苑'],
                '期数': self.info.get('期数'),
                '座数': self.info['座数'].strip('\n'),
                '地址': self.address.get('地址'),
                '入伙日期': self.address.get('入伙日期'),
                '單位數目': self.address.get('單位數目'),
                '層數': self.address.get('層數'),
                '每層伙數': self.address.get('每層伙數'),
                '所屬校網': self.address.get('所屬校網'),
                '發展商': self.address.get('發展商'),
                '管理公司': self.address.get('管理公司'),
                '物業設施': self.address.get('物業設施'),
                '註冊日期': record.get('註冊日期'),
                '單位地址': ' '.join(self.title.split()),
                '面積建': self.area.split('・')[-1].split(' ')[-1],
                '面積实': self.area.split('・')[0].split(' ')[-1],
                '成交價': record.get('成交價'),
                '呎價建': record.get('呎價建'),
                '呎價实': record.get('呎價实'),
                '成交日期': record.get('成交日期'),
                '升跌': record.get('升跌')
            }
            mongo.insert(row, 'centanet')
            logger.info(
                f'{self.info["地区"]} - {self.info["期数"]} - {self.info["座数"]} - 插入一条'
            )

    @run_func()
    def writer_csv(self, init=False):
        header = [
            '地区', '楼苑', '期数', '座数', '地址', '入伙日期', '單位數目', '層數', '每層伙數', '所屬校網',
            '發展商', '管理公司', '物業設施', '註冊日期', '單位地址', '面積建', '面積实', '成交價', '呎價建',
            '呎價实', '升跌'
        ]
        with open('./detail.csv', 'a', newline='', encoding='utf-8') as fn:
            writer = csv.DictWriter(fn, header)
            if init:
                writer.writeheader()
                return

            for record in self.records:
                row = {
                    '地区': self.info['地区'],
                    '楼苑': self.info['楼苑'],
                    '期数': self.info.get('期数'),
                    '座数': self.info['座数'].strip('\n'),
                    '地址': self.address.get('地址'),
                    '入伙日期': self.address.get('入伙日期'),
                    '單位數目': self.address.get('單位數目'),
                    '層數': self.address.get('層數'),
                    '每層伙數': self.address.get('每層伙數'),
                    '所屬校網': self.address.get('所屬校網'),
                    '發展商': self.address.get('發展商'),
                    '管理公司': self.address.get('管理公司'),
                    '物業設施': self.address.get('物業設施'),
                    '註冊日期': record.get('註冊日期'),
                    '單位地址': ' '.join(self.title.split()),
                    '面積建': self.area.split('・')[-1].split(' ')[-1],
                    '面積实': self.area.split('・')[0].split(' ')[-1],
                    '成交價': record.get('成交價'),
                    '呎價建': record.get('呎價建'),
                    '呎價实': record.get('呎價实'),
                    '成交日期': record.get('成交日期'),
                    '升跌': record.get('升跌')
                }
                writer.writerow(row)
                logger.info('插入一条')

    @run_func()
    def get_memo(self, _id):
        uri = 'http://hk.centanet.com/transaction/Ajax/AjaxServices.asmx/GenTransactionHistoryPinfo'
        header = {
            'Accept': 'application/xml, text/xml, */*; q=0.01',
            'User-Agent':
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'Origin': 'http://hk.centanet.com',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,zh;q=0.9'
        }
        data = f'acode={_id}&cblgcode={self.build_id}&cci_price='

        resp = request(uri, header, data)

        info_data = xmltodict.parse(resp)
        info_data = json.loads(dict(info_data.get('string')).get('#text'))

        self.records = []
        for line in info_data.get('transRecords'):
            self.records.append({
                '註冊日期': line.get('RegDate'),
                '成交價': line.get('InsPrice'),
                '呎價建': line.get('RftUprice'),
                '呎價实': line.get('UnitPrice'),
                '成交日期': line.get('InsDate'),
                '升跌': line.get('Amplitude')
            })

        self.area = info_data.get('header').get('Area')
        self.title = info_data.get('header').get('Title')

        self.writer()

    @run_func()
    def detail(self):
        header = {
            'User-Agent':
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36',
            'Accept':
            'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,zh;q=0.9',
        }
        resp = request(self.uri, header)

        table_info = soup(resp, {'class': 'unitTran-sub-table'}, all_tag=True)

        adress_info = soup(resp, {'class': 'table1'})
        self.address = {}
        for tr in soup(adress_info, 'tr', all_tag=True):
            tds = soup(tr, 'td', all_tag=True)
            self.address[remove_charater(tds[0].text)] = remove_charater(
                tds[1].text)

        for table in table_info:
            cleaned_tr = soup(table, {'class': 'trHasTrans'}, all_tag=True)

            # if not cleaned_tr:
            #     trs = soup(table, 'tr', all_tag=True)[1:]
            #     tds = soup(trs, 'td', all_tag=True)[1:]
            for tr in cleaned_tr:
                _id = tr.get('id')
                self.get_memo(_id)

                continue

            logger.info(
                f'{self.info["地区"]} - {self.info["期数"]} - {self.info["座数"]} - 完成一栋'
            )
        logger.info(
            f'{self.info["地区"]} - {self.info["期数"]} - {self.info["座数"]} - 完成一座'
        )

    @run_func()
    def auto_sed_page(self, _type):
        uri = f'http://hk.centanet.com/transaction/transactionhistory.aspx?type={_type}&code={self.build_id}&ci=zh-hk&q={self.region_id}'
        header = {
            'User-Agent':
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36',
            'Accept':
            'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,zh;q=0.9',
        }
        resp = request(uri, header)

        left_info = soup(resp, {'class': 'unitTran-left-a'})

        left_info_tr = list(filter(lambda x: not isinstance(x, str),
                                   left_info))

        for tr_info in left_info_tr:
            if isinstance(tr_info, str):
                continue

            if tr_info.td.get(
                    'class') and 'unitTran-left-a-estate' in tr_info.td.get(
                        'class'):
                self.info['期数'] = remove_charater(tr_info.text)

            elif tr_info.a and tr_info.a.get('href'):
                href = tr_info.a.get('href')
                self.uri = f'http://hk.centanet.com/transaction/{href}'
                self.info['座数'] = remove_charater(tr_info.text)

                # print(self.info)
                self.detail()

    @run_func()
    def auto_page(self):
        uri = 'http://hk.centanet.com/transaction/Ajax/AjaxServices.asmx/paddresssearch1'
        header = {
            'Accept': 'application/xml, text/xml, */*; q=0.01',
            'User-Agent':
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'Origin': 'http://hk.centanet.com',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,zh;q=0.9'
        }
        for page in range(1000):
            data = f'type=22&code={self.region_id}&pageIndex={page+1}&pageSize=20&columnName=vol180&order=desc'

            resp = request(uri, header, data)
            build_data = xmltodict.parse(resp)
            build_data = json.loads(
                dict(build_data.get('string')).get('#text')).get('d')

            for build in build_data:
                self.build_id = build.get('code')
                self.info['楼苑'] = build.get('namec')
                self.auto_sed_page(build.get('type'))

            if len(build_data) < 20:
                break

    def run(self, area, raea_id):
        self.info['地区'] = area
        self.region_id = raea_id

        self.auto_page()


def multi():
    spider = SpiderMan()

    with ProcessPoolExecutor(max_workers=15) as executor:
        for item in region:
            for second_region_item in item.get('item'):
                area = second_region_item.get('name')
                area_id = second_region_item.get('id')

                executor.submit(spider.run, area, area_id)
                # SpiderMan().run('山頂/南區', 107)
                # SpiderMan().run(area, area_id)

        # executor.shutdown(wait=True)


if __name__ == "__main__":
    freeze_support()
    multi()
    # spider = SpiderMan()
    # spider.run()

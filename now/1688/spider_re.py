from utils.request import Query
from utils.soup import DealSoup
from config import logger, Cookie

from urllib.parse import quote

import json
import time
import csv


def magic_time(during=2):
    def decorator(func):
        def wrapper(*args, **kwargs):
            start_time = time.time()
            # print('函数开始运行的时间为：', time.strftime('%Y:%m:%d %H:%M:%S', start_time))
            result = func(*args, **kwargs)
            magic = time.time() - start_time - during
            if magic < 0:
                time.sleep(-magic)
            return result

        return wrapper

    return decorator


class Deal(object):
    def __init__(self, cookie):
        super().__init__()
        self.cookie = cookie
        self.req = Query().run
        self.soup = DealSoup().judge
        self.header = {
            'Host': '',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent':
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.79 Safari/537.36',
            'Sec-Fetch-User': '?1',
            # Cache-Control: max-age=0
            'Accept':
            'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'Sec-Fetch-Site': 'same-site',
            'Sec-Fetch-Mode': 'navigate',
            'Referer': '',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Cookie': self.cookie
        }

    @magic_time()
    def good_detail(self, html):
        try:
            href = self.soup(html, attr='a').get('href')
        except AttributeError:
            logger.info('null')
            return

        html = self.req(path=href, header=self.header)

        self.info['产品网址'] = href.split('?')[0]

        self.info['产品名称'] = self.soup(html, attr={'class': 'd-title'}).text
        self.info['产品价格'] = self.soup(self.soup(
            html, attr={'id': 'mod-detail-price'}),
                                      attr={
                                          'class': 'value'
                                      }).text

        self.info['产品评论等级'] = self.soup(html,
                                        attr={'property':
                                              'og:product:score'})['content']
        temp = self.soup(html,
                         attr={'id':
                               'mod-detail-dealrecord'})['data-mod-config']

        data = json.loads(temp)

        self.info['产品评论量'] = data['totalRate']
        self.info['产品交易量'] = data['title'].replace('成交 <em>(',
                                                   '').replace(')</em>', '')

        href = self.soup(self.soup(html, attr={'class': 'creditdetail-page'}),
                         attr='a')['href']

        self.header['Referer'] = href
        self.shop_detail(href)

    @magic_time()
    def shop_detail(self, path):
        self.header['Host'] = path.replace('https://', '').split('/')[0]

        html = self.req(path=path, header=self.header)

        info_box = self.soup(html, attr={'class': 'info-box'})
        self.info['供应商名称'] = self.soup(info_box, attr={
            'class': 'name-text'
        }).text
        self.info['诚信通年数'] = self.soup(info_box,
                                       attr={
                                           'class': 'icon icon-chengxintong'
                                       }).text

        self.info['诚信等级'] = self.soup(self.soup(info_box,
                                                attr={'class':
                                                      'company-name'}),
                                      attr='a',
                                      all_tag=True)[-1].text

        li_list = self.soup(self.soup(html, attr={'class': 'section-main'}),
                            attr='li',
                            all_tag=True)

        self.info['累计成交数'] = self.soup(li_list[0],
                                       attr={
                                           'class': 'record-num'
                                       }).text
        self.info['累计买家数'] = self.soup(li_list[1],
                                       attr={
                                           'class': 'record-num'
                                       }).text
        self.info['重复购买率'] = self.soup(li_list[2],
                                       attr={
                                           'class': 'record-num'
                                       }).text
        self.info['退货率'] = self.soup(li_list[3], attr={
            'class': 'record-num'
        }).text

        self.info['诚信通年数'] = self.info['诚信通年数'].replace('第',
                                                        '').replace('年', '')

    def main(self):
        category = [
            '车载mp3',
            '行车记录仪',
            'GPS定位器',
            '车载空气净化器',
            '车载吸尘器',
            '车载摄像头',
            '车载充电器',
            '车载显示器',
            '车载手机支架',
            '车载蓝牙耳机',
            '车载蓝牙音箱',
            '车载储物',
            '车载冰箱',
            '车载充电器',
            '车载逆变器'
        ]
        with open('./data/already.txt', 'r', encoding='utf-8') as fn:
            already = fn.read().split('\n')
        error_count = 0
        for keyword in category:
            count, page = (0, 1) if keyword != '车载充电器' else (56, 3)
            keyword = quote(str(keyword).encode('gbk'))
            while count < 256:
                self.header['Host'] = 's.1688.com'

                if page == 1:
                    self.header['Referer'] = 'https://auto.1688.com/'
                    path = 'https://s.1688.com/company/company_search.htm?select-faker=companys&keywords={}&n=y&mastheadtype=&from=industrySearch&industryFlag='.format(
                        keyword)
                    resp = self.req(path, header=self.header)
                else:
                    # self.header['Referer'] = path
                    # path = 'https://s.1688.com/company/company_search.htm?keywords={}&button_click=top&earseDirect=false&n=y&netType=1%2C11&from=offer_search&pageSize=30&offset=3&beginPage={}'.format(
                    # keyword, page)
                    # path = 'https://s.1688.com/company/company_search.htm?keywords=%E8%BD%A6%E8%BD%BDmp3&button_click=top&earseDirect=false&n=y&netType=1%2C11&from=offer_search&pageSize=30&offset=3&beginPage=2'
                    path = 'https://s.1688.com/company/company_search.htm?keywords={}&netType=1%2C11&earseDirect=false&button_click=top&n=y&pageSize=30&from=offer_search&offset=3&beginPage={}'.format(
                        keyword, page)
                    header = {
                        'Host': 's.1688.com',
                        'Cache-Control': 'max-age=0',
                        'Origin': 'https://s.1688.com',
                        'Upgrade-Insecure-Requests': '1',
                        'Content-Type': 'application/x-www-form-urlencoded',
                        'User-Agent':
                        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.79 Safari/537.36',
                        'Sec-Fetch-User': '?1',
                        'Accept':
                        'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
                        'Sec-Fetch-Site': 'same-origin',
                        'Sec-Fetch-Mode': 'navigate',
                        'Referer':
                        'https://s.1688.com/company/company_search.htm?keywords=%B3%B5%D4%D8mp3&netType=1%2C11&earseDirect=false&button_click=top&n=y&pageSize=30&from=offer_search&offset=3&beginPage=3',
                        'Accept-Encoding': 'gzip, deflate, br',
                        'Accept-Language': 'zh-CN,zh;q=0.9',
                        'Cookie': self.cookie
                    }
                    resp = self.req(path, header=header, data=True)

                time.sleep(1)
                goods = self.soup(resp,
                                  attr={'class': 'company-list-item'},
                                  all_tag=True)

                for good in goods:
                    title = self.soup(good,
                                      attr={'class':
                                            'list-item-title-text'})['title']
                    if title in already:
                        logger.info('alrady have')
                        continue
                    else:
                        already.append(title)

                    self.info = {}
                    self.header['Referer'] = path
                    self.header['Host'] = 'detail.1688.com'

                    try:
                        self.good_detail(
                            self.soup(good,
                                      attr={'class': 'list-item-itemsWrap'}))
                    except Exception as exc:
                        logger.error('Error: {}\n path is {}'.format(
                            exc, path))
                        error_count += 1
                        if error_count > 15:
                            print(time.time(), keyword, count)
                            return
                        else:
                            continue

                    write(self.info)
                    count += 1
                page += 1


def remove_charater(content: str):
    return content.replace('\n', '').replace('\t',
                                             '').replace('\r',
                                                         '').replace(' ', '')


def write(content=None):
    title_list = [
        '供应商名称', '诚信通年数', '诚信等级', '累计成交数', '累计买家数', '重复购买率', '退货率', '产品名称',
        '产品价格', '产品评论量', '产品评论等级', '产品交易量', '产品网址'
    ]
    if content is None:
        need = title_list
    elif len(content) == 0:
        return
    else:
        need = [content[key] for key in title_list]

    need = [remove_charater(value) for value in need]

    with open('./data/data.csv', 'a', encoding='utf-8') as fn:
        writer = csv.writer(fn)
        writer.writerow(need)

    with open('./data/already.txt', 'a', encoding='utf-8') as fn:
        fn.write(need[0])
        fn.write('\n')


if __name__ == "__main__":
    # write()

    Deal(Cookie).main()

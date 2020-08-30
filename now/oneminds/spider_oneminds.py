import os
import time
# import json

import arrow
from configparser import ConfigParser
# import datetime
# from urllib.parse import urlparse, parse_qs, urlencode

from utils import logger, run_func, request

from utils.common import get_in
from utils.db import MysqlOpea, SqliteOpea
from utils.signer import magic


def remove(content: str):
    return content.replace('\r',
                           '').replace('\n',
                                       '').replace(' ',
                                                   '').replace('\xa0', '')


def get_timestamps(timestamps=0):
    if timestamps == 0:
        return int(time.time() * 1000)
    elif timestamps == 1:
        return arrow.now().replace(hour=0, minute=0, second=0).timestamp
    elif timestamps == 2:
        return arrow.now().replace(hour=23, minute=59, second=0).timestamp


def write(content):
    with open('./top_category.txt', 'a', encoding='utf-8') as fn:
        fn.write(content)
        fn.write('\n')


class MyParser(ConfigParser):
    def to_dict(self):
        d = dict(self._sections)
        for k in d:
            d[k] = dict(d[k])
        return d


class DealOneminds:
    def __init__(self, database={}):
        self.header = {
            'User-Agent':
            'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36 MicroMessenger/7.0.9.501 NetType/WIFI MiniProgramEnv/Windows WindowsWechat',
            'content-type': 'application/x-www-form-urlencoded',
            # Referer: https://servicewechat.com/wx975908a83811915b/49/page-frame.html
            'Accept-Encoding': 'gzip, deflate, br'
        }
        self.goods = []
        self.mysql = MysqlOpea(database)
        self.sqlite = SqliteOpea('goods.db')
        self.all_goods = {}
        super().__init__()

    def init_category(self):
        uri = f'https://ec.oneminds.cn/api/goods/group?platform=2&session_id=&sid=100043&store_id={self.store_id}&timestamp={get_timestamps()}'
        resp = request(uri, header=self.header, json=True)
        if resp.get('code') != 200:
            return

        top_categories = resp.get('data')
        top_category_count = len(top_categories)
        for top_category in top_categories:
            top_category_name = top_category.get('name')

            top_category_id = self.mysql.insert_category(
                top_category_name, sort=top_category_count)

            sub_categories = top_category.get('mid')
            if not sub_categories:
                continue
            sub_category_count = len(sub_categories)

            for sub_category in sub_categories:
                sub_category_name = sub_category.get('name')

                self.mysql.insert_category(sub_category_name, top_category_id,
                                           sub_category_count)

                sub_category_count -= 1
            top_category_count -= 1

    def goods_group(self):
        self.init_category()

        # uri = 'https://ec.oneminds.cn/api/goods/group?platform=2&session_id={self.session_id}&sid=100043&store_id={self.store_id}&timestamp=1597390905005'
        uri = f'https://ec.oneminds.cn/api/goods/group?platform=2&session_id=&sid=100043&store_id={self.store_id}&timestamp={get_timestamps()}'
        resp = request(uri, header=self.header, json=True)
        if resp.get('code') != 200:
            return

        for top_category in resp.get('data'):
            self.big_name = top_category.get('name')
            self.big_id = top_category.get('id')

            if self.save_category:
                write(self.big_name)
                continue
            if self.big_name not in self.categories:
                continue

            self.top_category_id = self.mysql.insert_category(self.big_name)

            if not top_category.get('mid'):
                self.mid_name = self.big_name
                self.mid_id = 0
                self.sub_category_id = self.top_category_id
                self.goods_list()
                self.to_order()
                continue

            for sub_category in top_category.get('mid'):
                self.mid_name = sub_category.get('name')
                self.mid_id = sub_category.get('id')
                self.sub_category_id = self.mysql.insert_category(
                    self.mid_name, self.top_category_id)

                self.goods_list()

            self.to_order()

    def goods_list(self):
        count = 10
        page = 0
        while page * 10 <= count:
            uri = f'https://ec.oneminds.cn/api/goods/list?platform=2&session_id={self.session_id}&sid=100043&store_id={self.store_id}&rp=10&page={page+1}&big_id={self.big_id}&mid_id={self.mid_id}&small_id=0&sort=&order=desc&qs=1&goods_type=0&keyword=&timestamp={get_timestamps()}'
            resp = request(uri, header=self.header, json=True)
            if not resp.get('data'):
                return

            count = resp.get('data').get('count')

            for data in resp.get('data').get('list'):
                self.good_id = data.get('id')
                self.goods_detail()

            page += 1

    def to_order(self):
        count = 10
        page = 0
        goods = []
        while page * 10 <= count:
            uri = f'https://ec.oneminds.cn/api/goods/list?platform=2&session_id={self.session_id}&sid=100043&store_id={self.store_id}&rp=10&page={page+1}&big_id={self.big_id}&mid_id=0&small_id=0&sort=&order=desc&qs=1&goods_type=0&keyword=&timestamp={get_timestamps()}'
            resp = request(uri, header=self.header, json=True)
            if not resp.get('data'):
                return

            count = resp.get('data').get('count')

            for data in resp.get('data').get('list'):
                codes = data.get('sku_id')
                if codes not in self.all_goods:
                    continue
                goods.append(codes)

            page += 1

        for codes in goods:
            item = self.all_goods[codes]

            good_info = item['good']
            common_info = item['common']
            img = item['img']
            good_info['index_sort'] = count

            good_id = self.mysql.insert_good(good_info)
            info_data = f'{good_info["codes"]},{good_id},{self.grounding},"{self.big_name}"'
            self.already_goods.remove(good_info['codes']) if good_info[
                'codes'] in self.already_goods else self.sqlite.insert(
                    info_data)
            self.mysql.configure_category(item['category'], good_id)
            common_info['goods_id'] = good_id
            self.mysql.insert_common(common_info)
            self.mysql.insert_image(good_id, img)

            logger.info(f'已添加 - {good_id}')

            count -= 1

        self.all_goods = {}

    @run_func()
    def goods_detail(self):
        uri = f'https://ec.oneminds.cn/api/goods?platform=2&session_id={self.session_id}&sid=100043&store_id={self.store_id}&id={self.good_id}&goods_type=1&timestamp={get_timestamps()}'
        resp = request(uri, header=self.header, json=True)
        data = resp.get('data')
        good_info = {}
        common_info = {}
        good_info = {}

        if get_in(data, 'sku.activity_type') in (3, 4):
            common_info['is_spike_buy'] = 1
        else:
            common_info['is_spike_buy'] = 0

        good_info['grounding'] = self.grounding
        name = get_in(data, 'sku.goods_name')
        good_info['goodsname'] = name.replace('1份', '').replace(
            'SX', '').replace('Way', '').replace('臻选', '精品')

        good_info['subtitle'] = get_in(data, 'base.sub_heads')
        good_info['sales'] = get_in(data, 'base.sales_qty')
        good_info['codes'] = get_in(data, 'sku.sku_id')
        good_info['total'] = get_in(data, 'sku.store')
        good_info['is_all_sale'] = self.is_all_sale

        good_info['productprice'] = get_in(data, 'sku.market_price')
        good_info['costprice'] = get_in(data, 'sku.price')
        good_info['price'] = get_in(data, 'sku.sale_price')

        if good_info['productprice'] < good_info['price']:
            good_info['productprice'] = good_info['price']

        common_info['big_img'] = get_in(data, 'sku.pic')
        common_info['goods_start_count'] = get_in(data, 'base.min_buy_qty')
        common_info['video'] = get_in(data, 'base.video_list')
        # common_info['begin_time'] = ''
        # common_info['end_time'] = ''
        common_info['oneday_limit_count'] = get_in(data, 'sku.max_buy_qty')
        common_info['content'] = get_in(data, 'base.description')
        common_info['diy_arrive_details'] = self.diy_arrive_details
        common_info['pick_up_type'] = self.pick_up_type

        common_info['begin_time'] = get_timestamps(1)
        common_info['end_time'] = get_timestamps(2)

        common_info[
            'video'] = common_info['video'][0] if common_info['video'] else ''

        self.all_goods[good_info['codes']] = {
            'good': good_info,
            'common': common_info,
            'img': get_in(data, 'pic_list'),
            'category': self.sub_category_id
        }

        logger.info(f'已加载 - {good_info["codes"]}')

    def login(self):
        verify_uri = f'https://ec.oneminds.cn/api/member/check?platform=2&session_id={self.session_id}&sid=100043&store_id={self.store_id}&mobile={self.mobile}&timestamp={get_timestamps()}'
        resp = request(verify_uri, header=self.header, json=True)
        csrf_token = get_in(resp, 'data.csrf_token')
        sms_uri = f'https://ec.oneminds.cn/api/sms?platform=2&session_id={self.session_id}&sid=100043&store_id={self.store_id}&mobile={self.mobile}&csrf_token={csrf_token}&timestamp={get_timestamps()}'
        resp = request(sms_uri, header=self.header, json=True)

        if resp.get('code') != 200:
            logger.error(f'登录失败 - {resp.get("message")}')
            return

        verify_code = input('输入验证码')
        login_uri = f'https://ec.oneminds.cn/api/member/login?platform=2&session_id={self.session_id}&sid=100043&store_id={self.store_id}&mobile={self.mobile}&smsyzm={verify_code}&longitude=126.562060&latitude=43.821420&user_id=0&timestamp={get_timestamps()}'
        resp = request(login_uri, header=self.header, json=True)

        if resp.get('code') != 200:
            logger.error(f'登录失败 - {resp.get("message")}')
            return

        return True

    def run(self,
            save_category=None,
            categories=[],
            fields={},
            default={},
            store=6,
            phone='',
            login=None):
        self.save_category = save_category
        self.categories = categories
        self.fields = fields
        self.session_id = 'aa886aee473a9f21dfd97c37e1518a72'
        self.store_id = store
        self.is_all_sale = 1
        self.mobile = phone

        self.grounding = int(default.get('grounding'))
        self.diy_arrive_details = default.get('diy_arrive_details')
        self.pick_up_type = int(default.get('pick_up_type'))

        if self.grounding not in (0, 1):
            logger.error('输入正确的 grounding')
            return
        if not self.diy_arrive_details:
            self.diy_arrive_details = ''
        if self.pick_up_type not in (1, 2, 3, 4):
            logger.error('输入正确的 pick_up_type')
            return

        if login == 1:
            if not self.login():
                logger.error('登录失败')
                return

        self.already_goods = self.sqlite.select()

        self.goods_group()

        for codes in self.already_goods:
            goods_id, category = self.sqlite.select_good(codes)
            if category not in self.categories:
                logger.info(f'未采集该商品分类, 暂不下架 - {goods_id}')
                continue
            self.mysql.change_grounding(goods_id)
            self.sqlite.update(codes)
            logger.info(f'已下架 - {goods_id}')


def main():
    config = MyParser()
    config.read('./config.ini', encoding='utf-8')
    config = config.to_dict()
    fields = config.get('Field')
    default = config.get('Default')
    store = config.get('Store').get('id')
    database = config.get('DataBase')
    save_category = int(get_in(config, 'Category.save'))
    phone = get_in(config, 'Account.phone')
    login = int(get_in(config, 'Account.login'))
    spider = DealOneminds(database)

    if save_category:
        os.remove('./top_category.txt')
        spider.run(save_category,
                   fields=fields,
                   default=default,
                   store=store,
                   phone=phone,
                   login=login)
    else:
        with open('./top_category.txt', 'r', encoding='utf-8') as fn:
            categories = fn.read().split('\n')

        spider.run(categories=categories,
                   fields=fields,
                   default=default,
                   store=store,
                   phone=phone,
                   login=login)


if __name__ == "__main__":
    magic()
    try:
        main()
    except Exception as exc:
        logger.error(f'运行失败 - {exc}')

    input('按任意键退出')

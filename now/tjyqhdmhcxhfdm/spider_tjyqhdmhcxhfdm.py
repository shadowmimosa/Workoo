import os
import time
import json
import hashlib
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor

from utils.log import logger
from utils.run import run_func
from utils.mongo import Mongo
from utils.soup import DealSoup
from config import DOMAIN, PROXY, HEADER
from utils.request import Query, DealRequest


def made_secret():
    timestamp = int(time.time())
    orderno = PROXY.get('orderno')
    secret = PROXY.get('secret')
    txt = f'orderno={orderno},secret={secret},timestamp={timestamp}'
    sign = hashlib.md5(txt.encode('utf-8')).hexdigest().upper()

    return f'sign={sign}&orderno={orderno}&timestamp={timestamp}&change=true'


def build_header():
    _header = HEADER

    # HEADER['User-Agent'] = ua()

    if PROXY.get('proxy'):
        _header.update({'Proxy-Authorization': made_secret()})

    return _header


class QueryHandle(object):
    def __init__(self):
        super().__init__()
        if PROXY.get('proxy'):
            self.req = DealRequest({
                "http":
                "http://dynamic.xiongmaodaili.com:8089",
                "https":
                "http://dynamic.xiongmaodaili.com:8089"
            }).run
        else:
            self.req = DealRequest().run

        self.soup = DealSoup().judge

    def to_mongo(self, info=None):
        if not info:
            info = {
                'year': self.year,
                'province_code': self.province_code,
                'province_name': self.province_name,
                'city_code': self.city_code,
                'city_name': self.city_name,
                'county_code': self.county_code,
                'county_name': self.county_name,
                'town_code': self.town_code,
                'town_name': self.town_name,
                'village_code': self.village_code,
                'village_sub_code': self.village_sub_code,
                'village_name': self.village_name
            }
        table = f'tjyqhdmhcxhfdm_{self.year}'
        result = Mongo.insert(info, table)
        logger.info(f'已插入 - {result}')

    def build_href(self, path, clip):
        return path.replace(path.split('/')[-1], '') + clip

    def get_clip(self, obj):
        return

    def village_handle(self, path):
        resp = self.req(path, header=build_header())

        villagetrs = self.soup(resp, {'class': 'villagetr'}, all_tag=True)

        for villagetr in villagetrs:
            tds = self.soup(villagetr, 'td', all_tag=True)
            self.village_code = tds[0].text
            self.village_sub_code = tds[1].text
            self.village_name = tds[2].text

            self.to_mongo()

    def town_handle(self, path):
        resp = self.req(path, header=build_header())

        towntrs = self.soup(resp, {'class': 'towntr'}, all_tag=True)

        for towntr in towntrs:
            tds = self.soup(towntr, 'td', all_tag=True)
            self.town_code = tds[0].text
            self.town_name = tds[-1].text

            if not tds[0].a:
                info = {
                    'year': self.year,
                    'province_code': self.province_code,
                    'province_name': self.province_name,
                    'city_code': self.city_code,
                    'city_name': self.city_name,
                    'county_code': self.county_code,
                    'county_name': self.county_name,
                    'town_code': self.town_code,
                    'town_name': self.town_name,
                }
                self.to_mongo(info)
                continue

            clip = tds[0].a.get('href')
            href = self.build_href(path, clip)

            self.village_handle(href)

    def county_handle(self, path):
        if not Mongo.select('tjyqhdmhcxhfdm_href', {
                'path': path,
                'status': 1
        }):
            result = Mongo.repeat({
                'path': path,
                'status': 0
            }, 'tjyqhdmhcxhfdm_href')
            logger.info(f'开始爬取列表 - {result} - {path}')
        else:
            logger.info(f'已存在 - {path}')
            return

        resp = self.req(path, header=build_header())

        countytrs = self.soup(resp, {'class': 'countytr'}, all_tag=True)

        for countytr in countytrs:
            tds = self.soup(countytr, 'td', all_tag=True)
            self.county_code = tds[0].text
            self.county_name = tds[-1].text

            if not tds[0].a:
                info = {
                    'year': self.year,
                    'province_code': self.province_code,
                    'province_name': self.province_name,
                    'city_code': self.city_code,
                    'city_name': self.city_name,
                    'county_code': self.county_code,
                    'county_name': self.county_name,
                }
                self.to_mongo(info)
                continue

            clip = tds[0].a.get('href')
            href = self.build_href(path, clip)

            self.town_handle(href)

        result = Mongo.update({
            '_id': result,
        }, {
            'status': 1,
            'year': self.year,
            'province_code': self.province_code,
            'province_name': self.province_name,
            'city_code': self.city_code,
            'city_name': self.city_name,
            'county_code': self.county_code,
            'county_name': self.county_name,
        }, 'tjyqhdmhcxhfdm_href')

        logger.info(f'已完成 - {result} - {path}')

    def city_handle(self, path):
        resp = self.req(path, header=build_header())

        citytrs = self.soup(resp, {'class': 'citytr'}, all_tag=True)

        for citytr in citytrs:
            tds = self.soup(citytr, 'td', all_tag=True)
            self.city_code = tds[0].text
            self.city_name = tds[-1].text

            if not tds[0].a:
                info = {
                    'year': self.year,
                    'province_code': self.province_code,
                    'province_name': self.province_name,
                    'city_code': self.city_code,
                    'city_name': self.city_name,
                }
                self.to_mongo(info)
                continue

            clip = tds[0].a.get('href')
            href = self.build_href(path, clip)

            run_func(self.county_handle, href)

    def province_handle(self):
        path = f'{DOMAIN}/{self.year}/index.html'

        resp = self.req(path, header=build_header())

        provincetrs = self.soup(resp, {'class': 'provincetr'}, all_tag=True)

        for provincetr in provincetrs:
            tds = self.soup(provincetr, 'td', all_tag=True)
            for td in tds:
                clip = td.a.get("href")
                href = self.build_href(path, clip)
                self.province_code = clip.split('.')[0]
                self.province_name = td.a.text

                run_func(self.city_handle, href)

    def run(self, year):
        self.year = year
        run_func(self.province_handle)


def mutl():
    thead_pool = ProcessPoolExecutor(3)
    for year in range(2013, 2020):
        thead_pool.submit(QueryHandle().run, year)


def main():
    spider = QueryHandle()
    for year in range(2013, 2020):
        run_func(spider.run, year)


if __name__ == "__main__":
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    # main()
    mutl()
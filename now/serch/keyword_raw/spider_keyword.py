import os
import time
import pyodbc
import hashlib
import urllib3
import datetime
import requests
from http import cookiejar
from configparser import ConfigParser
from multiprocessing import Pool, freeze_support

from utils.common import soup, remove_charater


class Mssql(object):
    def __init__(self):
        self.init_sql()
        super().__init__()

    def init_sql(self):
        conn = pyodbc.connect(
            f'DRIVER={{SQL Server}};SERVER={CONFIG.get("Mssql", "host")};DATABASE={CONFIG.get("Mssql", "database")};UID={CONFIG.get("Mssql", "user")};PWD={CONFIG.get("Mssql", "password")}',
            autocommit=True)
        cursor = conn.cursor()
        self.cursor = cursor

    def select(self):
        self.cursor.execute(f'{CONFIG.get("Condition", "sql")}')
        return self.cursor.fetchall()

    def update(self, result, _id):
        sql = f'UPDATE [dbo].[keyword_View] SET [cxdate] = \'{time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())}\', [Resultstr] = \'{result}\' WHERE [id] = {_id};'
        self.cursor.execute(sql)

    def insert(self, obj: dict):
        sql = 'INSERT INTO [dbo].[keywords_pm]([AuthCode], [keyword], [keytype], [sstype], [paiming]) VALUES (\'{AuthCode}\', \'{keyword}\', \'{keytype}\', \'{sstype}\', \'{paiming}\');'.format(
            **obj)
        self.cursor.execute(sql)


def clean_url(content: str):
    return content.replace('http://', '').replace('https://',
                                                  '').replace('www.', '')


def to_mssql(item):
    for key in item:
        value = item[key]
        if isinstance(value, str):
            item[key] = value.encode('gbk').decode('latin-1')
    return item


def judge_pages():
    need = {}
    for site in ['baidu', 'mbaidu', 'so']:
        temp = CONFIG.get('Spider', site)
        if temp is None:
            continue
        try:
            page = int(temp)
        except:
            input('页数输入有误, 任意键退出')
            os._exit(0)
        else:
            need[site] = page

    return need


def get_type(site):
    if site == 'baidu':
        return 1
    elif site == 'mbaidu':
        return 11
    else:
        return 2


def made_secret():
    timestamp = int(time.time())
    orderno = CONFIG.get("Proxy", "orderno")
    secret = CONFIG.get("Proxy", "secret")
    txt = f'orderno={orderno},secret={secret},timestamp={timestamp}'
    sign = hashlib.md5(txt.encode('utf-8')).hexdigest().upper()

    return f'sign={sign}&orderno={orderno}&timestamp={timestamp}&change=true'


class Keyword(object):
    def __init__(self):
        self.init_session()
        self.proxy = {
            "http": "http://dynamic.xiongmaodaili.com:8088",
            "https": "http://dynamic.xiongmaodaili.com:8088"
        }

        super().__init__()

    def init_session(self):
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
        session = requests.session()
        session.verify = False
        session.keep_alive = False
        self.session = session

    def set_cookies(self, site):
        if site == 'baidu':
            self.session.cookies = self._request(
                'https://www.baidu.com/').cookies
            self.session.headers = {
                'Accept': '*/*',
                "User-Agent":
                'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.100 Safari/537.36',
                'Accept-Encoding': 'gzip, deflate, br',
                'Accept-Language': 'zh-CN,zh;q=0.9'
            }
        elif site == 'mbaidu':
            self.session.headers = {
                'Accept': '*/*',
                "User-Agent":
                'Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1',
                'Accept-Encoding': 'gzip, deflate, br',
                'Accept-Language': 'zh-CN,zh;q=0.9'
            }
            self.session.cookies = self._request(
                'https://m.baidu.com/').cookies
        elif site == 'so':
            self.session.headers = {
                'Accept': '*/*',
                "User-Agent":
                'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.100 Safari/537.36',
                'Accept-Encoding': 'gzip, deflate, br',
                'Accept-Language': 'zh-CN,zh;q=0.9'
            }
            # self.session.cookies = self._request('https://www.so.com/').cookies
            self.session.cookies = cookiejar.CookieJar()

        if self.proxy:
            self.session.headers.update({'Proxy-Authorization': made_secret()})

    def _request(self, path):
        if PROXY:
            proxy = self.proxy
        else:
            proxy = None
        retry_count = 5
        while retry_count > 0:
            try:
                resp = self.session.get(path, proxies=proxy)
            except Exception as exc:
                retry_count -= 1
                print(exc)
            else:
                if resp.status_code == 200:
                    text = resp.text
                    if '百度安全验证' in text or '360搜索_访问异常出错' in text:
                        retry_count -= 1
                    else:
                        return resp
                else:
                    retry_count -= 1
        else:
            return '请求异常'

    def baidu(self, keyword: str, domain: str):
        result = []
        if SITES['baidu'] <= 0:
            return
        for page in range(SITES['baidu']):
            path = f'https://www.baidu.com/s?ie=utf-8&mod=1&wd={keyword}&pn={page*10}'
            resp = self._request(path)
            if isinstance(resp, str):
                return False, resp
            containers = soup(resp.text, {'class': 'c-container'},
                              all_tag=True)

            for index, container in enumerate(containers):
                url_obj = soup(container, {'class': 'c-showurl'})
                if not url_obj:
                    continue
                url = url_obj.text
                # domain = 'baidu.com'
                if domain in url:
                    result.append(str(page * 10 + index + 1))

        if not result:
            return False, 'baidu-0'
        else:
            return True, 'baidu-' + ','.join(result)

    def mbaidu(self, keyword: str, domain: str):
        result = []
        if SITES['mbaidu'] <= 0:
            return
        for page in range(SITES['mbaidu']):
            path = f'https://m.baidu.com/s?pn={page*10}&usm=9&word={keyword}'
            resp = self._request(path)
            if isinstance(resp, str):
                return False, resp
            containers = soup(resp.text,
                              {'class': 'c-showurl c-footer-showurl'},
                              all_tag=True)

            for index, container in enumerate(containers):
                url = container.text
                if domain in url:
                    result.append(str(page * 10 + index + 1))

        if not result:
            return False, 'mbaidu-0'
        else:
            return True, 'mbaidu-' + ','.join(result)

    def so(self, keyword: str, domain: str):
        result = []
        if SITES['so'] <= 0:
            return
        for page in range(1, SITES['so'] + 1):
            self.set_cookies('so')
            path = f'https://www.so.com/s?q={keyword}&pn={page}'
            resp = self._request(path)
            if isinstance(resp, str):
                return False, resp
            containers = soup(resp.text, {'class': 'res-linkinfo'},
                              all_tag=True)
            for index, container in enumerate(containers):
                url = container.cite.text
                if domain in url:
                    result.append(str(page * 10 + index + 1))

        if not result:
            return False, '360-0'
        else:
            return True, '360-' + ','.join(result)


def detail(item: tuple):
    result_str = []
    for site in SITES:
        query = Keyword()
        query.set_cookies(site)
        domain = clean_url(item[10])
        keyword = item[2]
        command = f'query.{site}(keyword, domain)'
        status, result = eval(command)
        result_str.append(result)
        if status:
            MSSQL.insert({
                'AuthCode': item[1],
                'keyword': item[2],
                'keytype': item[4],
                'sstype': get_type(site),
                'paiming': result.split('-')[-1]
            })
        print(result)
    MSSQL.update('|'.join(result_str), item[0])

    time.sleep(int(CONFIG.get('Sleep','second')))


def single(results):
    for item in results:
        item[2].encode('utf8')
        detail(item)


def multi(results):
    num = int(CONFIG.get('Process', 'num'))
    pool = Pool(num)

    for item in results:
        pool.apply_async(detail, (item, ))

    pool.close()
    pool.join()


def main():
    while True:
        results = MSSQL.select()
        if not results:
            time.sleep(300)
        else:
            # single(results)
            multi(results)


CONFIG = ConfigParser()
CONFIG.read('config.ini', encoding='utf-8')
SITES = judge_pages()
MSSQL = Mssql()
PROXY = True if CONFIG.get('Proxy', 'proxy') == '1' else False

if __name__ == "__main__":
    freeze_support()
    main()

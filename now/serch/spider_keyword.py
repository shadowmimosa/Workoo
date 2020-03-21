import os
import time
import random
import pyodbc
import hashlib
import urllib3
import datetime
import requests
import concurrent
import threading
from http import cookiejar
from configparser import ConfigParser
from concurrent.futures import ThreadPoolExecutor
from multiprocessing import Pool, freeze_support, current_process
from utils.common import soup, logger, remove_charater


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


def get_ua(mobile=False):
    if mobile:
        return random.choice([
            'Mozilla/5.0 (Linux; U; Android 8.1.0; zh-cn; BLA-AL00 Build/HUAWEIBLA-AL00) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/57.0.2987.132 MQQBrowser/8.9 Mobile Safari/537.36',
            'Mozilla/5.0 (Linux; Android 6.0.1; OPPO A57 Build/MMB29M; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/63.0.3239.83 Mobile Safari/537.36 T7/10.13 baiduboxapp/10.13.0.10 (Baidu; P1 6.0.1)',
            'Mozilla/5.0 (iPhone 92; CPU iPhone OS 10_3_2 like Mac OS X) AppleWebKit/603.2.4 (KHTML, like Gecko) Version/10.0 MQQBrowser/7.7.2 Mobile/14F89 Safari/8536.25 MttCustomUA/2 QBWebViewType/1 WKType/1',
            'Mozilla/4.0 (compatible; MSIE 6.0; ) Opera/UCWEB7.0.2.37/28/999'
        ])
    else:
        return random.choice([
            'Mozilla/5.0 (Windows NT 6.1; rv,2.0.1) Gecko/20100101 Firefox/4.0.1',
            'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50',
            'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; 360SE)',
            'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 UBrowser/6.2.4094.1 Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_0) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11',
            'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0;'
        ])


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
            self.session.headers = {
                'Accept': '*/*',
                "User-Agent": get_ua(),
                'Accept-Encoding': 'gzip, deflate, br',
                'Accept-Language': 'zh-CN,zh;q=0.9'
            }
            self.session.cookies = self._request(
                'https://www.baidu.com/').cookies
        elif site == 'mbaidu':
            self.session.headers = {
                'Accept': '*/*',
                "User-Agent": get_ua(True),
                'Accept-Encoding': 'gzip, deflate, br',
                'Accept-Language': 'zh-CN,zh;q=0.9'
            }
            self.session.cookies = self._request(
                'https://m.baidu.com/').cookies
        elif site == 'so':
            self.session.headers = {
                'Accept': '*/*',
                "User-Agent": get_ua(),
                'Accept-Encoding': 'gzip, deflate, br',
                'Accept-Language': 'zh-CN,zh;q=0.9'
            }
            self.session.cookies = cookiejar.CookieJar()

        if PROXY:
            self.session.headers.update({'Proxy-Authorization': made_secret()})

    def _request(self, path):
        if PROXY:
            proxy = self.proxy
        else:
            proxy = None
        retry_count = 5
        while retry_count > 0:
            logger.info(
                f'{threading.currentThread().name} - 开始第次 {6 - retry_count} 尝试'
            )
            try:
                resp = self.session.get(path, proxies=proxy, timeout=(5, 20))
            except Exception as exc:
                retry_count -= 1
                logger.error(
                    f'{threading.currentThread().name} - 错误信息 - {exc}')
            else:
                if resp.status_code == 200:
                    resp.encoding = resp.apparent_encoding
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
            resp.encoding = 'gbk'
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
        logger.info(
            f'{threading.currentThread().name} - 开始处理 {keyword} - {site}')
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
        logger.info(
            f'{threading.currentThread().name} - {keyword} - {site} - {result}'
        )
    MSSQL.update('|'.join(result_str), item[0])

    time.sleep(int(CONFIG.get('Sleep', 'second')))

    return threading.currentThread().name, item[2]


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


def multi_thread(results):

    with ThreadPoolExecutor(
            max_workers=int(CONFIG.get('Process', 'num'))) as executor:
        try:
            for thead, future in executor.map(detail, results, timeout=300):
                logger.info(f'{thead} - {future} - 处理完成')
        except concurrent.futures.TimeoutError:
            logger.info(f'{thead} - {future} - 处理超时')
        except Exception as exc:
            logger.error(f'{thead} - {future} - 处理异常')


def main():
    while True:
        results = MSSQL.select()
        if not results:
            time.sleep(300)
        else:
            # single(results)
            # multi(results)
            multi_thread(results)


CONFIG = ConfigParser()
CONFIG.read('config.ini', encoding='utf-8')
SITES = judge_pages()
MSSQL = Mssql()
PROXY = True if CONFIG.get('Proxy', 'proxy') == '1' else False

if __name__ == "__main__":
    freeze_support()
    main()

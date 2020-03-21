import json
import threading
from urllib import parse
from config import MONGO
from utils.run import run_func
from pymongo import MongoClient
from utils.soup import DealSoup
from utils.request import Query
from utils.log import logger
from concurrent.futures import ThreadPoolExecutor


def clean(content: str):
    return content.replace('.', '').replace('\n', '')


class MongoOpea(object):
    def __init__(self):
        self.init_mongo()
        super().__init__()

    def init_mongo(self):

        config = MONGO["debug"]

        config["user"] = parse.quote_plus(config["user"])
        config["passwd"] = parse.quote_plus(config["passwd"])

        client = MongoClient(
            "mongodb://{user}:{passwd}@{host}:{port}/".format(**config),
            connect=False)

        self.mongo = client["Workoo"]['proff']

    def insert(self, data):
        data = {clean(key): clean(data[key]) for key in data}
        result = self.mongo.insert_one(data)
        return result.inserted_id


def yield_id():
    with open('./data/need_title.json', 'r', encoding='utf-8') as fn:
        data = json.loads(fn.read())

    for _id in data:
        yield _id


class DealProff(object):
    def __init__(self):
        self.req = Query().run
        self.soup = DealSoup().judge
        self.domain = 'https://www.proff.no'
        self.header = {
            'User-Agent':
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.100 Safari/537.36',
            'Accept': '*/*',
            'Referer':
            'https://www.proff.no/laglister?l=Flatanger&samplerFilter=true',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            # Cookie: _ga=GA1.2.1177281469.1582623577; _pa=PA0.9729105361094414; _hjid=8c044dbf-3b78-436b-a609-c63e8f076b6a; __stripe_mid=cdb5b159-cf1b-4ff0-aaab-b0d6d1019f6a; BIGipServerpool-prod-proff-springwebfront-http-80=3450084268.20480.0000; JSESSIONID=430CD11FBC3E58FFB95B94343197BBCE; 3b4385f2546035568001fd05f095cbbd=16a54c5e79d61c0df71a79e57c6f1254; _gid=GA1.2.1689660455.1584760277; _pk_ses.2.dcc0=1; _hjIncludedInSample=1; __stripe_sid=6b99adae-d576-4bff-820f-5672834a14a1; _pk_id.2.dcc0=79d6e7588e7cf8c1.1582623583.5.1584761389.1584760287.; _gat=1
        }
        super().__init__()

    def company_list(self, l=None, page=None):
        if l is None:
            path = f'{self.domain}/laglister/{page}/?view=json'
        else:
            self.category = l
            path = f'https://www.proff.no/laglister?l={self.category}&phone=true&email=true&address=true&view=json'

        resp = run_func(self.req, path, self.header)
        if isinstance(resp, int):
            logger.error(f'{self.category} - {resp}')
            return
        data = json.loads(resp)

        for result in data['createListSearchResult']['resultList']:
            run_func(self.company_detail, result.get('uri'))

        nextpage = data.get('createListSearchResult').get('pagination').get(
            'next')

        if nextpage:
            run_func(self.company_list, page=nextpage.get('href'))

    def company_detail(self, uri):
        info = {}
        info['uri'] = uri
        info['catagory'] = self.category
        # logger.info(f'current - {self.category}')
        resp = self.req(f'{self.domain}{uri}', header=self.header)
        if isinstance(resp, str):
            info['real_uri'] = resp
            if isinstance(resp, int):
                logger.error(f'{self.category} - {resp}')
            resp = self.req(resp, header=self.header)

        contents = self.soup(resp, {'class': 'content definition-list'},
                             all_tag=True)

        for content in contents:
            for li in self.soup(content, 'li', all_tag=True):
                em = self.soup(li, 'em')
                span = self.soup(li, 'span')
                if em and span:
                    info[em.text] = span.text

        result = run_func(mongo.insert, info)
        logger.info(f'已添加 - {result}')

    def run(self, l):
        logger.info(f'{threading.currentThread().name} - 开始 - {l}')

        try:
            self.company_list(l)
        except Exception as exc:
            logger.error(f'1 - {exc}')
        else:
            logger.info(f'已完成 - {self.category}')


def multi_thread():
    with open('./data/need_title.json', 'r', encoding='utf-8') as fn:
        results = json.loads(fn.read())

    with ThreadPoolExecutor(max_workers=5) as executor:
        try:
            for result in executor.map(DealProff().run, results):
                pass
        except Exception as exc:
            print(exc)


def main():
    with open('./data/need_title.json', 'r', encoding='utf-8') as fn:
        results = json.loads(fn.read())

    spider = DealProff()
    for result in results:    
        spider.run(result)


mongo = MongoOpea()

if __name__ == "__main__":
    main()
    # multi_thread()
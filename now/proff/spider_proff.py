import json
import threading
from multiprocessing import freeze_support
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor

from utils.log import logger
from utils.run import run_func
from utils.soup import DealSoup
from utils.request import Query
from utils.mongo import Mongo


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
        }
        super().__init__()

    def company_list(self, l=None, page=None):
        if l is None:
            path = f'{self.domain}/laglister/{page}/?view=json'
        else:
            self.category = l
            path = f'https://www.proff.no/laglister?l={self.category}&phone=false&email=false&address=false&view=json'

        resp = run_func(self.req, path, header=self.header)
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

        result = run_func(Mongo.repeat, info, 'proff')
        logger.info(f'已添加 - {self.category} - {result}')

    def run(self, l):
        name = l.get('name')
        logger.info(f'开始 - {name}')

        try:
            self.company_list(name)
        except Exception as exc:
            logger.error(f'1 - {exc}')
        else:
            logger.info(f'已完成 - {self.category}')
            Mongo.update({'_id': l.get('_id')}, {'status': 1}, 'title')


def multi_thread(results):
    # thead_pool = ProcessPoolExecutor(5)
    thead_pool = ThreadPoolExecutor(20)

    # spider.run(result)

    with ProcessPoolExecutor(max_workers=20) as executor:
        # with ThreadPoolExecutor(max_workers=5) as executor:
        try:
            for result in executor.map(DealProff().run, results):
                pass
        except Exception as exc:
            print(exc)


def single(results):
    spider = DealProff()
    for result in results:
        spider.run(result)


def main():
    results = Mongo.select('title', {'status': 0}, limit=120, _id=False)

    while results:
        multi_thread(results)
        # single(results)

        results = Mongo.select('title', {'status': 0}, limit=120, _id=False)


if __name__ == "__main__":
    freeze_support()
    main()
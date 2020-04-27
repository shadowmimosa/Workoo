import bs4
from urllib import parse
from bson import ObjectId
from bs4 import BeautifulSoup
from datetime import datetime
from pymongo import MongoClient
from config import MONGO, DEBUG


class MongoOpea(object):
    def __init__(self):
        self.init_mongo()
        super().__init__()

    def init_mongo(self):

        config = MONGO['debug']

        config['user'] = parse.quote_plus(config['user'])
        config['passwd'] = parse.quote_plus(config['passwd'])

        client = MongoClient(
            'mongodb://{user}:{passwd}@{host}:{port}/'.format(**config),
            connect=False)

        self.mongo = client[config.get('basedata')]

    def repeat(self, condition, data, table):
        data['created_at'] = datetime.utcnow()
        result = self.mongo[table].update_one(condition, {'$set': data}, True)

        result_id = result.upserted_id
        if not result_id:
            result_id = self.select(table, condition)

        return result_id

    def insert(self, data, table):
        data['created_at'] = datetime.utcnow()
        if isinstance(data, list):
            result = self.mongo[table].insert_many(data)
            return result.inserted_ids
        else:
            result = self.mongo[table].insert_one(data)
            return result.inserted_id

    def select(self, table, query={}, limit=1, _id=True):
        if limit == 1:
            result = self.mongo[table].find_one(query)
            if _id and result:
                return result.get('_id')
            else:
                return result
        else:
            result = self.mongo[table].find(query).limit(limit)
            return list(result)

    def update(self, query, data, table, multi=False):
        data['updated_at'] = datetime.utcnow()
        if not multi:
            result = self.mongo[table].update_one(query, {'$set': data})
            return result.upserted_id
        else:
            result = self.mongo[table].update_many(query, {'$set': data})
            return result.upserted_ids

    def push(self, condition, data, table):
        self.mongo[table].update_one(condition, {'$push': {'resumes': data}})


class DealSoup(object):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def find_tag_by_attr(self):
        if self.all_tag is False:
            return self.soup.find(attrs=self.attr)
        else:
            return self.soup.find_all(attrs=self.attr)

    def find_tag_by_name(self):
        if self.all_tag is False:
            return self.soup.find(self.attr)
        else:
            return self.soup.find_all(self.attr)

    def find_tag(self):
        if isinstance(self.attr, dict):
            return self.find_tag_by_attr()
        elif isinstance(self.attr, str):
            return self.find_tag_by_name()

    def init_soup(self):
        if isinstance(self.content, str):
            self.soup = BeautifulSoup(self.content, 'lxml')
        elif isinstance(self.content, bs4.Tag):
            self.soup = self.content
        elif isinstance(self.content, bs4.BeautifulSoup):
            print('略略略')

    def judge(self, content, attr: dict = None, all_tag: bool = False):
        self.content = content
        self.attr = attr
        self.all_tag = all_tag

        self.init_soup()

        if self.attr is None:
            return self.soup
        else:
            return self.find_tag()


class ParseHtml(object):
    def __init__(self):
        super().__init__()

    def _import(self, html, account=None):
        resume_id = SOUP(html, {'data-nick': 'res_id'}).text
        if not MONGO.select('resumes', {'resume_id': resume_id}):
            basic_info = SOUP(html, {'class': 'resume-basic-info'})
            basics = SOUP(basic_info, 'tr', all_tag=True)
            info = {}
            for basic in basics:
                tds = SOUP(basic, 'td', all_tag=True)
                for td in tds:
                    temp = td.text.replace(' ', '').replace('\n',
                                                            '').split('：')
                    info[temp[0]] = temp[-1]

            info['resume_id'] = resume_id
            info['html'] = html

            MONGO.repeat({'resume_id': resume_id}, info, 'resumes')

        MONGO.push({'account': account}, resume_id, 'user')

    def parse(self, html, account=None):
        resume_id = SOUP(html, {'data-nick': 'res_id'}).text
        basic_info = SOUP(html, {'class': 'resume-basic-info'})
        basics = SOUP(basic_info, 'tr', all_tag=True)
        info = {}
        for basic in basics:
            tds = SOUP(basic, 'td', all_tag=True)
            for td in tds:
                temp = td.text.replace(' ', '').replace('\n', '').split('：')
                info[temp[0]] = temp[-1]

        info['resume_id'] = resume_id
        info['html'] = html
        MONGO.repeat({'resume_id': resume_id}, info, 'public')

        if account and not MONGO.select('user', {
                'account': account,
                'resumes': resume_id
        }):
            return

        data = MONGO.select('resumes', {'resume_id': resume_id}, _id=False)
        if not data:
            return

        create_at = data.get('created_at')
        create_at = datetime.strftime(create_at, '%Y-%m-%d')
        result = {
            'name': data.get('姓名'),
            'sex': data.get('性别'),
            'age': data.get('年龄'),
            'education': data.get('学历'),
            'create_time': create_at,
            'id': str(data.get('_id')),
            'update_time': create_at
        }

        return [result]


def reader_html(_id):
    result = MONGO.select('resumes', {'_id': ObjectId(_id)}, _id=False)
    return result.get('html')


MONGO = MongoOpea()
SOUP = DealSoup().judge
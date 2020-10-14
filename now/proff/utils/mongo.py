from copy import copy
from urllib import parse
from datetime import datetime
import pymongo

from config import MONGO, DEBUG


class MongoOpea(object):
    def __init__(self):
        self.init_mongo()
        super().__init__()

    def init_mongo(self):

        config = MONGO["debug"]

        config["user"] = parse.quote_plus(config["user"])
        config["passwd"] = parse.quote_plus(config["passwd"])

        # client = pymongo.MongoClient(
        #     host=config.get('host'),
        #     port=config.get('port'),
        #     #  username=config.get('user'),
        #     #  password=config.get('passwd'),
        #     connect=False,
        #     maxPoolSize=None)
        # client.admin.authenticate(config.get('user'), config.get('passwd'))
        passwd = 'mongodb://dogyue_dev:aZj2WDyLo%261PkQwg@123.56.175.240:27017/'
        # 'mongodb://dogyue_dev:aZj2WDyLo%25261PkQwg@123.56.175.240:27017/'
        # client = pymongo.MongoClient(
        #     "mongodb://{user}:{passwd}@{host}:{port}/".format(**config),
        #     connect=False)
        client = pymongo.MongoClient(passwd)

        self.mongo = client[config.get('basedata')]
        # print(self.mongo)

    def repeat(self, data, table):
        data = {clean(key): clean(data[key]) for key in data}
        condition = copy(data)
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


def clean(content: str):
    if isinstance(content, str):
        content = content.replace('.', '').replace('\n', '')

    return content


# Mongo = MongoOpea()
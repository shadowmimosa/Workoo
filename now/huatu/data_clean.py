from config import MONGO
from urllib import parse
from bson import ObjectId
from pymongo import MongoClient


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

        self.mongo = client["huatu"]

    def select(self, _id):
        return list(self.mongo['raw_data'].find({
            '_id': {
                '$gt': _id
            }
        }).sort('_id').limit(800))

    def update(self, data):
        self.mongo['current_data'].insert_one(data)


def main():
    results = list(mongo.mongo['raw_data'].find({
        '_id': {
            '$gt': ObjectId('5e693267d7a87657f4e35d89')
        }
    }).sort('_id').limit(800))

    while results:
        for item in results:
            point = item.get('pointList')
            if not point:
                continue
            if point[0]['points'][0] not in [
                    392, 435, 482, 642, 754, 65836, 65877, 65903, 65904, 65905,
                    65902, 66089
            ]:
                continue
            mongo.update(item)

        results = mongo.select(results[-1].get('_id'))


if __name__ == "__main__":
    mongo = MongoOpea()
    main()
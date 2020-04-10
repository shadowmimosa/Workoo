from copy import copy
from utils.mongo import Mongo


def main():
    results = Mongo.select('tjyqhdmhcxhfdm', limit=200)

    while results:
        for result in results:

            year = result.get('year')
            table = f'tjyqhdmhcxhfdm_{year}'
            data = copy(result)
            data.pop('_id')
            Mongo.repeat(data, table)

        results = Mongo.select('tjyqhdmhcxhfdm',
                               {'_id': {
                                   '$gt': result.get('_id')
                               }},
                               limit=200)


if __name__ == "__main__":
    main()
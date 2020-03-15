import csv
import json


def json2csv():
    with open('./covid.json', 'r', encoding='utf-8') as fn:
        data = json.loads(fn.read())


if __name__ == "__main__":
    json2csv()
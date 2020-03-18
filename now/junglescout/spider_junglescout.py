import os
import csv
import json
from configparser import ConfigParser
from urllib.parse import urlencode, quote
from utils.request import Query
from utils.run import run_func
from utils.log import logger

req = Query().run
config = ConfigParser()
config.read('./config/config.txt')
email = config.get('account', 'email')
password = config.get('account', 'password')

header = {
    'Accept': '*',
    'Authorization':
    'Bearer eyJhbGciOiJIUzI1NiJ9.eyJleHAiOjE1ODQ5NjA1NTQsImlhdCI6MTU4NDM1NTc1NCwiaXNzIjoianVuZ2xlc2NvdXRfYXBpIiwiYXVkIjoiY2xpZW50IiwiYXV0aF90b2tlbiI6ImVmNTAzYTAxMzBmN2EwZWYwMWE1MGMzNzBlMjAxYWU2In0.yC0g1PER36U5TW0D6FWnmbbR942QnM28EunbV1vkNCk',
    'User-Agent':
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.100 Safari/537.36',
    'Content-Type': 'application/json',
    # Origin: https://members.junglescout.com
    # 'Referer':
    # 'https://members.junglescout.com/?_ga=2.105128899.1343704030.1584355678-1232530840.1583473519',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'zh-CN,zh;q=0.9'
}
info = []

params = {
    'data[query][type]': 'query',
    'data[query][searchTerm]': 'actinput',
    'data[query][queryFields][]': 'name',
    'data[query][queryFields][]': 'brand',
    'data[query][queryFields][]': 'asin',
    'data[calculatedCategory][type]': 'terms',
    'data[calculatedCategory][valuesArray][]': 'Health & Household',
    'data[calculatedCategory][valuesArray][]': 'Clothing, Shoes & Jewelry',
    'data[calculatedCategory][valuesArray][]': 'Beauty & Personal Care',
    'data[calculatedCategory][valuesArray][]': 'Sports & Outdoors',
    'data[country][type]': 'terms',
    'data[country][valuesArray][]': 'us',
    'data[sort][type]': 'sort',
    'data[sort][column]': 'name',
    'data[sort][direction]': 'asc',
    'data[paginate][type]': 'paginate',
    'data[paginate][pageSize]': '200',
    'data[paginate][from]': 200,
    'data[isUnavailable][type]': 'terms',
    'data[isUnavailable][valuesArray][]': 'false',
    'data[isComplete][type]': 'terms',
    'data[isComplete][valuesArray][]': 'true',
    'data[state][type]': 'terms',
    'data[state][valuesArray][]': 'active',
    'excludeTopBrands': 'false',
}

csv_header = [
    'ASIN', 'Product Name', 'Brand', 'Category', 'Est. Monthly Revenue',
    'Est. Monthly Sales', 'Price', 'Fees', 'Net', 'Rank', 'Reviews', 'LQS',
    'Sellers', 'Buy Box Owner', 'Rating', 'Dimensions', 'Product Tier',
    'Weight'
]


def login():
    # return 'eyJhbGciOiJIUzI1NiJ9.eyJleHAiOjE1ODUwMTE2ODMsImlhdCI6MTU4NDQwNjg4MywiaXNzIjoianVuZ2xlc2NvdXRfYXBpIiwiYXVkIjoiY2xpZW50IiwiYXV0aF90b2tlbiI6IjUyNzMwNDMzNDRkYzQ0MTVmYzc1NWFkMWQ3NDE5MDJkIn0.v26YaT8qiF_4eDwnblIvThLtmwFfiVBGQ1c6eNEcvck'
    path = 'https://api.junglescout.com/users/sign_in'
    local_header = header
    local_header['Authorization'] = 'Bearer'
    data = {"email": email, "password": password}
    resp = req(path, header=local_header, data=data)

    return json.loads(resp).get('data').get('token')


def get_keyword(path):
    need = []
    with open(path, 'r', encoding='utf-8') as fn:
        data = fn.readlines()

    for value in data:
        if value == '\n':
            continue
        need.append(value.replace('\n', ''))

    return need


def save(path, info):
    with open(path, 'w', newline='', encoding='utf-8') as fn:
        f_csv = csv.writer(fn)
        f_csv.writerow(csv_header)
        f_csv.writerows(info)


def detail(item):
    return [
        item.get('asin'),
        item.get('name'),
        item.get('brand'),
        item.get('category'),
        '$' + item.get('estRevenue') if item.get('estRevenue') else 'N.A.',
        item.get('estimatedSales'),
        '$' + item.get('price') if item.get('price') else 'N.A.',
        '$' + item.get('fees') if item.get('fees') else 'N.A.',
        round(eval(item.get('net')), 2) if item.get('net') else 'N.A.',
        format(int(item.get('rank')), ',') if item.get('rank') else 'N.A.',
        item.get('nReviews'),
        int(round(int(item.get('listingQualityScore')), 0))
        if item.get('listingQualityScore') else 'N.A.',
        item.get('nSellers'),
        item.get('sellerName'),
        item.get('rating'),
        f'"{item.get("length")}" x "{item.get("width")}" x "{item.get("height")}"'
        if item.get("length") else 'N.A.',
        item.get('tier'),
        item.get('weight')
    ]


def get_data(token):
    local_header = header
    local_header['Authorization'] = 'Bearer ' + token
    keywords = get_keyword('./config/keywords.txt')
    categories = get_keyword('./config/categories.txt')
    param = '&'.join([
        'data[calculatedCategory][valuesArray][]' + '=' + quote(category)
        for category in categories
    ])
    if not os.path.exists('./data/'):
        os.mkdir('./data/')

    for keyword in keywords:
        info = []
        upper = f'https://api.junglescout.com/api/products/get_products?data[query][type]=query&data[query][searchTerm]={keyword}&data[query][queryFields][]=name&data[query][queryFields][]=brand&data[query][queryFields][]=asin&data[calculatedCategory][type]=terms&'
        for page in range(0, 100):
            count = page * 200
            lower = f'&data[country][type]=terms&data[country][valuesArray][]=us&data[sort][type]=sort&data[sort][column]=name&data[sort][direction]=asc&data[paginate][type]=paginate&data[paginate][pageSize]=200&data[paginate][from]={count}&data[isUnavailable][type]=terms&data[isUnavailable][valuesArray][]=false&data[isComplete][type]=terms&data[isComplete][valuesArray][]=true&data[state][type]=terms&data[state][valuesArray][]=active&skipCounter=true&excludeTopBrands=false'
            path = upper + param + lower
            resp = req(path, header=local_header)
            data = json.loads(resp).get('data').get('data')

            for item in data.get('products'):
                detail_info = run_func(detail, item)
                if detail_info:
                    info.append(detail_info)
                    logger.info(f'已添加 - {detail_info}')

            if data.get('total_count') < count:
                try:
                    save(f'./data/{keyword}.csv', info)
                except Exception as exc:
                    logger.error(f'保存错误 - {exc}')
                else:
                    logger.info(f'保存成功 - {keyword}')
                finally:
                    break


def spider():
    try:
        token = login()
    except Exception as exc:
        logger.info(f'登录失败 - {exc}')
    else:
        logger.info(f'登录成功')
        try:
            get_data(token)
        except Exception as exc:
            logger.info(f'Somethng wrong - {exc}')

    input('按任意键退出')


if __name__ == "__main__":
    os.chdir(os.path.abspath(os.path.dirname(__file__)))
    spider()
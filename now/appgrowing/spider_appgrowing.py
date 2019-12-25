import json, time
import datetime
from bson import ObjectId

from utils.run import run_func
from utils.request import Query
from utils.soup import DealSoup
from config import DEBUG, logger, mongo, get_cookie


def clean_json():
    new_data = []

    with open('./data/categroy.json', 'r', encoding='utf-8') as fn:
        data = json.loads(fn.read())

    init = -1
    init_ = -1
    for value in data:
        if value['parentId'] == 0:
            new_data.append(value)
            init += 1
        elif 99 < value['parentId'] < 999:
            if new_data[init].get('categroy') is None:
                new_data[init]['categroy'] = []
            new_data[init]['categroy'].append(value)
            init_ += 1
        else:
            try:
                new_data[init]['categroy'][init_]
            except IndexError:
                init_ = 0
            if new_data[init]['categroy'][init_].get('categroy') is None:
                new_data[init]['categroy'][init_]['categroy'] = []
            new_data[init]['categroy'][init_]['categroy'].append(value)

    with open('./data.json', 'w', encoding='utf-8') as fn:
        fn.write(json.dumps(new_data))


def magic_time():
    second = mongo['cookie'].find_one(
        {'_id': ObjectId('5e03287f913800005e007d28')})['waiting']
    time.sleep(second)


def get_id():
    with open('./data/categroy.json', 'r', encoding='utf-8') as fn:
        data = json.loads(fn.read())

    new_data = []

    for value in data:
        if value['id'] > 99999:
            new_data.append(value)

    for value in new_data:
        yield value


def get_link(code):
    path = f'{host}/api/leaflet/detail?id={code}&page=1&limit=1'

    resp = req(path, header=header)
    data = json.loads(resp)

    return data['data'][0]['finalLink']


def phone_in_link(path):
    if 'jinritemai' in path:
        # 'https://ec.snssdk.com/product/lubanajaxstaticitem?id={}&token=75e3ed2998ec50c5213a4e6dee9e648b&page_id=&b_type_new=0'
        path = 'https://ec.snssdk.com/product/lubanajaxstaticitem?id={}&page_id=&b_type_new=0'.format(
            path.split('=')[-1])
        resp = req(path, header_snssdk)
        data = json.loads(resp)
        phone = data['data'].get('mobile')
        second_phone = data['data'].get('second_mobile')
        phones = []
        if phone:
            phones.append(phone)
        if second_phone:
            phones.append(second_phone)
        return phones
    elif 'fyeds' in path:
        header_fyeds['Host'] = path.split('/')[2]
        resp = req(path, header=header_fyeds)
        contact = soup(resp, attr={'id': 'contact_tel'})
        if contact:
            return [contact['href'].replace('tel:', '')]
        else:
            return []
    else:
        logger.error('the detail link is {}'.format(path))
        return


def judge_repeat(code):
    result = mongo["appgrowing"].find({'companyId': code})

    if len(list(result)) < 1:
        return True


def get_phones(company_id):
    path = f'{host}/api/sellerCompany?sellerCompanyId={company_id}'
    resp = req(path, header=header)
    data = json.loads(resp)

    return data['data']['telephone']


def leaflet_list(category, page):

    channel = 102
    startDate = '2019-11-26'
    endDate = '2019-12-25'
    order = '-updatedAt'
    isExact = 'false'
    limit = 60

    path = f'{host}/api/leaflet/mt?category={category}&channel={channel}&startDate={startDate}&endDate={endDate}&order={order}&isExact={isExact}&page={page}&limit={limit}'

    resp = req(path, header=header)

    data = run_func(json.loads, resp)

    if data['m'] == 'ok':
        for value in data['data']:
            code = value['id']
            company_id = value['sellerCompany']['id']
            company_name = value['sellerCompany']['name']

            if not judge_repeat(company_id):
                logger.info(f'---> the {company_id} exist already')
                continue

            link = run_func(get_link, code)

            magic_time()
            phones = run_func(get_phones, company_id)
            magic_time()
            phone_detail = run_func(phone_in_link, link)

            mongo["appgrowing"].insert_many([{
                'code':
                code,
                'category':
                category,
                'page':
                page,
                'companyId':
                company_id,
                'companyName':
                company_name,
                'link':
                link,
                'phones':
                phones,
                'phoneDetail':
                phone_detail,
                'addTime':
                datetime.datetime.utcnow()
            }])
            logger.debug(phones, link, phone_detail)
        return data['total']
    else:
        logger.error('the message is {}'.format(data))


def main():
    yield_id = get_id()
    while True:
        try:
            categroy = next(yield_id)['id']
        except StopIteration:
            break
        else:
            for page in range(1, 167):
                total = run_func(leaflet_list, categroy, page)
                if total and total / 60 > page:
                    continue
                else:
                    break
            time.sleep(2)


req = Query().run
soup = DealSoup().judge
host = 'https://ds.appgrowing.cn'
header = {
    'Host': 'ds.appgrowing.cn',
    'Accept': 'application/json, text/plain, */*',
    'User-Agent':
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36',
    'Sec-Fetch-Site': 'same-origin',
    'Sec-Fetch-Mode': 'cors',
    # 'Referer':
    # 'https://ds.appgrowing.cn/leaflet?category=1210101&channel=102&startDate=2019-06-25&endDate=2019-12-21&order=-updatedAt&isExact=false&page=1',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Cookie': get_cookie()
}
header_fyeds = {
    'Host': 'd9650aad.fyeds6.com',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent':
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.79 Safari/537.36',
    'Accept':
    'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'Sec-Fetch-Site': 'none',
    'Sec-Fetch-Mode': 'navigate',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'zh-CN,zh;q=0.9'
}
header_snssdk = {
    'Host': 'ec.snssdk.com',
    'Accept': 'application/json, text/plain, */*',
    'Origin': 'https://haohuo.jinritemai.com',
    'User-Agent':
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.79 Safari/537.36',
    'Sec-Fetch-Site': 'cross-site',
    'Sec-Fetch-Mode': 'cors',
    'Referer':
    'https://haohuo.jinritemai.com/views/product/item?id=3375241637788821075',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'zh-CN,zh;q=0.9'
}

if __name__ == "__main__":
    # clean_json()
    main()
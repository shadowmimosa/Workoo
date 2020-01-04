import re
import json
import time

from utils.run import run_func
from utils.request import Query
from utils.soup import DealSoup
from config import DEBUG, logger


def get_phones(company_id):
    path = f'{host}/api/sellerCompany?sellerCompanyId={company_id}'
    resp = req(path, header=header)
    data = json.loads(resp)

    return data['data']['telephone']


def leaflet_list(category, page):

    channel = 102
    startDate = '2019-11-30'
    endDate = '2019-12-29'
    order = '-updatedAt'
    isExact = 'false'
    limit = 60

    path = f'{host}/api/leaflet/mt?category={category}&channel={channel}&startDate={startDate}&endDate={endDate}&order={order}&isExact={isExact}&page={page}&limit={limit}'

    resp = req(path, header=header)

    data = run_func(json.loads, resp)


def main():
    path = 'https://www.nike.com/cn/w/mens-shoes-nik1zy7ok'
    resp = req(path, header=header)
    pattern = re.compile(r'window.INITIAL_REDUX_STATE=.*</script>')
    a = re.search(resp, pattern)
    html = soup(resp)
    print(html)


req = Query().run
soup = DealSoup().judge
host = 'https://www.nike.com'

header = {
    'Host': 'www.nike.com',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent':
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36',
    'Accept':
    'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'Sec-Fetch-Site': 'none',
    'Sec-Fetch-Mode': 'navigate',
    # 'Referer': '',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    # 'Cookie': get_cookie()
}

if __name__ == "__main__":
    main()
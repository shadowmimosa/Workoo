import time
import math
import random
from loguru import logger
from utils import soup, request, mongo

HEADER = {
    'Host':
    'quote.eastmoney.com',
    'Accept':
    'application/json, text/javascript, */*; q=0.01',
    'User-Agent':
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36',
    'Referer':
    'http://quote.eastmoney.com/zixuan/?from=home',
    'Accept-Encoding':
    'gzip, deflate',
    'Accept-Language':
    'zh-CN,zh;q=0.9',
    'Cookie':
    'qgqp_b_id=d3e909d530154657027020e640c0f62d; isoutside=0; st_si=97596402581527; st_asi=delete; em-quote-version=topspeed; waptgshowtime=202072; p_origin=https%3A%2F%2Fpassport2.eastmoney.com; ct=Lji-d7SXVqQbKLjWbcIANTTbmyv1Tp4LKGV905T0a-loHnCXpUjCh-sxhoFa8PJDVyYdnpMm329Gq_4rVRbP7f0uHUAN4uH3D0xOg7lAFmfIU0x5PyACBiaockZu_bapC5V0xVDjXd7wY1P3aPuteWRYd82uOFAzm4zkzIawGJ0; ut=FobyicMgeV6Gl5Ws0rOH5siJGM5kyGokE0OSnwizZOvF5_YD_1cwbyeoCKwNimV2-KH0ssCPBek4CFIykisx5clOD5gxzV6pPBf5Jll7WzC9YhVchN7Gt1Fm_0YF3NjHVEv0L3fO6WzdtE-hYjyCtuYB_qzmPEkip7blafirEXkfAxSkFBqDzqrjV1CJFqM86UeDKarlY1Gc6PK9QrH8rV8x5yUFPr5aAUZudStYY98EaRBHFVMM-XbhFSf7AkDjx2PQIKR8Zwh1FKdlEPo7uQFn2JO9-wfp; pi=9541055275247638%3bz9541055275247638%3b%e5%b0%8f%e4%b8%83%e5%a2%a8%e5%a2%a8%3bCZSfhs2h7%2bj7PNXo08zs1izQPVlecmpoT9vlYcC4JukUJMkYj%2fFrq75FiY7ll1rHDyfsgtiKNt4HpJrCvWYXjnPTfHJMoQ8RthWe0EG6Lb%2bKhrDT0Yn9dgDy5Ll3yGnogNa2pD0RfpbnZYTRXao5nP9Rb4u51BusYsUYrtohbJh%2bM%2fSh01cmLDtEWbYUDYEJABAmNghW%3bzZEnl%2bgT3SLCKJmTUzP9u%2fXThF5fJtILA1gZeOZnxREbd%2f7KOuBMKJme2%2b1wcv3lP8apSA1uD9piaEAXG7IyhsO435ElyK5%2bKxYtsLpPBvEmQIB2QV%2b09U7cKym2g7g3yWNNVuLjXKveFlmojodSTIGAZD7aEw%3d%3d; uidal=9541055275247638%e5%b0%8f%e4%b8%83%e5%a2%a8%e5%a2%a8; sid=124926045; vtpst=|; HAList=a-sh-600688-%u4E0A%u6D77%u77F3%u5316%2Ca-sz-002828-%u8D1D%u80AF%u80FD%u6E90; st_pvi=20684234639942; st_sp=2019-12-06%2014%3A41%3A52; st_inirUrl=http%3A%2F%2Fguba.eastmoney.com%2F; st_sn=20; st_psi=20200702225619411-113200301712-9818133675'
}
HEADER_NO_COOKIE = {
    'Host': 'emweb.securities.eastmoney.com',
    'User-Agent':
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36',
    'Accept':
    'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'zh-CN,zh;q=0.9'
}


def get_group_info():
    with open('./raw/home.html', 'r', encoding='utf-8') as fn:
        html = fn.read()

    groups_obj = soup(html, {'class': 'populd lia noshow'}, True)

    groups = [{
        'groupid': x.get('data-groupid'),
        'groupname': x.get('data-groupname')
    } for x in groups_obj]

    for index, group in enumerate(groups):
        stocks = get_stock_by_groupid(group['groupid'])
        stocks_info = []
        for stock in stocks:
            stock_info = get_stock_info_by_stockid(stock)
            stocks_info.append(stock_info)
            logger.info(f'add one - {stock}')
        groups[index].update({'stock_info': stocks_info})

    mongo.insert(groups, 'eastmoney_7_3')


def get_stock_by_groupid(groupid):
    timestamps = int(time.time() * 1000)
    rnd = math.floor(random.random() * 10000000 + 1)
    uri = f'http://quote.eastmoney.com/zixuan/api/zxg/getstockbygroupid/{groupid}?rnd={rnd}&_={timestamps}'
    data = request(uri, HEADER, json=True)
    codes = [x.replace('1.', 'sh').replace('0.', 'sz') for x in data['result']]
    return codes

    # codestr = '\n'.join(data['result']).replace('1.', 'sh').replace('0.', 'sz')


def company_survey(stockid):
    # uri = f'http://emweb.securities.eastmoney.com/CompanySurvey/Index?type=web&code={stockid}'
    uri = f'http://emweb.securities.eastmoney.com/CompanySurvey/CompanySurveyAjax?code={stockid}'

    data = request(uri, HEADER_NO_COOKIE, json=True)
    return data


def core_conception(stockid):
    # uri = f'http://emweb.securities.eastmoney.com/CoreConception/Index?type=web&code={stockid}'
    uri = f'http://emweb.securities.eastmoney.com/CoreConception/CoreConceptionAjax?code={stockid}'

    data = request(uri, HEADER_NO_COOKIE, json=True)
    return data


def business_analysis(stockid):
    # uri = f'http://emweb.securities.eastmoney.com/BusinessAnalysis/Index?type=web&code={stockid}'
    uri = f'http://emweb.securities.eastmoney.com/BusinessAnalysis/BusinessAnalysisAjax?code={stockid}'

    data = request(uri, HEADER_NO_COOKIE, json=True)
    return data


def get_stock_info_by_stockid(stockid):
    info = {}
    info['company_survey'] = company_survey(stockid)
    info['core_conception'] = core_conception(stockid)
    info['business_analysis'] = business_analysis(stockid)

    return info


if __name__ == "__main__":
    get_group_info()
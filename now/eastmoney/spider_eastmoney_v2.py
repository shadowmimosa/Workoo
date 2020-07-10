import time
import math
import random
from pathlib import Path
from loguru import logger
from utils import soup, request, mongo

HEADER_NO_COOKIE = {
    'Host': 'emweb.securities.eastmoney.com',
    'User-Agent':
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36',
    'Accept':
    'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'zh-CN,zh;q=0.9'
}


def main():
    for page in range(1, 205):
        timestamps = int(time.time() * 1000)
        uri = f'http://36.push2.eastmoney.com/api/qt/clist/get?pn={page}&pz=20&po=1&np=1&ut=bd1d9ddb04089700cf9c27f6f7426281&fltt=2&invt=2&fid=f3&fs=m:0+t:6,m:0+t:13,m:0+t:80,m:1+t:2,m:1+t:23&fields=f12,f13&_={timestamps}'
        data = request(uri, HEADER_NO_COOKIE,
                       json=True).get('data').get('diff')

        for company in data:
            stockid = get_real_stockid(company.get('f12'), company.get('f13'))
            stock_info = get_stock_info_by_stockid(stockid)
            mongo.insert(stock_info, 'eastmoney_7_10')


def get_real_stockid(code, sign):

    return f'sh{code}' if sign == 1 else f'sz{code}'

    codes = [x.replace('1.', 'sh').replace('0.', 'sz') for x in data['result']]
    uri = f'http://quote.eastmoney.com/unify/r/{sign}.{code}'
    real_uri = request(uri, HEADER_NO_COOKIE, redirect=False)
    stockid = Path(real_uri).stem
    return stockid


def company_survey(stockid):
    uri = f'http://emweb.securities.eastmoney.com/CompanySurvey/CompanySurveyAjax?code={stockid}'

    data = request(uri, HEADER_NO_COOKIE, json=True)
    return data


def core_conception(stockid):
    uri = f'http://emweb.securities.eastmoney.com/CoreConception/CoreConceptionAjax?code={stockid}'

    data = request(uri, HEADER_NO_COOKIE, json=True)
    return data


def business_analysis(stockid):
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
    main()
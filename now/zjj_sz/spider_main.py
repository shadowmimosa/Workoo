import os
import json
import time
import datetime

import hashlib
from config import AUTH, SALT, FIXED, APP
from utils import logger, run_func, request, excel, mysql, soup

excel.init_sheet(header=[
    '项目楼栋情况', '座号', '合同号', '拟售价格', '楼层', '房号', '用途', '预售查丈-建筑面积', '预售查丈-户内面积',
    '预售查丈-分摊面积', '竣工查丈-户内面积', '竣工查丈-分摊面积', '竣工查丈-建筑面积'
])

header = {
    'appId': '2',
    'currentVersion': '12.0.0',
    'customerId': '51275736',
    'clientId': '23544d12-5c5c-47f5-8cb7-d6577f66370e',
    'apiVersion': '1',
    'appCode': '1',
    'clientType': 'CONSUMER',
    'signature': '2a62aebba4c3153aba71c83cb2f98043',
    'appTime': '2020-03-15T15:28:47.561+0800',
    'Accept-Encoding': 'gzip',
    'User-Agent': 'okhttp/3.7.0'
}

city: '深圳'
city_id: '607'
interval = 2
HEADER = {
    'Host': 'zjj.sz.gov.cn',
    'User-Agent':
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36',
    'Accept':
    'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'Referer': 'http://zjj.sz.gov.cn:8004/commonSkipAspx/fdcProjectInfo.html',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'zh-CN,zh;q=0.9',
}


def unit_price(total, area):
    try:
        price = int(total) / int(area)
    except Exception:
        logger.warning(f'Calculate Price is Error - {total} - {area}')
    else:
        return round(price, 3)


def to_excel(data: dict):
    if not data:
        return
    info = {}
    info['楼盘名称'] = data.get('houseName')
    info['板块'] = data.get('districtPlateName')
    info['楼号'] = data.get('building')
    info['楼层'] = data.get('floorTag')
    info['面积'] = data.get('bargainArea')
    info['网签价格'] = data.get('dealTag').get('dealOrEvalSinPrice')
    info['复原价格'] = data.get('evalTag').get('dealOrEvalSinPrice')
    info['合同价格(万)'] = data.get('contractRealPrice')
    info['单价(万元/m²)'] = unit_price(info['合同价格(万)'], info['面积'])
    info['成交时间'] = data.get('dealTime')

    excel.write(info)
    try:
        sql = 'INSERT INTO `backstage`.`2boss`(`楼盘名称`, `板块`, `楼号`, `楼层`, `面积`, `网签价格`, `复原价格`, `合同价格`, `单价`, `成交时间`) VALUES ("{楼盘名称}", "{板块}", "{楼号}", "{楼层}", "{面积}", "{网签价格}", "{复原价格}", "{合同价格(万)}", "{单价(万元/m²)}", "{成交时间}");'.format(
            **info)
        mysql.execute(sql)
    except Exception as exc:
        pass
    message = json.dumps(info, ensure_ascii=False).replace('²', '2')
    logger.info(f'已插入 - {message}')


def remove(content: str):
    return content.replace('\r',
                           '').replace('\n',
                                       '').replace(' ',
                                                   '').replace('\xa0', '')


def get_data():
    url = 'http://zjj.sz.gov.cn/ris/bol/szfdc/index.aspx'

    resp = request(url, header=HEADER)
    data = {}
    data['__VIEWSTATEGENERATOR'] = soup(resp, {
        'name': '__VIEWSTATEGENERATOR'
    }).get('value')
    data['__VIEWSTATEENCRYPTED'] = soup(resp, {
        'name': '__VIEWSTATEENCRYPTED'
    }).get('value')
    data['__EVENTVALIDATION'] = soup(resp, {
        'name': '__EVENTVALIDATION'
    }).get('value')

    data['__EVENTTARGET'] = soup(resp, {'name': '__EVENTTARGET'}).get('value')
    data['__EVENTARGUMENT'] = soup(resp, {
        'name': '__EVENTARGUMENT'
    }).get('value')
    data['__LASTFOCUS'] = soup(resp, {'name': '__LASTFOCUS'}).get('value')
    data['__VIEWSTATE'] = soup(resp, {'name': '__VIEWSTATE'}).get('value')

    return data


def house_detail(href):
    resp = request(href, header=HEADER)
    table = soup(resp, {'class': 'table ta-c table2 table-white'})

    info = {}
    sign = ''
    for tr in soup(table, 'tr', 1):
        tds = soup(tr, 'td', 1)
        if not tds:
            sign = remove(tr.h3.text)

        for td in tds[::2]:
            if sign:
                key = f'{sign}-{remove(td.text)}'
            else:
                key = remove(td.text)
            info[key] = remove(tds[tds.index(td) + 1].text)

    print(info)


def building(href):
    resp = request(href, header=HEADER)
    
    table = soup(resp, {'class': 'table ta-c table2'})

    for tr in soup(table, 'tr', 1):
        for child in tr.contents:
            if child.name != 'td':
                continue
            a = child.a
            if not a:
                continue
            href = a.get('href')
            if not href:
                continue

            house_detail(href)


def project_detail(href):
    resp = request(href, header=HEADER)
    table = soup(resp, {'class': 'table ta-c table2 table-white'}, 1)[-1]

    for tr in soup(table, 'tr', 1)[1:]:
        tds = soup(tr, 'td', 1)
        href = tds[-1].a.get('href')
        building(href)


def serch_keyword(keyword):
    result = get_data()  # dict
    url = 'http://zjj.sz.gov.cn/ris/bol/szfdc/index.aspx'
    header = {
        'Host': 'zjj.sz.gov.cn',
        'Origin': 'http://zjj.sz.gov.cn',
        'Content-Type': 'application/x-www-form-urlencoded',
        'User-Agent':
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36',
        'Accept':
        'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Referer': 'http://zjj.sz.gov.cn/ris/bol/szfdc/index.aspx',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        # 'Cookie':
        # 'cookie_3.36_8080=85416329; insert_cookie=40523543; ASP.NET_SessionId=du3hn055gouxgei2skvahk45; zlpt-session-id_test=ac7cfbef-19ae-43ba-8b68-64c444f4cae4'
    }
    data = {
        '__EVENTTARGET': result.get('__EVENTTARGET'),
        '__EVENTARGUMENT': result.get('__EVENTARGUMENT'),
        '__LASTFOCUS': result.get('__LASTFOCUS'),
        '__VIEWSTATE': result.get('__VIEWSTATE'),
        '__VIEWSTATEGENERATOR': result.get('__VIEWSTATEGENERATOR'),
        '__VIEWSTATEENCRYPTED': result.get('__VIEWSTATEENCRYPTED'),
        '__EVENTVALIDATION': result.get('__EVENTVALIDATION'),
        'tep_name': keyword,
        'organ_name': '',
        'site_address': '',
        'Button1': '查询',
        'ddlPageCount': '10'
    }

    resp = request(url, header=header)
    table = soup(resp, {'class': 'table ta-c bor-b-1 table-white'})
    trs = soup(table, 'tr', 1)
    tds = soup(trs[1], 'td', 1)
    href = tds[2].a.get('href')

    project_detail(href)


def get_keyword():
    need = []
    with open('./houses.txt', 'r', encoding='utf-8') as fn:
        keywords = fn.readlines()

    for keyword in keywords:
        need.append(keyword.replace('\n', ''))

    return need


def encrypt(app=APP, timestamp=int(time.time() * 1000), fixed=FIXED):
    text = f'?auth={AUTH}&app={app}&timestamp={timestamp}&fixed={fixed}'
    md5 = hashlib.md5(SALT)
    md5.update(text.encode('utf-8'))
    secret = md5.hexdigest().lower()

    return f'{text.replace("auth=shadowmimosa&","")}&token={secret}'


class MagicError(Exception):
    def __init__(self, *args):
        self.args = args


def magic():
    path = f'http://auth.bigbe.cn/workoo/auth{encrypt()}'
    result = request(path, json=True, redirect=True)
    if result.get('code') != 200:
        raise MagicError('Something Wrong')


def spider():
    for keyword in get_keyword():
        for house in serch_keyword(keyword):
            run_func(get_prices, house)
            time.sleep(interval)
    try:
        name = excel.save()
    except Exception as exc:
        logger.error(f'保存失败 - {exc}')
    else:
        logger.info(f'保存成功 - {name}')


if __name__ == "__main__":
    magic()
    spider()
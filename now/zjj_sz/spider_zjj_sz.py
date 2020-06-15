import os
import json
import time
import datetime
import hashlib
from copy import copy
from urllib.parse import urlparse, parse_qs, urlencode
from config import AUTH, SALT, FIXED, APP
from utils import logger, run_func, request, excel, soup, mongo

excel.init_sheet(header=[
    '楼盘名称', '现售/预售', '项目楼栋情况', '座号', '合同号', '拟售价格', '楼层', '房号', '用途',
    '预售查丈-建筑面积', '预售查丈-户内面积', '预售查丈-分摊面积', '竣工查丈-户内面积', '竣工查丈-分摊面积',
    '竣工查丈-建筑面积'
])

info = {}
count = 0
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


def form_data(html):
    form_html = soup(html, {'id': 'Form1'})
    return form_html.get('action')

    form_data = {}
    form_data['__EVENTTARGET'] = soup(form_html, {
        'id': '__EVENTTARGET'
    }).get('value')
    form_data['__EVENTARGUMENT'] = soup(form_html, {
        'id': '__EVENTARGUMENT'
    }).get('value')
    form_data['__VIEWSTATE'] = soup(form_html, {
        'id': '__VIEWSTATE'
    }).get('value')

    return form_data


def house_detail(href):
    global info, count
    mongo_info = copy(info)

    resp = request(href, header=HEADER)
    table = soup(resp, {'class': 'table ta-c table2 table-white'})

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
            mongo_info[key] = remove(tds[tds.index(td) + 1].text).replace(
                '元/平方米(按建筑面积计)', '').replace('平方米', '')

    excel.write(info)
    mongo.insert(mongo_info, 'zjj_sz_data')
    count += 1
    print(f'已采集 {count} 条')


def building(href):
    global info

    resp = request(href, header=HEADER)
    branches = soup(resp, {'id': 'divShowBranch'})
    branches = soup(branches, 'a', 1)
    # href = form_data(resp)
    # building.aspx?id=36123&presellid=44453&Branch=A&isBlock=xs
    # params = urlparse(href)
    # for building_type in ['imgBt1', 'imgBt2']:
    for branch in branches:
        href = branch.get('href')
        params = parse_qs(urlparse(href).query)
        for key in params:
            params[key] = params[key][0]

        for block_name, block in [('预售', 'ys'), ('现售', 'xs')]:
            info['现售/预售'] = block_name
            params['isBlock'] = block
            href = f'building.aspx?{urlencode(params)}'
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
    global info

    info = {}

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

    resp = request(url, header=header, data=urlencode(data))
    table = soup(resp, {'class': 'table ta-c bor-b-1 table-white'})
    trs = soup(table, 'tr', 1)
    tds = soup(trs[1], 'td', 1)
    href = tds[2].a.get('href')

    info['楼盘名称'] = keyword

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
        serch_keyword(keyword)

    try:
        name = excel.save()
    except Exception as exc:
        logger.error(f'保存失败 - {exc}')
    else:
        logger.info(f'保存成功 - {name}')

    input('按任意键退出')


if __name__ == "__main__":
    magic()
    spider()
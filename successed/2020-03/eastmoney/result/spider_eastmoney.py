import json
import codecs
import pandas
import requests

from fontTools.ttLib import TTFont

path = 'http://dcfm.eastmoney.com/em_mutisvcexpandinterface/api/js/get'
headers = {
    'Accept':
    '*/*',
    'Accept-Encoding':
    'gzip, deflate',
    'Accept-Language':
    'zh-CN,zh;q=0.9',
    'Referer':
    'http://data.eastmoney.com/bbsj/201812/yjbb.html',
    'User-Agent':
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'
}
font_header = {
    'User-Agent':
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.100 Safari/537.36',
    'Accept': '*/*',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Referer': 'http://data.eastmoney.com/bbsj/201812/yjbb.html',
}
params = {
    'type': 'YJBB21_YJBB',
    'token': '70f12f2f4f091e459a279469fe49eca5',
    'st': 'latestnoticedate',
    'sr': '-1',
    'p': '1',
    'ps': '50',
    'js': 'var IUahecdO={pages:(tp),data: (x),font:(font)}',
    'filter':
    "(securitytypecode in ('058001001','058001002'))(reportdate=^2019-09-30^)",
    'rt': '52789127'
}


def deal_font(font):
    resp = requests.get(font['WoffUrl'], headers=font_header, timeout=30)

    font_name = './font/{}'.format(font['WoffUrl'].split("/")[-1])
    with codecs.open(font_name, 'wb') as fn:
        fn.write(resp.content)

    font_map = TTFont(font_name).getBestCmap()
    font_index = [
        hex(key).upper().replace('0X', '&#x') + ';' for key in font_map.keys()
    ]
    font_mapping = font['FontMapping']

    return {i['code']: str(i['value']) for i in font_mapping}


def get_data(page):
    session = requests.session()
    session.keep_alive = False
    session.verify = False

    params['p'] = str(page)

    resp = session.post(path, data=params, headers=headers)

    raw = resp.text[resp.text.index("{"):]
    json_str = raw.replace('data:', '"data":').replace('pages:',
                                                       '"pages":').replace(
                                                           'font:', '"font":')
    data = json.loads(json_str)
    font = deal_font(data['font'])

    for key, value in font.items():
        json_str = json_str.replace(key, value)

    return json.loads(json_str)


def spider():
    info = pandas.DataFrame(columns=[
        '序号', '股票代码', '股票简称', '每股收益(元)', '营业收入', '季度同比增长(%)', '季度环比增长(%)',
        '净利润(元)', '净利润同比增长(%)', '净利润季度环比增长(%)', '每股净资产(元)', '净资产收益率(%)',
        '每股经营现金流量(元)', '销售毛利率(%)', '利润分配', '所处行业', '最新公告日期'
    ])
    index = 0
    
    for page in range(1, 79):
        data = get_data(page)

        for item in data['data']:
            index += 1
            info = info.append(
                {
                    '序号': index,
                    '股票代码': item['scode'],
                    '股票简称': item['sname'],
                    '每股收益(元)': item['basiceps'],
                    '营业收入': item['totaloperatereve'],
                    '季度同比增长(%)': item['ystz'],
                    '季度环比增长(%)': item['yshz'],
                    '净利润(元)': item['parentnetprofit'],
                    '净利润同比增长(%)': item['sjltz'],
                    '净利润季度环比增长(%)': item['sjlhz'],
                    '每股净资产(元)': item['bps'],
                    '净资产收益率(%)': item['roeweighted'],
                    '每股经营现金流量(元)': item['mgjyxjje'],
                    '销售毛利率(%)': item['xsmll'],
                    '利润分配': item['gxl'],
                    '所处行业': item['publishname'],
                    '最新公告日期': item['latestnoticedate'].split('T')[0]
                },
                ignore_index=True)

    info.to_excel('./data.xlsx', index=False)


if __name__ == "__main__":
    spider()
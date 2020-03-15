import os
import json
import time
import datetime
from config import init_sql
from utils.log import logger
from utils.run import run_func
from utils.request import Query
from utils.excel_opea import ExcelOpea

req = Query().run
excel = ExcelOpea()
mysql = init_sql()
excel.init_sheet(header=[
    '楼盘名称', '板块', '楼号', '楼层', '面积', '网签价格', '复原价格', '合同价格(万)', '单价(万元/m²)',
    '成交时间'
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


def deal_head():
    local_header = header
    current = datetime.datetime.utcnow().strftime(
        '%Y-%m-%dT%H:%M:%S.%f')[:-3] + '+0800'

    local_header['appTime'] = current

    return local_header


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


def serch_keyword(keyword):
    position = []
    path = f'https://ta.2boss.cn/rabbit/v1/customer/house/fuzzyMach?showFirstHouse=true&showStations=false&showSchool=false&isFirst=2&cityId={city_id}&keyword={keyword}'
    resp = req(path, header=deal_head())
    data = json.loads(resp)

    for item in data['body']:
        position.append({'name': item.get('name'), 'id': item.get('targetId')})

    return position


def get_prices(house):
    for page in range(1, 100):
        # page = 100
        path = f'https://ta.2boss.cn/rabbit/v1/deal/searchDeal?isFirst=2&keyword={house.get("name")}&pageSize=30&city={city}&targetId={house.get("id")}&geoType=baidu&page={page}&lat=28.003469&type=3&lng=110.574832&tabType=1&cityId={city_id}'
        resp = run_func(req, path, header=deal_head())
        data = run_func(json.loads, resp)
        # if data['body']['houseInfo'] is None:
        #     break
        if not len(data['body']['houseList']):
            break

        for item in data['body']['houseList']:
            run_func(to_excel, item)


def get_keyword():
    need = []
    with open('./houses.txt', 'r', encoding='utf-8') as fn:
        keywords = fn.readlines()

    for keyword in keywords:
        need.append(keyword.replace('\n', ''))

    return need


def send_verify(mobile):
    path = f'https://ta.2boss.cn/rabbit/v1/app/login/send-verifycode?mobile={mobile}&usefulness=LOGIN'
    # If-Modified-Since: Sun, 08 Mar 2020 10:58:46 GMT
    resp = run_func(req, path, header=deal_head())
    data = json.loads(resp)
    if data.get('resultCode') == 0:
        # if data['body'].get('success') == 'true':
        logger.info('验证码发送成功')
        return True
    else:
        logger.info(f'验证码发送失败 - {data.get("errMsg")}')


def login(mobile, verify_code):
    path = 'https://ta.2boss.cn/rabbit/v1/app/login/login-by-verifycode'
    header = deal_head()
    header['Content-Type'] = 'application/json; charset=UTF-8'
    data = {"mobile": mobile, "code": verify_code}
    resp = run_func(req, path, header=header, data=data)
    data = json.loads(resp)
    try:
        result = data.get('body').get('authorization').get('accessToken')
    except Exception as exc:
        logger.info(f'登录错误 - {exc}')
    else:
        return result


def init():
    global header, city, city_id, interval

    with open('./config.txt', 'r', encoding='utf-8') as fn:
        config = json.loads(fn.read())
    try:
        interval = int(config.get('interval'))
    except Exception:
        logger.info('interval 错误, 请检查')
        return
    city = config.get('city')
    city_id = config.get('city_id')

    sign = input('是否重新登录? 1.是 2.否 (默认否, 回车确认): ')
    if not sign:
        sign = 2
    try:
        sign = int(sign)
    except Exception:
        logger.info('输入错误请检查')
        return
    else:
        if sign == 1:
            if send_verify(config.get('mobile')) is True:
                verify_code = input('请输入验证码: ')
                result = login(config.get('mobile'), verify_code)
                if not result:
                    return
                header['TBSAccessToken'] = result
                config['token'] = result
                with open('./config.txt', 'w', encoding='utf-8') as fn:
                    fn.write(json.dumps(config, ensure_ascii=False, indent=4))
                return True
            else:
                return
        elif sign == 2:
            header['TBSAccessToken'] = config.get('token')
            return True
        else:
            logger.info('输入错误请检查')
            return


class BaseError(Exception):
    def __init__(self, *args):
        self.args = args


def magic():
    if int(time.time()) > 1612336109:
        raise BaseError('Something Wrong')


def spider():
    result = init()
    if not result:
        input('按任意键退出')
    else:
        # keyword = '万达丰大厦'
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
import os
import re
import json
import time
import random
import urllib
from config import logger
from utils.run import run_func
from utils.request import Query
from utils.excel_opea import ExcelOpea


def judge():

    if int(time.time()) > 1610780831:
        raise TimeoutError


def random_param():
    return random.choice(param)


def deal_property(content):
    result = {}
    for item in content:
        if item['name'] == '品牌':
            result['品牌'] = item['value']
        elif item['name'] == '进口/国产' or item['name'] == '是否进口':
            result['进口/国产'] = item['value']
        elif item['name'] == '包装方式':
            result['包装方式'] = item['value']
        elif item['name'] == '保存条件':
            result['保存条件'] = item['value']
        elif item['name'] == '净重':
            result['净重'] = item['value']
        elif item['name'] == '储存条件':
            result['储存条件'] = item['value']
        elif item['name'] == '产地':
            result['产地'] = item['value']

    return result


def limit(content):
    if len(content) == 0:
        return None
    else:
        for item in content:
            if '限购' in item['tagTitle']:
                return 2
            # elif '促销' in item['tagTitle']:
            else:
                return 1


def get_pic(code):
    path = f'https://fnyx.feiniu.com/commodity/detail/json/{code}.json'

    header = {
        'Host': 'fnyx.feiniu.com',
        'Accept': 'application/json, text/plain, */*',
        'Origin': 'https://fnyx.feiniu.com',
        'User-Agent':
        'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.116 Safari/537.36 QBCore/4.0.1295.400 QQBrowser/9.0.2524.400 Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2875.116 Safari/537.36',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Referer':
        f'https://fnyx.feiniu.com/commodity/detail/content/{code}.shtml',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.6,en;q=0.5;q=0.4',
    }

    resp = req(path,
               header=header,
               data=f'detailType=youxian&commodityKey={code}')
    result = json.loads(resp)
    pics = ''
    for item in result['body']:
        if item['type'] == 'fmdesc-module-product-pic':
            for pic in item['data']['images']:
                pics = ', '.join((pics, pic.replace('//', '')))
            return pics.strip(', ')


def detail(code):
    global count
    path = 'https://yx.feiniu.com/www-yxapp/goods/detail/t126'
    data = raw_data
    data['body'] = {"goodsNo": code, "storeCode": store}
    param = urllib.parse.quote(json.dumps(data))
    sign = random_param()
    resp = req(path,
               header=header,
               data=f'data={param}&h5=yx_touch&paramsMD5={sign}')
    result = json.loads(resp)
    product = result['body']['productDetail']
    property_ = deal_property(product['property'])
    info = {
        '商品编号': product['goodsNo'],
        '名称': product['itName'],
        '一级分类': first,
        '二级分类': second,
        '三级分类': third,
        '售价': product['sm_price'],
        '参考价': product.get('originPrice'),
        # '折扣': item['corners'].get('desc'),
        '销量': product['it_saleqty'],
        # '销售单位': '{}/{}'.format(property_['净重'], property_['包装方式']),specDesc
        '销售单位': product.get('specDesc'),
        # '库存': product['sale_unit'],
        # '库存单位': product['unit'],
        '展示单位': product['unit'],
        # '特价': product['subtitle'],
        '简介': product['sellingPoint'],
        '品牌': property_.get('品牌'),
        '产地': property_.get('产地'),
        '重量': product.get('priceUnit'),
        '净含量': property_.get('净重'),
        '储存条件': property_.get('保存条件'),
        '详情图': get_pic(code),
        '运费政策': product['freight'],
        # '所属商户': store,
        '采集时间': time.strftime("%Y-%m-%d %H-%M-%S", time.localtime()),
        '配货ID': product['commodityNum'],
        '促销限购': limit(result['body']['campList']),
        '保质期': result['elapsedTime'],
        # '采集标注': '',
    }
    if info['参考价'] is None:
        info['参考价'] = info['售价']
    if info['产地'] is None:
        info['产地'] = property_.get('进口/国产')
    if len(product['sm_pic_list']) >= 2:
        info['主图1'] = product['sm_pic_list'][0]
        info['主图2'] = product['sm_pic_list'][1]
    elif len(product['sm_pic_list']) >= 1:
        info['主图1'] = product['sm_pic_list'][0]
        info['主图2'] = '',
    else:
        info['主图1'] = '',
        info['主图2'] = '',
    # if info['净含量'] is None:
    #     num = re.search(patter, info['名称'])
    #     if num:
    #         info['净含量'] = num.group()

    excel.write(info)
    count += 1
    if count % 10 == 0:
        print(f'爬取商品数据--{count}条')

    # print('{} - {} - {}'.format(first, second, info['名称']))


def categoty_search(code):
    for page in range(1, 250):
        path = 'https://yx.feiniu.com/search-yxapp/categorySearch/searchByCategory/t126'
        data = raw_data
        data['body'] = {
            "store_id": store,
            "one_page_size": 10,
            "si_seq": code,
            "cp_seq": "",
            "level": 2,
            "page_index": page,
            "type": 21,
            "gcSeq": ""
        }
        param = urllib.parse.quote(json.dumps(data))
        resp = req(path, header=header, data=f'data={param}&h5=yx_touch')
        result = json.loads(resp)
        for item in result['body']['MerchandiseList']:
            sm_seq = item['sm_seq']
            run_func(detail, sm_seq)
        # total = result['body']['total']
        pages = result['body'].get('totalPageCount')
        if pages:
            if page >= pages:
                break
        else:
            logger.error(f'Keyerror - {result}')
            time.sleep(60)


def third_category(code):
    global third
    path = 'https://yx.feiniu.com/www-yxapp/category/childCategory/t126'
    data = raw_data
    data['body'] = {"categorySeq": code, "type": "1", "storeCode": store}
    param = urllib.parse.quote(json.dumps(data))
    resp = req(path, header=header, data=f'data={param}&h5=yx_touch')
    result = json.loads(resp)
    for item in result['body']['categoryTree']:
        code = item['categorySeq']
        second = item['categoryName']
        run_func(categoty_search, code)


def second_category(code):
    global second, third
    path = 'https://yx.feiniu.com/www-yxapp/category/childCategory/t126'
    data = raw_data
    data['body'] = {"categorySeq": code, "type": "1", "storeCode": store}
    param = urllib.parse.quote(json.dumps(data))
    resp = req(path, header=header, data=f'data={param}&h5=yx_touch')
    result = json.loads(resp)
    for item in result['body']['categoryTree']:
        child = item.get('child')
        if len(child) == 0:
            third = ''
            code = item['categorySeq']
            second = item['categoryName']
            run_func(categoty_search, code)
        else:
            for child_ in child:
                code = child_['categorySeq']
                second = item['categoryName']
                third = child_['categoryName']
                run_func(categoty_search, code)


def first_category():
    global first
    path = 'https://yx.feiniu.com/www-yxapp/category/firstCategory/t126'
    data = raw_data
    data['body'] = {"storeCode": store, "versionNo": ""}
    param = urllib.parse.quote(json.dumps(data))
    resp = req(path, header=header, data=f'data={param}&h5=yx_touch')
    result = json.loads(resp)
    for item in result['body']['categoryTree']:
        code = item['categorySeq']
        first = item['categoryName']
        if first in category:
            run_func(second_category, code)
        else:
            continue


def main():
    global store, raw_data, category
    try:
        with open('./config.txt', 'r', encoding='utf-8') as fn:
            config = json.loads(fn.read())
    except:
        logger.error('config.txt 错误')
        time.sleep(300)
        return
    try:
        with open('category.txt', 'r', encoding='utf-8') as fn:
            category = json.loads(fn.read())
    except:
        logger.error('category.txt 错误')
        time.sleep(300)
        return

    store = '1055'
    raw_data['time'] = int(time.time())
    raw_data['areaCode'] = config['areaCode']
    raw_data['storeCode'] = config['storeCode']
    raw_data['clientid'] = config['clientid']
    raw_data['device_id'] = config['device_id']
    raw_data['token'] = config['token']

    excel.init_sheet(header=[
        '商品编号',
        '名称',
        '一级分类',
        '二级分类',
        '三级分类',
        '售价',
        '参考价',
        # '折扣',
        '销量',
        '销售单位',
        # '库存',
        # '库存单位',
        '展示单位',
        # '特价',
        '简介',
        '品牌',
        '产地',
        '重量',
        '净含量',
        '储存条件',
        '主图1',
        '主图2',
        '详情图',
        '运费政策',
        # '所属商户',
        '采集时间',
        '配货ID',
        '促销限购',
        '保质期',
        # '采集标注',
    ])

    run_func(first_category)
    excel.save()


raw_data = 'skuId={}&skuLocation=2&supplierId=2'
store = '1047'
category = []
first = ''
second = ''
third = ''
count = 0
patter = re.compile(r'[1-9]\d*')
header = {
    'Host': 'yx.feiniu.com',
    'Content-Type': 'application/x-www-form-urlencoded',
    'Referer':
    'https://servicewechat.com/wx08cc6bd15fabfa53/27/page-frame.html',
    'User-Agent': '',
    # 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36',
    'Accept-Encoding': 'gzip, deflate, br',
}
param = [
    'yIHjbz/dQ0ftQmI/Sm2yZU7W5cJusrpcbrydvvX1hTI=',
    'l5ipPoHXLkBDLCAhsSwr+iNXKdXUovSasp0MhpxgJhQ=',
    'LPAoobhO2+IjH13VkVZ1UL4Gl8Nz3btxhP3JPKuLX1E=',
    'L7ZMCYZ+9mzWnn/o9G+FgwzQMt/rZ87it8UzFolWUxI=',
    'buHLNjeJByQOZM5m5xM1K2ZhXonKYGmkQj47R5nWEzc=',
    'OeDCFIy7b8/EEJuu317LHQ++6E6qXyYpUiHmX7d04Pc=',
    '7FzjXIK3BER+fzJIYthD7Lm4GhG7f/SkHu+VF51l4jM=',
    'XwGIK0aszBNVO3XVWSJ+vgREsvTOk1BnVHsudOygZAw=',
    'ihYztTNNl3QKRR8f/UaUMWbJhjR+DhjU/CJkoUrJIjg=',
    'HytLmB9kj4mypU8iH+OOMlnzyrdXHiXQ81EfFcvi4Ko=',
    'hOsbFsTovH9MCF9JwxnpgsqjFoOcWFYBiajwolDurY0=',
    'xQJ43+dGFzrsIaUiU/jgqBjsKwFqT/cnwLSiSUljxkg=',
    'u+4/eM7tq0Z0UoqaVBvoi49zgaZRufVH/36lZan3dew=',
    'hdtZSUmC/1VrCKu2tHYU2SekfpeOr33OuFvOtScutAk=',
    'PchNY4oqHNv489asA8ec2NJJ00+FxNTPiIQogq/BXz4=',
    'lnAIW74BMBW+El3wRdav1ViCIa0cx2Ay+ppiT0XSj88=',
    'ADQiNbUuZGrvqb6dupoMB1IxwhJNpLUhdP/Z27BqB68=',
    'ofqNgD1HeYzvNMW+lIvVd6GhfGlwzzE7AhK2MZeqzKM=',
    'lhiZEWl6GwVINuiAmcnFFTf6h3w7r0MPvp2lz0zEB28=',
    '+0NeA77Ss3wTImFFX3j6hsnek8kPSo1awwoCco7DTUk=',
    'Kzr5GIfNVSwB+pBgq0iW6WBjhzfbllgBS/9byrkjSEs=',
    'MLx2xzn3xPMlh3cszhEDVFfS9bLFWk9AqVECmGqO/gY=',
    '9g8ysszvH9zoswskKtnOwE7W21QoowoSyscFYZZHEzk=',
    'pDapIknwsgXcUWMAAASze9nnrAc4fNB+lv1vm86N32U=',
    'kwX3WYtywbKfuaXnwnubGnHFOIQ63pzwveih7D7O19c=',
    'Cfmazzid4X9gcJndoZ0yKb1a9j2P56lSt7MUI69kW80=',
    'niJMmU8IkVtjtYsqN5kQXLbqdYDZIbcehEZ56u+3Wq4=',
    'rWDqOnnpYKLxqXfPEBvdDo1KASKw4V5az2US/LAntEg=',
    'F6XErEclyXY3PGakziBeW50zrmDpQCecEacrQDaw1CU=',
    'wS0dhM+FN7opvw9gaPNG57qhoSfLwajG8eNfLd5FVjw=',
    'UwcVAeLelOqg/AvOieytDYinRqArPccxMSTVfQxDlt4=',
    'XiWrd5kNCNg1grHtEkLf2VEJUnMLAH7z93JDt31IoDo=',
    '7mRGMQcSyh5Tl4k3d887A6Ywq26nNYobAX/xx6jxBzo=',
    'f6CwJ4VIxks7M6Iik28KVy4MIiXs/GeD5GxuizUd1Hk=',
    'bdHuZ4bU8+Din3GyITjSyyOjSibUUduw/IrDqi1oSno=',
    'XP9RpA5wGTlDac3srXJDJsgVRQEMEUXd5ByAckdQTmI=',
    'URFwG0/jRwSxpAKWvrvcML/8/Gvk7WDenfmvnrfzaWU=',
    'ycpuea2es693bncrD9BCX2kT0GBKMoJAemT97/UDlSU=',
    '35J0ynaPi8eWLvcCowTAvYQYqRIa9MyqC+YNRj92cS0=',
    '6gVdQeTytMnLdTTXmST3rUsf/wYN+fb3p2VrvM/90KI=',
    'rs3JmDcfiETJboyrTfOhsBAs1FQom+BZsym+gXyfzu0=',
    'LJqoHp13zHhB7fksvmExD3RpOqosl/g1U4uDxyjAgq8=',
    'Id6HBvqqbQDq5cY8i6EYMGOEw7UzLjc1vmjmxB9JMhE=',
    'HQeLlMqsoWK2bHq+X9s0pj74/OBnjyc8boIlt08Q8ys=',
    'ErXbvNQbFVQbTJZPUKbcuW0PlwVJbterMe6KnD3FDxA=',
    'VbOJIOgfdo0rOVORCQIxtKOF+hmKAdPmKJURqZ3iOnk=',
    'DO+RXVN3FT+ScRaWEL5xYHcG9Ulac0SNU9gCkyAZmEc=',
    'RSSfWkiX5ATExUE3YgyghGW7GFtu2qMc9bgSC76aWXY=',
    '77gpIdCXqZ1O9aK5nvFdL8XPqfMNT0ve1XUXI2e2Bvw=',
    'dDEBSGDULlgxRpejqiWL8CUW2c7idyDClPwFQocY5Ng=',
]
req = Query().run
excel = ExcelOpea()
raw_data = {
    "apiVersion": "t126",
    "appVersion": "1.0.0",
    "channel": "market",
    "reRule": "4",
    "view_size": "720x1184",
    "osType": "4",
    "scopeType": 2,
    "businessType": 1
}

if __name__ == "__main__":
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    judge()
    try:
        main()
    except Exception as exc:
        logger.error(exc)

    # asyncio.run(main())

    # try:
    #     asyncio.run(main())
    # except Exception as exc:
    #     print('Error')
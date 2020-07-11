import re
import os
import pathlib
from utils import mongo, excel
from number2chinese import number2chinese


def company_survey(details: dict):
    header = [
        '股票代码', '股票名称', '公司名称', '公司简介', '经营范围', '员工人数', '办公地址', '网址', '联系电话',
        '总经理', '法人代表', '董事长', '注册地址'
    ]
    excel.init_sheet(header, '公司概况')
    base = details.get('jbzl')

    info = {
        '股票代码': details.get('SecurityCode'),
        '股票名称': details.get('SecurityShortName'),
        '公司名称': base.get('gsmc'),
        '公司简介': base.get('gsjj'),
        '经营范围': base.get('jyfw'),
        '员工人数': base.get('gyrs'),
        '办公地址': base.get('bgdz'),
        '网址': base.get('gswz'),
        '联系电话': base.get('lxdh'),
        '总经理': base.get('zjl'),
        '法人代表': base.get('frdb'),
        '董事长': base.get('dsz'),
        '注册地址': base.get('zcdz')
    }

    excel.write(info, '公司概况')


def core_conception(details: dict):
    header = ['核心题材']
    excel.init_sheet(header, '核心题材')

    info_lines = details.get('hxtc')
    info = []
    for index, line in enumerate(info_lines):
        string = f'要点{number2chinese(index+1)}:{line.get("gjc")} {line.get("ydnr")}'
        info.append(string)
        excel.write([string], '核心题材')

    # info = '\n'.join(info)
    # excel.write(info, '核心题材')


def business_analysis(details: dict):
    header = [
        '日期', '分类', '主营构成', '主营收入(元)', '收入比例', '主营成本(元)', '成本比例', '主营利润(元)',
        '利润比例', '毛利率(%)'
    ]
    excel.init_sheet(header, '经营分析')

    analysis_data = details.get('zygcfx')
    info = []
    for date_data in analysis_data:
        date = date_data.get('rq')

        for product in date_data.get('hy'):
            info.append({
                '日期': product.get('rq'),
                '分类': '按行业分类',
                '主营构成': product.get('zygc'),
                '主营收入(元)': product.get('zysr'),
                '收入比例': product.get('srbl'),
                '主营成本(元)': product.get('zycb'),
                '成本比例': product.get('cbbl'),
                '主营利润(元)': product.get('zylr'),
                '利润比例': product.get('lrbl'),
                '毛利率(%)': product.get('mll'),
            })
        for product in date_data.get('cp'):
            info.append({
                '日期': product.get('rq'),
                '分类': '按产品分类',
                '主营构成': product.get('zygc'),
                '主营收入(元)': product.get('zysr'),
                '收入比例': product.get('srbl'),
                '主营成本(元)': product.get('zycb'),
                '成本比例': product.get('cbbl'),
                '主营利润(元)': product.get('zylr'),
                '利润比例': product.get('lrbl'),
                '毛利率(%)': product.get('mll'),
            })
        for product in date_data.get('qy'):
            info.append({
                '日期': product.get('rq'),
                '分类': '按地区分类',
                '主营构成': product.get('zygc'),
                '主营收入(元)': product.get('zysr'),
                '收入比例': product.get('srbl'),
                '主营成本(元)': product.get('zycb'),
                '成本比例': product.get('cbbl'),
                '主营利润(元)': product.get('zylr'),
                '利润比例': product.get('lrbl'),
                '毛利率(%)': product.get('mll'),
            })

    excel.write_many(info, '经营分析')


def main():
    count = 0
    result = mongo.select('eastmoney_7_10', _id=False, limit=1000)
    # import json
    # with open('./demo.json', 'r', encoding='utf-8') as fn:
    #     result = json.loads(fn.read())

    while result:
        for stock in result:
            excel.__init__()
            dirpath = f'data/'

            path = f'{dirpath}/{stock.get("company_survey").get("SecurityShortName")}.xlsx'
            if pathlib.Path(path).is_file():
                print(stock.get('_id'))

            business_analysis(stock['business_analysis'])
            core_conception(stock['core_conception'])
            company_survey(stock['company_survey'])

            excel.save(path)
            count += 1
            
        print(count)
        result = mongo.select('eastmoney_7_10', {'_id': {
            '$gt': stock['_id']
        }},
                              limit=1000,
                              _id=False)


if __name__ == "__main__":
    main()

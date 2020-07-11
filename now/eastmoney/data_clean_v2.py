import re
import os
import cpca
from utils import mongo, excel


def company_survey(details: dict):
    base = details.get('jbzl')

    info = {
        '股票代码': details.get('SecurityCode'),
        '股票名称': details.get('SecurityShortName'),
        '公司名称': base.get('gsmc'),
        '注册地址': base.get('zcdz')
    }
    return info
    excel.write(info, '公司概况')


def core_conception(details: dict):
    info_lines = details.get('hxtc')

    length = len(info_lines)

    if length >= 4:
        return {
            '要点三':
            f'要点三:{info_lines[2].get("gjc")} {info_lines[2].get("ydnr")}',
            '要点四':
            f'要点四:{info_lines[3].get("gjc")} {info_lines[3].get("ydnr")}'
        }
    elif length == 3:
        return {
            '要点三':
            f'要点三:{info_lines[2].get("gjc")} {info_lines[2].get("ydnr")}',
            '要点四':
            f'要点四:{info_lines[3].get("gjc")} {info_lines[3].get("ydnr")}'
        }
    else:
        return {'要点三': None, '要点四': None}


def extract_region(address):
    result = cpca.transform([address], open_warning=False, cut=False)
    
    return


def main():
    count = 0
    header = ['股票代码', '股票名称', '公司名称', '省', '市', '注册地址', '要点三', '要点四']
    excel.init_sheet(header, 'sheet')
    result = mongo.select('eastmoney_7_10', _id=False)

    while result:
        for stock in result:
            info = {}
            path = f'data/汇总.xlsx'

            info.update(core_conception(stock['core_conception']))
            info.update(company_survey(stock['company_survey']))

            info.update(extract_region(info.get('注册地址')))

            excel.save(path)
            count += 1

        print(count)
        result = mongo.select('eastmoney_7_10',
                              {'_id': {
                                  '$gt': result['_id']
                              }},
                              _id=False)


if __name__ == "__main__":
    main()

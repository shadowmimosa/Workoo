import re
import os
import json
import time
import pymysql
from config import DATABASES, DEBUG

try:
    if DEBUG:
        config = DATABASES["debug"]
    else:
        config = DATABASES["product"]

    ecnu_mysql = pymysql.connect(**config)

except pymysql.err.OperationalError as exc:
    print('登录失败！TimeoutError!')
    os._exit(0)
else:
    ecnu_cursor = ecnu_mysql.cursor()


def judge(text):
    sql = f'SELECT `id` FROM `workoo`.`xianyu` WHERE `商品介绍` = "{text}" LIMIT 1;'
    if ecnu_cursor.execute(sql) == 0:
        return True
    else:
        return


def to_sql(info):
    sql = 'INSERT INTO `workoo`.`xianyu`(`昵称`, `登录时间`, `发布地`, `原价`, `现价`, `服务`, `商品介绍`, `想要`, `超赞`, `浏览`, `个人简介`, `实人认证`, `芝麻信用`, `留言个数`, `留言`, `添加时间`) VALUES ("{昵称}", "{登录时间}", "{发布地}", "{原价}", "{现价}", "{服务}", "{商品介绍}", "{想要}", "{超赞}", "{浏览}", "{个人简介}", "{实人认证}", "{芝麻信用}", "{留言个数}", "{留言}", "{添加时间}");'
    for key in info:
        if isinstance(info[key], str):
            info[key] = pymysql.escape_string(info[key])
    sql = sql.format(**info)
    if not judge(info['商品介绍']):
        return
    try:
        ecnu_cursor.execute(sql)
    except Exception as exc:
        print(exc)


def clean(data: dict):
    info = {}
    temp = data.get('个人信息').split('\n')
    info['昵称'] = temp[0]
    info['登录时间'] = temp[-1].split(' ')[0]
    info['发布地'] = temp[-1].split(' ')[-1].replace('发布于', '')

    temp = data.get('售价')
    if '原价' in temp:
        info['原价'] = temp.split(' ')[0].replace('原价', '')
        info['现价'] = temp.split(' ')[1].replace('现价', '')
    elif '现价' in temp:
        info['原价'] = ''
        info['现价'] = temp.split(' ')[0].replace('现价', '')

    if data.get('商品介绍2') is None or data.get('商品介绍2') == '宝贝图片0':
        info['服务'] = None
        info['商品介绍'] = data.get('商品介绍')
    else:
        info['服务'] = data.get('商品介绍')
        info['商品介绍'] = data.get('商品介绍2')

    info['添加时间'] = time.strftime('%Y-%m-%d %X',
                                 time.localtime(data.get('添加时间')))

    patterns = {
        '想要': '([0-9]\d*)人想要',
        '超赞': '超赞([0-9]\d*)',
        '浏览': '浏览([0-9]\d*)'
    }
    temp = data.get('人数')
    for key in patterns:
        if temp is None:
            info[key] = 0
            continue
        result = re.search(patterns[key], temp)
        if result:
            info[key] = result.group(1)
        else:
            info[key] = 0

    temp = data.get('个人简介')
    if temp is None:
        info['个人简介'] = ''
        info['实人认证'] = ''
        info['芝麻信用'] = ''
        print('person wrong')
    else:
        temp = temp.split('\n')
        if temp[0] != info['昵称']:
            if '...' not in info['昵称']:
                print('wrong {}'.format(json.dumps(temp, ensure_ascii=False)))
                info['昵称'] = temp[0]
                # return
            elif info['昵称'].replace('...', '') in temp[0]:
                info['昵称'] = temp[0]
            else:
                print('wrong {}'.format(json.dumps(temp, ensure_ascii=False)))
                return
        info['个人简介'] = temp[1]
        info['实人认证'] = temp[2]
        info['芝麻信用'] = temp[3]
    temp = data.get('留言个数')
    if temp is None:
        info['留言个数'] = ''
    else:
        temp = data.get('留言个数').replace('全部留言',
                                        '').replace('·', '').replace(' ', '')
        info['留言个数'] = temp if temp else 0
    info['留言'] = []
    for item in data.get('留言'):
        if isinstance(item, list):
            for sub_item in item:
                if isinstance(sub_item, dict):
                    for key in sub_item:
                        temp = sub_item[key].split('\n')
                        if key == 'null':
                            key = info.get('昵称')
                        string = f'{key} - {temp[0]} - {temp[-1]}'
                        info['留言'].append(string)
                else:
                    # print('2')
                    # print(sub_item)
                    pass
            pass
        elif isinstance(item, dict):
            for key in item:
                if '回复@' in key:
                    temp = key.split('\n')
                    text = temp[0].split(':')[-1]
                    string = f'回复 - {text} - {temp[-1]}'
                    info['留言'].append(string)
                else:
                    # print('3')
                    # print(item)
                    pass
        else:
            # print('1')
            # print(item)
            pass
    to_sql(info)


def main():
    with open('./data_2.txt', 'r', encoding='utf-8') as fn:
        data_list = fn.readlines()

    data_list = [json.loads(x) for x in data_list]

    # count = []
    # for data in data_list:
    #     if data['个人信息'] not in count:
    #         count.append(data['个人信息'])
    for data in data_list:
        clean(data)


if __name__ == "__main__":
    main()

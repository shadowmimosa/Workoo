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


def txt2json(lines: list):
    data = []
    for line in lines:
        line = line.lstrip('\n')
        if not line:
            continue

        temp = json.loads(line)
        if isinstance(temp[3], list):
            if None in temp[3]:
                temp[3].remove(None)

            temp[3] = '\n'.join(temp[3])

        data.append([temp[0], temp[1], temp[2], temp[3]])

    return data


def is_repeat(data, shop):
    sql = f'SELECT * FROM `workoo`.`hema` WHERE `店铺` = "{shop}" ORDER BY `id` DESC LIMIT 0,2;'
    ecnu_cursor.execute(sql)
    result = ecnu_cursor.fetchall()

    for item in result:
        if data[0] in item and data[1] in item and data[2] in item and data[
                3] in item:
            return True


def to_sql(param, shop):
    sql = 'INSERT INTO `workoo`.`hema`(`昵称`, `满意度`, `评价`, `时间`, `店铺`) VALUES ("{}", "{}", "{}", "{}", "{}");'
    ecnu_cursor.execute(
        sql.format(param[0], param[1], param[3], param[2], shop))


def main():

    for name in ['9_2']:
        if name in [1, 2]:
            continue

        with open('./{}.txt'.format(name), 'r', encoding='utf-8') as fn:
            result = txt2json(fn.readlines())

        for item in result:
            if is_repeat(item, name):
                continue
            to_sql(item, name)

    # with open('9_1.txt', 'r', encoding='utf-8') as fn:
    #     data_1 = fn.readlines()
    # with open('9_2.txt', 'r', encoding='utf-8') as fn:
    #     data_2 = fn.readlines()

    # count = 0
    # for data in data_1:
    #     if data not in data_2:
    #         count += 1
    #         print(data)


if __name__ == "__main__":
    main()

# import os
from os.path import *
from os import chdir, mkdir, listdir
from datetime import datetime, timedelta
from re import compile, search, findall, S
# import re
import xlwt
import time


class DealRecord(object):
    def __init__(self):
        self.dirpath = "./data/"
        self.record_path = join(self.dirpath, "聊天记录/")
        self.info_path = join(self.dirpath, "结果/")
        self.ending_path = join(self.dirpath, "话术/")
        self.keyword_path = join(self.dirpath, "关键字/")

        self.header = [
            '客服ID',
            '客户ID',
            '回复时间（秒）',
            '包含行业关键字',
            '有无结尾话术',
            '手机号',
            '手机号所在记录',
            # '聊天记录'
        ]
        # self.phone_pattern = compile(r'\d{3}-\d{8}|\d{4}-\{7,8}')
        self.phone_pattern = compile(r'^1[34578]\d{9}')

        self.init_path()
        self.init_sheet()

    def init_path(self):
        try:
            mkdir(self.dirpath)
        except FileExistsError:
            pass

        try:
            mkdir(self.record_path)
        except FileExistsError:
            pass

        try:
            mkdir(self.ending_path)
        except FileExistsError:
            pass

        try:
            mkdir(self.info_path)
        except FileExistsError:
            pass

        try:
            mkdir(self.keyword_path)
        except FileExistsError:
            pass

    def init_sheet(self):
        self.wkb = xlwt.Workbook()
        self.sheet = self.wkb.add_sheet('sheet1', cell_overwrite_ok=True)
        self.row = 0
        self.write(self.header)

    def save(self):

        self.wkb.save('{}{}.xlsx'.format(self.info_path, int(time.time())))

    def write(self, content: list or dict):
        if isinstance(content, list):
            for index, value in enumerate(content):
                self.sheet.write(self.row, index, value)
        elif isinstance(content, dict):
            for index, value in enumerate(self.header):
                try:
                    need_write = content[value]
                except KeyError:
                    need_write = ''
                self.sheet.write(self.row, index, need_write)

        self.row += 1

    def deal_text(self, content: list):
        time_pattern = compile(
            r'([0-9]{3}[1-9]|[0-9]{2}[1-9][0-9]{1}|[0-9]{1}[1-9][0-9]{2}|[1-9][0-9]{3})-(((0[13578]|1[02])-(0[1-9]|[12][0-9]|3[01]))|((0[469]|11)-(0[1-9]|[12][0-9]|30))|(02-(0[1-9]|[1][0-9]|2[0-8]))) (0[0-9]|1[0-9]|2[0-3]):([0-5][0-9]):([0-5][0-9])'
        )
        record_data = {}
        for item in content:
            if '----------------------------' in item:
                customer = item.replace('----------------------------', '')
                record_data.update({customer: []})
                temp_record = ''
            else:
                sign = search(time_pattern, item)

                if sign:
                    if len(temp_record) == 0:
                        record_data[customer].append(item)
                    else:
                        record_data[customer][-1] = '{}{}'.format(
                            record_data[customer][-1], temp_record)
                        record_data[customer].append(item)
                        temp_record = ''
                else:
                    temp_record = '\n'.join((temp_record, item))

        for record in record_data:
            for index, text in enumerate(record_data[record]):
                temp = text.split('):  ')
                record_data[record][index] = {'text': temp[-1]}
                temp = temp[0].split('(')
                record_data[record][index]['person'] = temp[0]
                record_data[record][index]['time'] = temp[-1].replace(')', '')

        return record_data

    def filter_customer(self, content: list):
        for item in content:
            for text_list in item:
                for text in text_list:
                    for keyword in trade_keyword:
                        if keyword in text['text']:
                            return True

    def ending_skill(self, content):
        # for item in reversed(content):

        if content['person'] != self.staff:
            self.info['有无结尾话术'] = '无'
        else:
            if content['text'] not in self.ending_list:
                self.info['有无结尾话术'] = '无'
            else:
                self.info['有无结尾话术'] = '有'

    def deal_keyword(self, content: str):
        exist_list = []
        raw = self.info.get('包含行业关键字')

        if raw is None:
            raw_list = []
        else:
            raw_list = raw.split('\n')

        for keyword in self.keyword_list:
            if keyword in content:
                exist_list.append(keyword)

        exist_list.extend(raw_list)

        if len(exist_list) > 0:
            self.info['包含行业关键字'] = '\n'.join(set(exist_list))

    def get_phone(self, content):
        phone_obj = search(self.phone_pattern, content)

        if phone_obj:
            self.info['手机号'] = phone_obj.group()
            self.info['手机号所在记录'] = content
        else:
            self.info['手机号'] = '无'
            self.info['手机号所在记录'] = '无'

    def deal_time(self, content: list):
        sign = 0
        record_time = None
        for item in content:
            if item['person'] == self.staff:
                if sign == 0 and record_time is not None:
                    time_diff = str2time(item['time']) - record_time
                    time_temp = self.info.get('回复时间（秒）')

                    if time_temp:
                        if time_diff.total_seconds() > time_temp.total_seconds(
                        ):
                            self.info['回复时间（秒）'] = time_diff
                    else:
                        self.info['回复时间（秒）'] = time_diff

                    print(convert_timedelta(time_diff))
                sign = 1
            elif item['person'] == self.info['客户ID']:
                record_time = str2time(item['time'])

                self.deal_keyword(item['text'])
                # self.get_phone('15044120331')
                self.get_phone(item['text'])

                sign = 0

        self.info['回复时间（秒）'] = convert_timedelta(self.info['回复时间（秒）'])

        if self.info.get('包含行业关键字') is None:
            self.info['包含行业关键字'] = '无'

    def extract_record(self, path):
        with open(path, 'r', encoding='gbk') as fn:
            self.staff = fn.readline().replace('\n', '')
            content = fn.read()

        text = findall(r'={64}.*?={64}(.*?)={64}', content,
                       S)[0].strip('\n').split('\n')
        # text1 = re.search(r'={64}[\n\s\r]*(.*)[\n\s\r]*={64}', content)

        text_list = self.deal_text(text)

        for key, value in text_list.items():
            self.info = {}
            self.info['客服ID'] = self.staff
            self.info['客户ID'] = key
            self.ending_skill(value[-1])

            self.deal_time(value)

            self.write(self.info)
        self.save()
        print(text_list)

    def main(self):
        with open(
                '{}结尾话术.txt'.format(self.ending_path), 'r',
                encoding='gbk') as fn:
            self.ending_list = fn.readline().replace('\n', '')

        with open(
                '{}行业关键字.txt'.format(self.keyword_path), 'r',
                encoding='gbk') as fn:
            self.trade_list = fn.read().split('\n')

        with open(
                '{}包含关键字列表.txt'.format(self.keyword_path), 'r',
                encoding='utf-8') as fn:
            self.keyword_list = fn.read().split('\n')

        for filename in listdir(self.record_path):
            self.extract_record(join(self.record_path, filename))


def filter_record(content: str):
    for text in content.split('\n'):
        for line in open('过滤关键字列表.txt', 'r', encoding='utf-8').readlines():
            if '\n' == line:
                continue
            if line.strip('\n').decode('utf-8-sig').encode('gbk') in text:
                content = content.replace(text, '')
    return content


def str2time(string: str):
    return datetime.strptime(string, '%Y-%m-%d %H:%M:%S')


def convert_timedelta(duration: timedelta):
    days, seconds = duration.days, duration.seconds
    hours = days * 24 + seconds // 3600
    minutes = (seconds % 3600) // 60
    seconds = (seconds % 60)

    return '{:0>2d}:{:0>2d}:{:0>2d}'.format(hours, minutes, seconds)


if __name__ == "__main__":
    chdir(dirname(abspath(__file__)))
    DealRecord().main()


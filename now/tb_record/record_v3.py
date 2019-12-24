from time import time
from os.path import *
from json import dumps
from chardet import detect
from os import chdir, mkdir, listdir
from datetime import datetime, timedelta
from re import compile, search, findall, S
from shutil import copyfile

from excel_opea import ExcelOpea


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
            '访客数据',
        ]
        self.phone_pattern = compile(r'^1[34578]\d{9}')

        self.init_path()

    def init_path(self):
        for path in [
                self.dirpath, self.record_path, self.info_path,
                self.ending_path, self.keyword_path
        ]:
            try:
                mkdir(path)
            except FileExistsError:
                continue

    def deal_text(self, content: list):
        time_pattern = compile(
            r'([0-9]{3}[1-9]|[0-9]{2}[1-9][0-9]{1}|[0-9]{1}[1-9][0-9]{2}|[1-9][0-9]{3})-(((0[13578]|1[02])-(0[1-9]|[12][0-9]|3[01]))|((0[469]|11)-(0[1-9]|[12][0-9]|30))|(02-(0[1-9]|[1][0-9]|2[0-8]))) (0[0-9]|1[0-9]|2[0-3]):([0-5][0-9]):([0-5][0-9])'
        )
        if len(content) <= 1:
            return

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

    def ending_skill(self, content):
        # for item in reversed(content):

        if content['person'] != self.staff:
            self.info['有无结尾话术'] = '无'
        else:
            for line in self.ending_list:
                if line in content['text']:
                    self.info['有无结尾话术'] = '有'
                    return

            self.info['有无结尾话术'] = '无'

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

    def deal_trade(self, content: str):

        if self.is_trade is None:
            for trade in self.trade_list.keys():
                if trade in content:
                    self.is_trade = True
                    self.trade_list[trade] += 1

    def tourist(self, date: str):
        self.tourist_second = 60
        date = date.split(' ')[-1].split(':')
        for item in self.tourist_list:
            _time = item[1]

            try:

                seconds = _time.hour * 3600 + _time.minute * 60 + _time.second
                date_seconds = int(date[0]) * 3600 + int(date[1]) * 60 + int(
                    date[2])
            except AttributeError:
                continue
            else:
                if date_seconds - self.tourist_second <= seconds and date_seconds + self.tourist_second >= seconds:
                    self.info['访客数据'] = "{} {} {} {} {}".format(
                        item[0],
                        '{}:{}:{}'.format(item[1].hour, item[1].minute,
                                          item[1].second), item[2], item[3],
                        item[4])

    def get_phone(self, content):
        phone_obj = search(self.phone_pattern, content)

        if phone_obj:
            self.info['手机号'] = phone_obj.group()
            self.info['手机号所在记录'] = content
        elif self.info.get('手机号', None) is None:
            self.info['手机号'] = '无'
            self.info['手机号所在记录'] = '无'

    def judge_count(self, content):
        count = 0

        for value in content:
            if value['person'] is not self.staff:
                if value['text'] != '[卡片]':
                    count += 1

        if count == 0:
            self.statistical['一句后再无回复'] += 1

    # def trade_count(self, content):

    #     if self.statistical['行业数量'].get(keyword) is None:
    #         self.statistical['行业数量'][keyword] = 1
    #     else:
    #         self.statistical['行业数量'][keyword] += 1

    def deal_time(self, content: list):
        self.is_trade = None
        sign = 0
        record_time = None
        self.judge_count(content)
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
                self.get_phone(item['text'])
                self.deal_trade(item['text'])

                sign = 0

        if self.info.get('包含行业关键字') is None:
            self.info['包含行业关键字'] = '无'

        if self.info.get('回复时间（秒）') is not None:
            self.info['回复时间（秒）'] = convert_timedelta(self.info['回复时间（秒）'])

            if self.is_trade is not None:
                self.write(self.info)
            else:
                self.statistical['无关行业'] += 1

                if self.info.get('手机号', None) is not None:
                    self.write(self.info)

    def extract_record(self, path):

        try:
            with open(path, 'r', encoding='gbk') as fn:
                self.staff = fn.readline().replace('\n', '')
                content = fn.read()
        except UnicodeDecodeError:
            with open(path, 'r', encoding='utf-8') as fn:
                self.staff = fn.readline().replace('\n', '')
                content = fn.read()

        text = findall(r'={64}.*?={64}(.*?)={64}', content,
                       S)[0].strip('\n').split('\n')

        text_list = self.deal_text(text)

        if text_list is None:
            return

        shop = self.staff.split(':')[0]
        staff = self.staff.split(':')[-1]

        if self.statistical.get(shop) is None:
            self.statistical[shop] = {}
        if self.statistical[shop].get(staff) is None:
            self.statistical[shop][staff] = 0

        for key, value in text_list.items():
            self.info = {}
            self.info['客服ID'] = self.staff
            self.info['客户ID'] = key

            if key not in self.customer_list:
                self.customer_list.append(key)
            else:
                continue

            self.ending_skill(value[-1])
            self.tourist(value[0]['time'])
            self.deal_time(value)

            self.statistical[shop][staff] += 1

    def summary(self, path):
        summary_path = './data/结果/汇总.xlsx'
        now_data = self.excel.read(path)

        try:
            last_data = self.excel.read(summary_path)
        except FileNotFoundError:
            # system('xcopy "{}" "{}"'.format(path, summary_path))
            copyfile(path, summary_path)
        else:
            last_customer = [x[1] for x in last_data[1:]]
            # last_shop = [{x[1]: x[0].split(':')[0]} for x in last_data[1:-1]]
            last_shop = [x[0].split(':')[0] for x in last_data[1:]]

            for line in now_data[1:]:
                if line[1] in last_customer and line[0].split(
                        ':')[0] != last_shop[last_customer.index(line[1])]:
                    self.excel.append(line, fgColor='FF0000')
                else:
                    self.excel.append(line)

            self.excel.save(path=summary_path, mode='read')

    def single(self):
        a = self.statistical.pop('无关行业')
        b = self.statistical.pop('一句后再无回复')
        c = self.statistical.pop('行业数量')
        self.excel.init_sheet()
        for shop, data in self.statistical.items():
            for key, value in data.items():
                self.excel.write([shop, key, value])
        self.excel.write([f'无关行业:{a}', f'一句后再无回复:{b}', f'行业数量:{c}'])
        self.excel.save('{}统计.xlsx'.format(self.info_path))

    def main(self):
        self.some_input()
        self.statistical = {'无关行业': 0, '一句后再无回复': 0}

        self.excel = ExcelOpea()
        self.excel.init_sheet(header=self.header)
        self.write = self.excel.write

        self.tourist_list = self.excel.read('./data/访客数据/访客数据.xlsx')

        self.customer_list = []

        path = '{}结尾话术.txt'.format(self.ending_path)
        self.ending_list = read_lines(path, judge_code(path))

        path = '{}行业关键字.txt'.format(self.keyword_path)
        self.trade_list = read_lines(path, judge_code(path))
        self.trade_list = {i: 0 for i in self.trade_list}

        path = '{}包含关键字列表.txt'.format(self.keyword_path)
        self.keyword_list = read_lines(path, judge_code(path))

        for filename in listdir(self.record_path):
            self.extract_record(join(self.record_path, filename))

        self.statistical['行业数量'] = self.trade_list
        result_path = self.excel.save(self.info_path)

        self.summary(result_path)
        self.single()
        input('文件已保存, 按任意键退出')

    def some_input(self):
        self.tourist_second = check_int(input('请输入访客数据匹配时间, 默认 60 秒\n---> '))

        if not self.tourist_second:
            self.tourist_second = 60


def check_int(item):
    try:
        int(item)
    except TypeError:
        return False
    except ValueError:
        return 60
    else:
        return int(item)


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


def judge_code(path):
    with open(path, 'rb') as fn:
        data = fn.read()
        charinfo = detect(data)

    gb_encode = ["gb2312", "GB2312", "gb18030", "GB18030", "GBK", "gbk"]

    return 'GBK' if charinfo['encoding'] in gb_encode else charinfo['encoding']


def read_lines(path, encoding):
    with open(path, 'r', encoding=encoding) as fn:
        lines = fn.readlines()

    return [x.strip('\n') for x in lines]


if __name__ == "__main__":
    chdir(dirname(abspath(__file__)))
    DealRecord().main()

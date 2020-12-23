import re
import json
import time
import hashlib
from arr import arr_json
from loguru import logger
from configparser import ConfigParser
from chardet import detect

from utils import run_func, request, magic, excel
from config import PROXY


def judge_code(path):
    with open(path, 'rb') as fn:
        data = fn.read()
        charinfo = detect(data)

    gb_encode = ["gb2312", "GB2312", "gb18030", "GB18030", "GBK", "gbk"]

    return 'GBK' if charinfo['encoding'] in gb_encode else charinfo['encoding']


config = ConfigParser()
config.read('config.txt', encoding=judge_code('config.txt'))
country = config.get('配置', '国家')
match = config.get('配置', '联赛')
team = config.get('配置', '球队')
score = config.get('配置', '比分')


def made_secret():
    timestamp = int(time.time())
    orderno = PROXY.get('orderno')
    secret = PROXY.get('secret')
    txt = f'orderno={orderno},secret={secret},timestamp={timestamp}'
    sign = hashlib.md5(txt.encode('utf-8')).hexdigest().upper()

    return f'sign={sign}&orderno={orderno}&timestamp={timestamp}&change=true'


header = {
    'User-Agent':
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.100 Safari/537.36',
    'Accept': '*/*',
    'Referer': 'http://zq.win007.com/cn/League/2019-2020/36.html',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    # 'Proxy-Authorization': made_secret()
}
domain = 'http://zq.win007.com'
team_detail = []


@run_func()
def build_version():
    return time.strftime("%Y%m%d%H", time.localtime())


@run_func()
def build_href():
    data_list = arr_json
    need = []
    for data in data_list:
        current_country = data[1]
        if country and country != current_country:
            continue

        arr_class = data[-1]
        for arr_match in arr_class:
            arr_match = arr_match.split(',')
            if len(arr_match) <= 4:
                continue
            if match and match != arr_match[1]:
                continue

            if arr_match[2] == '1':
                aspx_name = 'League'
                if arr_match[3] != '0':
                    aspx_name = 'SubLeague'
                for temp_match in arr_match[4::]:
                    href = f'/cn/{aspx_name}/{temp_match}/{arr_match[0]}.html'
                    need.append((href, current_country))
            elif arr_match[2] == '2':
                for temp_match in arr_match[4::]:
                    href = f'/cn/CupMatch/{temp_match}/{arr_match[0]}.html'
                    need.append((href, current_country))
    return need


@run_func()
def show_team(team_id):
    return f'/cn/team/Summary/{team_id}.html'


@run_func()
def match_result(uri):
    resp = request(f'{domain}{uri}', header=header)
    result = re.search(
        r'<script type="text/javascript">var selectSeason = .*;var lang = .*; var jh = new Object\(\);var teamHelper = new Object\(\);var SclassID = .*; </script><script type="text/javascript"  src="(.*)"></script><script type="text/javascript"  src=".*"></script>',
        resp)

    if not result:
        return

    href = result.group(1)

    resp = request(f'{domain}{href}', header=header)
    result = re.search(r'var arrTeam = (.*?);', resp)
    if result:
        need = []
        arr_team = result.group(1)
        data = json.loads(arr_team.replace('\'', '\"'))
        for item in data:
            if not team:
                need.append(
                    (item[0], item[1])) if (item[0],
                                            item[1]) not in need else True
            elif team not in item:
                continue
            else:
                return [(item[0], item[1])]
    return need


@run_func()
def summary_team(team_id, current):
    uri = f'http://zq.win007.com/jsData/teamInfo/teamDetail/tdl{team_id}.js?version={build_version()}'

    if uri in team_detail:
        return
    else:
        team_detail.append(uri)
        resp = request(uri, header=header)
        if resp == 443:
            logger.error(f'443 - {uri}')
            return
        to_excel(resp, current)


@run_func()
class Miss(object):
    def __init__(self):
        self.miss_num = 0
        self.hit_num = 0
        self.miss_list = []
        super().__init__()

    def judge(self, hit=False):
        if hit:
            self.hit_num += 1
            self.miss_list.append(self.miss_num)
            self.miss_num = 0
        else:
            self.miss_num += 1

    def final(self):
        if not self.miss_list:
            return 0, 0, self.miss_num, self.miss_num, self.miss_list

        self.miss_list.append(self.miss_num)
        miss_sum = 0
        for x in self.miss_list:
            miss_sum += x

        miss_ave = miss_sum / len(self.miss_list)

        return self.hit_num, miss_ave, max(
            self.miss_list), self.miss_list[-1], self.miss_list


@run_func()
def get_team(content):
    return content.split('^')[0]


@run_func()
def to_excel(html, current):
    total.__init__()
    result = re.search(r'var teamCount = (.*);', html)
    if not result:
        return
    team_counts = result.group(1)
    team_counts = json.loads(team_counts.replace('\'', '\"'))
    stood = score.split('-')
    stood = [int(x) for x in stood]
    for team_count in team_counts[::-1]:
        team1 = get_team(team_count[7])
        team2 = get_team(team_count[8])

        if team and team not in [
                team1,
                team2,
        ]:
            continue
        if team != team1:
            temp = team1
            team1 = team2
            team2 = temp
            team_stood = [team_count[10], team_count[9]]
        else:
            team_stood = [team_count[9], team_count[10]]

        if match and match != get_team(team_count[5]):
            continue

        if score:
            if stood[0] == team_stood[0] and stood[1] == team_stood[1]:
                total.judge(hit=True)
            else:
                total.judge()
        else:
            continue


class BaseError(Exception):
    def __init__(self, *args):
        self.args = args


def main():
    global team
    excel.init_sheet(
        header=['国家', '联赛', '球队', '比分', '总次数', '平均遗漏', '最长遗漏', '目前遗漏', '遗漏数据'])
    href_list = build_href()
    teams = []
    for href, current in href_list:
        results = match_result(href)
        if not results:
            continue

        for result in results:
            if result in teams:
                continue
            teams.append(result)

    for team_id, team_name in teams:
        team = team_name
        result = summary_team(team_id, current)

        result = total.final()
        detail = {}
        detail['国家'] = current
        detail['联赛'] = match
        detail['球队'] = team_name
        detail['比分'] = score
        detail['总次数'] = result[0]
        detail['平均遗漏'] = result[1]
        detail['最长遗漏'] = result[2]
        detail['目前遗漏'] = result[3]
        detail['遗漏数据'] = result[4]

        excel.write(detail)
        # mongo.insert({'time': 1, 'data': detail}, 'win007')

    result = excel.save()
    if result:
        print(f'已保存为 - {result}')
    else:
        print(f'保存失败')

    input('按任意键继续')


total = Miss()

if __name__ == "__main__":
    if int(time.time()) < 1629729356:
        magic()
        main()

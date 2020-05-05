import os
import re
import time
import json
import random
import pymysql
from bs4 import BeautifulSoup

from config import DEBUG, logger
from utils.run import run_func
from utils.request import Query
from utils.soup import DealSoup


def remove_character(content: str):
    return content.replace("\n", "").replace("\r",
                                             "").replace(" ",
                                                         "").replace("\t", "")


def to_date(content: str):
    return content.split(': ')[-1].strip(' ')


def clean_date(content: str):
    return content.replace('年', '-').replace('月', '-').replace('日', '')


class DealZhuhai(object):
    def __init__(self):
        self.bid_path = "https://www.youzhicai.com/sn{}/2102.html"
        self.bid_detail = "https://www.gec123.com/xcjenquiry/notice!enquiryNotice.action?notic_seq={}"
        self.result_path = "https://www.youzhicai.com/sn{}/2202.html"
        self.result_detail = "https://www.gec123.com/xcj-gateway/api/v1/notices/stable/{}"
        self.header = {
            'User-Agent':
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.100 Safari/537.36',
            'Accept':
            'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'zh-CN,zh;q=0.9'
        }

        self.insert_tb_bid = "INSERT INTO `bidpython`.`tb_bid` ( `title`, `inviter_number`, `announce_time`, `end_time`, `budget_money`, `platform_id`, `url`, `company` ) VALUES ( '{网上竞价名称}', '{网上竞价编号}', '{竞价开始时间}', '{竞价截止时间}', '{金额上限}', 21, '{path}', '{采购人}' );"
        self.insert_bid_result = "INSERT INTO `bidpython`.`tb_bid_result` ( `title`, `inviter_number`, `announce_time`, `end_time`, `announce_date`, `platform_id`, `url`, `company`, `budget_money`, `announce_company` ) VALUES ( '{网上竞价名称}', '{网上竞价编号}', '{竞价开始时间}', '{竞价截至时间}', '{成交公告时间}', 21, '{path}', '{采购人}', '{中标总额}', '{中标公司}' );"
        self.insert_bid_json = "INSERT INTO `bidpython`.`tb_bid_json` ( `shot`, `platform_name`, `inviter_number`, `url`, `json_kv`, `create_time` ) VALUES ( '', '优质采', '{}', '{}', '{}', '{}');"
        self.insert_tr_json = "INSERT INTO `bidpython`.`tb_tr_json` ( `platform_id`, `platform_name`, `tr_json`, `url` ) VALUES ( 21, '优质采', '{}', '{}');"
        self.request = Query().run
        self.soup = DealSoup().judge
        self.init_sql()

    def init_sql(self):
        from config import DATABASES

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
            self.ecnu_cursor = ecnu_mysql.cursor()

    def ergodic_p(self, p_objs: BeautifulSoup):
        p_list = p_objs.contents
        info = {}
        for p_obj in p_list:
            if isinstance(p_obj, str):
                continue
            else:
                text = p_obj.text

                if "网上竞价编号：" in text:
                    info["网上竞价编号"] = text.split(("："))[-1]
                elif "网上竞价名称：" in text:
                    info["网上竞价名称"] = text.split(("："))[-1]
                elif "采购人：" in text:
                    info["采购人"] = text.split(("："))[-1]
                elif "联系人：'" in text:
                    info["联系人"] = text.split(("："))[-1]
                elif "联系电话：" in text:
                    info["联系电话"] = text.split(("："))[-1]
                elif "竞价开始时间" in text or "竞价截止时间" in text:
                    if "竞价截止时间" in text:
                        info["竞价截止时间"] = text.split("竞价截止时间：")[-1]
                    if "竞价开始时间：" in text:
                        info["竞价开始时间"] = text.split(" 竞价截止时间")[0].split(
                            "：")[-1]
                elif "品目类型：" in text:
                    info["品目类型"] = text.split(("："))[-1]
                elif "金额上限：" in text:
                    info["金额上限"] = text.split(("："))[-1].replace("元", "")

        return info

    def ergodic_tr(self, tr_list: list, sign='td'):
        info = {}

        if sign == 'td':
            info['产品名称'] = self.soup(tr_list[0], attr=sign).text.replace(
                '需求1', '').replace('(', '').replace(')', '')
            temp = self.soup(tr_list[1], attr=sign, all_tag=True)
            info['产品单价'] = temp[1].text.replace('¥', '')
            info['数量'] = temp[3].text.split(' ')[0]
            info['单位'] = temp[3].text.split(' ')[-1]
            info['单位'] = temp[3].text.split(' ')[-1]
            info['金额上限'] = temp[-1].text.replace('¥', '')

            return info
        elif sign == 'p':
            td_list = self.soup(tr_list[1], attr=sign, all_tag=True)

            info['竞价开始时间'] = td_list[2].text.split('：')[-1].split(
                '～')[0].strip(' ')
            info['竞价截止时间'] = td_list[2].text.split('：')[-1].split(
                '～')[-1].strip(' ')
            info['采购人'] = td_list[3].text.split('：')[-1]

            return info

    def judge_already(self, item_code):
        if self.bid_type == "bid":
            sql = "SELECT `id` FROM `bidpython`.`tb_bid` WHERE `inviter_number` = '{}' and `platform_id` = 18 LIMIT 1;"
        elif self.bid_type == "bidResult":
            sql = "SELECT `id` FROM `bidpython`.`tb_bid_result` WHERE `inviter_number` = '{}' and `platform_id` = 18 LIMIT 1;"

        if run_func(self.ecnu_cursor.execute, sql.format(item_code)) == 0:
            return True
        else:
            return

    def get_time(self):
        return time.strftime('%Y-%m-%d %H:%M:%S',
                             time.localtime(int(time.time())))

    def get_text(self, content):
        if content is None:
            return
        else:
            text = content.text
            if text is None:
                return
            else:
                return text

    def deal_detail(self, page):
        resp = run_func(self.request,
                        self.bid_path.format(page),
                        header=self.header)
        projects = self.soup(resp,
                             attr={'class': 'project-li clearfix'},
                             all_tag=True)

        for project in projects:
            if self.soup(project, attr={'class': 'left-day'}).text == '已截止':
                continue

            info = {}
            info["网上竞价名称"] = self.soup(project,
                                       attr={
                                           'class': 'project-name0 el'
                                       }).get('title')
            info["竞价开始时间"] = self.soup(project, attr={
                'class': 'pub-value0'
            }).text
            info["采购人"] = self.soup(project, attr={
                'class': 'pub-company0 el'
            }).text
            info["path"] = f'https://www.youzhicai.com{project.a.get("href")}'

            resp = run_func(self.request, info["path"], header=self.header)

            detail = self.soup(resp, attr={'class': 'content-message'})
            divs = self.soup(detail, 'div', all_tag=True)

            info["网上竞价编号"] = to_date(divs[1].text)

            if not self.judge_already(info["网上竞价编号"]):
                continue

            info["竞价截止时间"] = to_date(divs[2].text)
            info['金额上限'] = ''

            tr_json = [{
                "参数": "",
                "单位": '',
                "招标编号": '',
                "序号": 1,
                "产品名称": '',
                "产品类别": "",
                "产品单价": '',
                "合计": '',
                "品牌": "",
                "数量": '',
                "标配": "",
                "型号": '',
                "url": '',
                "招标平台": "优质采",
                "售后服务": "",
            }]

            run_func(self.ecnu_cursor.execute,
                     self.insert_tb_bid.format(**info))

            run_func(
                self.ecnu_cursor.execute,
                self.insert_bid_json.format(
                    info["网上竞价编号"], info["path"],
                    json.dumps(tr_json, ensure_ascii=False), self.get_time()))

    def deal_result(self, page):
        resp = run_func(self.request,
                        self.result_path.format(page),
                        header=self.header)
        projects = self.soup(resp,
                             attr={'class': 'project-li clearfix'},
                             all_tag=True)

        for project in projects:
            info = {}
            info["网上竞价名称"] = self.soup(project,
                                       attr={
                                           'class': 'project-name0 el'
                                       }).get('title')

            info["采购人"] = self.soup(project, attr={
                'class': 'pub-company0 el'
            }).text
            info["path"] = f'https://www.youzhicai.com{project.a.get("href")}'
            resp = run_func(self.request, info["path"], header=self.header)
            detail = self.soup(resp, attr={'class': 'content-message'})
            divs = self.soup(detail, 'div', all_tag=True)
            info["网上竞价编号"] = to_date(divs[1].text)
            if not self.judge_already(info["网上竞价编号"]):
                continue
            info["成交公告时间"] = to_date(divs[0].text)
            info["竞价开始时间"] = ''
            info["竞价截至时间"] = to_date(divs[2].text)
            info["中标总额"] = ''
            info['中标公司'] = ''

            tr_json = [{
                "成交时间": "",
                "招标编号": '',
                "规格配置": '',
                "详情url": '',
                "平台名称": "优质采",
                "总价": '',
                "中标供应商": '',
                "设备名称": '',
                "创建时间": '',
                "品牌": '',
                "型号": '',
                "数量": ''
            }]

            run_func(self.ecnu_cursor.execute,
                     self.insert_bid_result.format(**info))

            run_func(
                self.ecnu_cursor.execute,
                self.insert_tr_json.format(
                    json.dumps(tr_json, ensure_ascii=False), info["path"]))

    def main(self):
        for page in range(1, 2):
            self.bid_type = "bid"
            run_func(self.deal_detail, page)
            self.bid_type = "bidResult"
            run_func(self.deal_result, page)


if __name__ == "__main__":
    os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    DealZhuhai().main()

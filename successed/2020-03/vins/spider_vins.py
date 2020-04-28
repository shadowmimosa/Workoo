import os
import re
import time
import json
import random
import hashlib
import pymysql
from bs4 import BeautifulSoup

from utils.run import run_func
from utils.request import Query
from utils.soup import DealSoup
from config import DEBUG, logger, PROXY


def remove_character(content: str):
    return content.replace("\n", "").replace("\r",
                                             "").replace(" ",
                                                         "").replace("\t", "")


def clean_date(content: str):
    return content.replace('年', '-').replace('月', '-').replace('日', '')


def made_secret():
    timestamp = int(time.time())
    orderno = PROXY.get('orderno')
    secret = PROXY.get('secret')
    txt = f'orderno={orderno},secret={secret},timestamp={timestamp}'
    sign = hashlib.md5(txt.encode('utf-8')).hexdigest().upper()

    return f'sign={sign}&orderno={orderno}&timestamp={timestamp}&change=true'


class DealVins(object):
    def __init__(self):
        self.bid_path = "http://s.vins.com.cn/business/home/tf24Page"
        self.bid_detail = ""
        self.result_path = "http://s.vins.com.cn/business/home/tf23Page"
        self.result_detail = ""
        self.header = {
            'Origin': 'http://s.vins.com.cn',
            'Content-Type': 'application/x-www-form-urlencoded',
            'User-Agent':
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.100 Safari/537.36',
            'Accept':
            'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'Referer': 'http://s.vins.com.cn/business/home/tf24Page',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,zh;q=0.9',
        }
        self.data = 'keyword=f01&condition=LIKE&searchValue=&orderField=&orderDirection=&pageNum={}'
        self.insert_tb_bid = "INSERT INTO `bidpython`.`tb_bid` ( `title`, `inviter_number`, `announce_time`, `end_time`, `budget_money`, `platform_id`, `url`, `company` ) VALUES ( '{网上竞价名称}', '{网上竞价编号}', '{竞价开始时间}', '{竞价截止时间}', '{金额上限}', 19, '{path}', '{采购人}' );"
        self.insert_bid_result = "INSERT INTO `bidpython`.`tb_bid_result` ( `title`, `inviter_number`, `announce_time`, `end_time`, `announce_date`, `platform_id`, `url`, `company`, `budget_money`, `announce_company` ) VALUES ( '{网上竞价名称}', '{网上竞价编号}', '{竞价开始时间}', '{竞价截止时间}', '{成交公告时间}', 19, '{path}', '{采购人}', '{中标总额}', '{中标公司}' );"
        self.insert_bid_json = "INSERT INTO `bidpython`.`tb_bid_json` ( `shot`, `platform_name`, `inviter_number`, `url`, `json_kv`, `create_time` ) VALUES ( '', '高校优采仪器设备竞价网', '{}', '{}', '{}', '{}');"
        self.insert_tr_json = "INSERT INTO `bidpython`.`tb_tr_json` ( `platform_id`, `platform_name`, `tr_json`, `url` ) VALUES ( 19, '高校优采仪器设备竞价网', '{}', '{}');"
        self.request = Query().run
        self.soup = DealSoup().judge
        self.init_sql()
        self.pattern = re.compile(r"\(询价编号：.*\)")

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
            sql = "SELECT `id` FROM `bidpython`.`tb_bid` WHERE `inviter_number` = '{}' and `platform_id` = 19 LIMIT 1;"
        elif self.bid_type == "bidResult":
            sql = "SELECT `id` FROM `bidpython`.`tb_bid_result` WHERE `inviter_number` = '{}' and `platform_id` = 19 LIMIT 1;"

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
        self.header.update({'Proxy-Authorization': made_secret()})
        resp = run_func(self.request,
                        self.bid_path,
                        header=self.header,
                        data=self.data.format(page)).replace(r'&nbsp;', '')

        divs = self.soup(resp,
                         attr={'class': 'bidding-order-block'},
                         all_tag=True)
        for div in divs:
            info = {}
            info["采购人"] = self.soup(div, attr={'class': 'school-name'}).text
            temp = self.soup(div, attr={'class': 'order-detail'})
            info["网上竞价名称"] = temp.text

            bidding = self.soup(div, attr={'class': 'bidding-order-line'})

            info["网上竞价编号"] = self.soup(div, attr={
                'class': 'order-number'
            }).text.split('：')[-1]

            if not self.judge_already(info["网上竞价编号"]):
                logger.info(f'{info["网上竞价编号"]} - 已存在')
                continue

            info["竞价截止时间"] = self.soup(div, attr={
                'class': 'time_surplus'
            }).get('value')
            info["竞价开始时间"] = self.soup(div,
                                       attr={
                                           'class': 'order-publishdate'
                                       }).text.split('：')[-1]

            temp = temp.get('onclick').split('(')[-1].split(',')
            info[
                "path"] = 'http://s.vins.com.cn/business/home/bidinput/1/{}/{}'.format(
                    temp[0].replace('\'', ''),
                    temp[-1].replace(')', '').replace('\'', ''))

            info['金额上限'] = ''
            self.header.update({'Proxy-Authorization': made_secret()})
            resp = run_func(self.request, info["path"],
                            header=self.header).replace(r'&nbsp;', '')
            # table = self.soup(resp, 'table', all_tag=True)[-1]
            tds = self.soup(resp, attr={'class': 'L4'}, all_tag=True)

            order_type = self.soup(div, attr={'class': 'order-type'}).text

            tr_json = [{
                "参数": tds[4].text,
                "单位": '',
                "招标编号": info["网上竞价编号"],
                "序号": 1,
                "产品名称": tds[0].text,
                "产品类别": order_type,
                "产品单价": '',
                "合计": '',
                "品牌": tds[1].text,
                "数量": tds[5].text,
                "标配": tds[3].text,
                "型号": tds[2].text,
                "url": info["path"],
                "招标平台": "高校优采仪器设备竞价网",
                "售后服务": tds[7].text,
            }]

            run_func(self.ecnu_cursor.execute,
                     self.insert_tb_bid.format(**info))

            run_func(
                self.ecnu_cursor.execute,
                self.insert_bid_json.format(
                    info["网上竞价编号"], info["path"],
                    json.dumps(tr_json, ensure_ascii=False), self.get_time()))

    def deal_result(self, page):
        self.header.update({'Proxy-Authorization': made_secret()})
        resp = run_func(self.request,
                        self.result_path,
                        header=self.header,
                        data=self.data.format(page)).replace(r'&nbsp;', '')

        divs = self.soup(resp,
                         attr={'class': 'bidding-order-block'},
                         all_tag=True)
        for div in divs:
            info = {}
            info["采购人"] = self.soup(div, attr={'class': 'school-name'}).text
            temp = self.soup(div, attr={'class': 'order-detail'})
            info["网上竞价名称"] = temp.text

            bidding = self.soup(div, attr={'class': 'bidding-order-line'})

            info["网上竞价编号"] = self.soup(div, attr={
                'class': 'order-number'
            }).text.split('：')[-1]

            if not self.judge_already(info["网上竞价编号"]):
                logger.info(f'{info["网上竞价编号"]} - 已存在')
                continue

            info["竞价截止时间"] = ''
            info["成交公告时间"] = self.soup(div,
                                       attr={
                                           'class': 'order-publishdate'
                                       }).text.split('：')[-1]
            info["竞价开始时间"] = ""

            temp = temp.get('onclick').split('(')[-1].split(',')
            info[
                "path"] = 'http://s.vins.com.cn/business/home/bidinput/2/{}/{}'.format(
                    temp[0].replace('\'', ''),
                    temp[-1].replace(')', '').replace('\'', ''))

            info['金额上限'] = ''
            self.header.update({'Proxy-Authorization': made_secret()})
            resp = run_func(self.request, info["path"],
                            header=self.header).replace(r'&nbsp;', '')
            item = self.soup(
                resp,
                attr={
                    'style':
                    'border-top:solid 1px #abc4c1; border-right:solid 1px #abc4c1'
                })
            item_result = self.soup(
                resp, attr={'style': 'background-color:#fffee1;'})

            tds_1 = self.soup(item, attr={'class': 'L4'}, all_tag=True)
            tds_2 = self.soup(item_result, attr='td', all_tag=True)

            order_type = self.soup(div, attr={'class': 'order-type'}).text
            info['中标公司'] = tds_2[0].text
            info["中标总额"] = tds_2[2].text

            tr_json = [{
                "成交时间": "",
                "招标编号": info["网上竞价编号"],
                "规格配置": tds_1[4].text,
                "详情url": info['path'],
                "平台名称": "高校优采仪器设备竞价网",
                "总价": tds_2[2].text,
                "中标供应商": info['中标公司'],
                "设备名称": tds_1[0].text,
                "创建时间": self.get_time(),
                "品牌": tds_1[1].text,
                "型号": tds_1[2].text,
                "数量": tds_1[5].text
            }]

            run_func(self.ecnu_cursor.execute,
                     self.insert_bid_result.format(**info))

            run_func(
                self.ecnu_cursor.execute,
                self.insert_tr_json.format(
                    json.dumps(tr_json, ensure_ascii=False), info["path"]))

    def main(self):
        for page in range(1, 15):
            self.bid_type = "bid"
            run_func(self.deal_detail, page)
            self.bid_type = "bidResult"
            run_func(self.deal_result, page)


if __name__ == "__main__":
    os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    DealVins().main()

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


def clean_date(content: str):
    return content.replace('年', '-').replace('月', '-').replace('日', '')


class DealVins(object):
    def __init__(self):
        self.bid_path = "http://mkt.zycg.gov.cn/proxy/platform/platform/notice/queryMallNoticePageList?pageSize=10&pageNum={}&noticeTypes=1&effectType=9&noticeStatus=10"
        self.bid_detail = ""
        self.result_path = "http://mkt.zycg.gov.cn/proxy/platform/platform/notice/queryMallNoticePageList?pageSize=10&pageNum={}&noticeTypes=4&effectType=9&noticeStatus=10"
        self.result_detail = ""
        self.header = {
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'User-Agent':
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.100 Safari/537.36',
            'Referer':
            'http://mkt.zycg.gov.cn/mall-view/information/noticeList/',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,zh;q=0.9',
        }
        self.data = 'keyword=f01&condition=LIKE&searchValue=&orderField=&orderDirection=&pageNum={}'
        self.insert_tb_bid = "INSERT INTO `bidpython`.`tb_bid` ( `title`, `inviter_number`, `announce_time`, `end_time`, `budget_money`, `platform_id`, `url`, `company` ) VALUES ( '{网上竞价名称}', '{网上竞价编号}', '{竞价开始时间}', '{竞价截止时间}', '{金额上限}', 20, '{path}', '{采购人}' );"
        self.insert_bid_result = "INSERT INTO `bidpython`.`tb_bid_result` ( `title`, `inviter_number`, `announce_time`, `end_time`, `announce_date`, `platform_id`, `url`, `company`, `budget_money`, `announce_company` ) VALUES ( '{网上竞价名称}', '{网上竞价编号}', '{竞价开始时间}', '{竞价截止时间}', '{成交公告时间}', 20, '{path}', '{采购人}', '{中标总额}', '{中标公司}' );"
        self.insert_bid_json = "INSERT INTO `bidpython`.`tb_bid_json` ( `shot`, `platform_name`, `inviter_number`, `url`, `json_kv`, `create_time` ) VALUES ( '', '中央政府采购网', '{}', '{}', '{}', '{}');"
        self.insert_tr_json = "INSERT INTO `bidpython`.`tb_tr_json` ( `platform_id`, `platform_name`, `tr_json`, `url` ) VALUES ( 20, '中央政府采购网', '{}', '{}');"
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
            sql = "SELECT `id` FROM `bidpython`.`tb_bid` WHERE `inviter_number` = '{}' and `platform_id` = 20 LIMIT 1;"
        elif self.bid_type == "bidResult":
            sql = "SELECT `id` FROM `bidpython`.`tb_bid_result` WHERE `inviter_number` = '{}' and `platform_id` = 20 LIMIT 1;"

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

    def deal_detail(self, item):
        path = f'http://mkt.zycg.gov.cn/proxy/platform/platform/notice/queryMallNoticeById?platformId=20&id={item["id"]}'
        info = {}
        resp = run_func(
            self.request,
            path,
            header=self.header,
        )
        data = json.loads(resp)['data']
        content = data['contentStr']

        info["网上竞价名称"] = self.soup(content, {
            'class': 'inquiry-order-name'
        }).text.replace('项目名称: ', '')
        info["采购人"] = self.soup(content, {'id': 'buyerName'}).text
        info["网上竞价编号"] = self.soup(content, {
            'class': 'inquiry-order-number'
        }).text.replace('项目编号: ', '')

        if not self.judge_already(info["网上竞价编号"]):
            logger.info(f'{info["网上竞价编号"]} - 已存在')
            return

        info["竞价截止时间"] = self.soup(content, {'id': 'quoteEndTime'}).text
        info["竞价开始时间"] = item['publishTimeStr']
        info["金额上限"] = self.soup(content, {'id': 'projectBudget'}).text
        info[
            "path"] = f'http://mkt.zycg.gov.cn/mall-view/information/detail?noticeId={item["id"]}'

        tds = self.soup(self.soup(content, 'tbody'), 'td', True)

        if not tds:
            tr_json = [{}]
        else:
            tr_json = [{
                "参数": tds[-1].text,
                "单位": tds[5].text,
                "招标编号": info["网上竞价编号"],
                "序号": 1,
                "产品名称": tds[2].text,
                "产品类别": tds[1].text,
                "产品单价": '',
                "合计": '',
                "品牌": tds[3].text,
                "数量": tds[6].text,
                "标配": '',
                "型号": tds[4].text,
                "url":
                f'http://mkt.zycg.gov.cn/mall-view/information/detail?noticeId={item["id"]}',
                "招标平台": "中央政府采购网",
                "售后服务": '',
            }]

        run_func(self.ecnu_cursor.execute, self.insert_tb_bid.format(**info))

        run_func(
            self.ecnu_cursor.execute,
            self.insert_bid_json.format(
                info["网上竞价编号"], info["path"],
                json.dumps(tr_json, ensure_ascii=False), self.get_time()))

    def deal_result(self, item):
        path = f'http://mkt.zycg.gov.cn/proxy/platform/platform/notice/queryMallNoticeById?platformId=20&id={item["id"]}'
        info = {}
        resp = run_func(
            self.request,
            path,
            header=self.header,
        )
        data = json.loads(resp)['data']
        content = data['contentStr']

        info["网上竞价名称"] = self.soup(content, {
            'class': 'inquiry-order-name'
        }).text.replace('项目名称: ', '')

        info["采购人"] = self.soup(content, {'id': 'buyerName'}).text
        info["网上竞价编号"] = self.soup(content, {
            'class': 'inquiry-order-number'
        }).text.replace('项目编号: ', '')

        if not self.judge_already(info["网上竞价编号"]):
            logger.info(f'{info["网上竞价编号"]} - 已存在')
            return

        info["竞价截止时间"] = self.soup(content, {'id': 'quoteEndTime'}).text
        info["成交公告时间"] = item['publishTimeStr']
        info["竞价开始时间"] = ""
        info[
            "path"] = f'http://mkt.zycg.gov.cn/mall-view/information/detail?noticeId={item["id"]}'

        info["金额上限"] = self.soup(content, {'id': 'projectBudget'}).text

        requires = self.soup(content, {'class': 'requireList-wrap'}, True)

        goods = self.soup(self.soup(requires[0], 'tbody'), 'td', True)
        companys = self.soup(self.soup(requires[1], 'tbody'), 'td', True)

        info['中标公司'] = companys[2].text
        info["中标总额"] = companys[5].text

        tr_json = [{
            "成交时间": '',
            "招标编号": info["网上竞价编号"],
            "规格配置": '',
            "详情url": info['path'],
            "平台名称": "中央政府采购网",
            "总价": companys[5].text,
            "中标供应商": info['中标公司'],
            "设备名称": goods[2].text,
            "创建时间": self.get_time(),
            "品牌": goods[3].text,
            "型号": goods[4].text,
            "数量": goods[6].text
        }]

        run_func(self.ecnu_cursor.execute,
                 self.insert_bid_result.format(**info))

        run_func(
            self.ecnu_cursor.execute,
            self.insert_tr_json.format(json.dumps(tr_json, ensure_ascii=False),
                                       info["path"]))

    def single(self, path):

        resp = run_func(
            self.request,
            path,
            header=self.header,
        )
        data_list = json.loads(resp)

        for item in data_list['data']['result']:
            if self.bid_type == 'bid':
                run_func(self.deal_detail, item)
            elif self.bid_type == 'bidResult':
                run_func(self.deal_result, item)

    def main(self):
        for page in range(1, 5):
            self.bid_type = "bid"
            run_func(self.single, self.bid_path.format(page))
            self.bid_type = "bidResult"
            run_func(self.single, self.result_path.format(page))


if __name__ == "__main__":
    os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    DealVins().main()

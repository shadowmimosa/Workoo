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


class DealGec(object):
    def __init__(self):
        self.bid_path = 'https://www.gec123.com/enquiry/api/v1/packages?pi={}&ps=12'
        self.header = {
            "User-Agent":
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.120 Safari/537.36",
            "Accept": "*/*",
            "Referer": "https://www.gec123.com/ge/",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "zh-CN,zh;q=0.9",
        }

        self.insert_tb_bid = "INSERT INTO `bidpython`.`tb_bid` ( `title`, `inviter_number`, `announce_time`, `end_time`, `budget_money`, `platform_id`, `url`, `company` ) VALUES ( '{网上竞价名称}', '{网上竞价编号}', '{竞价开始时间}', '{竞价截止时间}', '{金额上限}', 23, '{path}', '{采购人}' );"
        self.insert_bid_result = "INSERT INTO `bidpython`.`tb_bid_result` ( `title`, `inviter_number`, `announce_time`, `end_time`, `announce_date`, `platform_id`, `url`, `company`, `budget_money`, `announce_company` ) VALUES ( '{网上竞价名称}', '{网上竞价编号}', '{竞价开始时间}', '{竞价截至时间}', '{成交公告时间}', 23, '{path}', '{采购人}', '{中标总额}', '{中标公司}' );"
        self.insert_bid_json = insert_sql = "INSERT INTO `bidpython`.`tb_bid_json` ( `shot`, `platform_name`, `inviter_number`, `url`, `json_kv`, `create_time` ) VALUES ( '', '重庆市政府采购云平台', '{}', '{}', '{}', '{}');"
        self.insert_tr_json = insert_sql = "INSERT INTO `bidpython`.`tb_tr_json` ( `platform_id`, `platform_name`, `tr_json`, `url` ) VALUES ( 23, '重庆市政府采购云平台', '{}', '{}');"
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

    def judge_already(self, item_code):
        if self.bid_type == "bid":
            sql = "SELECT `id` FROM `bidpython`.`tb_bid` WHERE `inviter_number` = '{}' and `platform_id` = 23 LIMIT 1;"
        elif self.bid_type == "bidResult":
            sql = "SELECT `id` FROM `bidpython`.`tb_bid_result` WHERE `inviter_number` = '{}' and `platform_id` = 23 LIMIT 1;"

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

    def remove_character(self, content: str):
        return content.replace("\n",
                               "").replace("\r", "").replace(" ", "").replace(
                                   ")", "").replace('（', '').replace(
                                       '询价号', '').replace('：',
                                                          '').replace('）', '')

    def deal_detail(self, path, item):
        info = {}
        resp = run_func(self.request, path, header=self.header)
        no = self.soup(resp, {'class': 'enquiry-no'})
        info["网上竞价编号"] = self.remove_character(no.text)

        if not self.judge_already(info["网上竞价编号"]):
            return

        info["网上竞价名称"] = item["noticeName"]
        info["金额上限"] = item["totalLimit"]
        info["path"] = path

        info["采购人"] = self.soup(resp, {'class': 'contact-content'}).text

        # item["publishTime"]
        info["竞价开始时间"] = time.strftime(
            '%Y-%m-%d %H:%M:%S',
            time.localtime(int(item['enqStartTime']) / 1000))

        info["竞价截止时间"] = time.strftime(
            '%Y-%m-%d %H:%M:%S',
            time.localtime(int(item['enqEndTime']) / 1000))

        tr_json = []

        for index, good in enumerate(item.get('goods')):
            tr_json.append({
                "参数": "",
                "单位": good.get("unit"),
                "招标编号": info["网上竞价编号"],
                "序号": index + 1,
                "产品名称": good.get('stockDirName'),
                "产品类别": "",
                "产品单价": "",
                "合计": good.get('stockLimit'),
                "品牌": "",
                "数量": good.get('goodsNum'),
                "标配": "",
                "型号": good.get('stockDirCode'),
                "url": path,
                "招标平台": "重庆市政府采购云平台",
                "售后服务": "",
            })

        run_func(self.ecnu_cursor.execute, self.insert_tb_bid.format(**info))

        run_func(
            self.ecnu_cursor.execute,
            self.insert_bid_json.format(
                info["网上竞价编号"], info["path"],
                json.dumps(tr_json, ensure_ascii=False), self.get_time()))

    def deal_result(self, path, item):
        info = {}
        resp = run_func(self.request, path, header=self.header)
        no = self.soup(resp, {'class': 'enquiry-no'})
        info["网上竞价编号"] = self.remove_character(no.text)

        if not self.judge_already(info["网上竞价编号"]):
            return

        info["网上竞价名称"] = item["noticeName"]
        info["采购人"] = self.soup(resp, {'class': 'contact-content'}).text
        info["path"] = path

        info["中标公司"] = item.get('providerOrgName')
        info["成交公告时间"] = time.strftime(
            '%Y-%m-%d %H:%M:%S',
            time.localtime(int(item.get('publishTime')) / 1000))
        info["竞价开始时间"] = ""
        info["竞价截至时间"] = ""

        info["中标总额"] = item.get('totalLimit')

        tr_json = []

        for good in item.get('goods'):
            tr_json.append({
                "成交时间": "",
                "招标编号": info["网上竞价编号"],
                "规格配置": '',
                "详情url": info["path"],
                "平台名称": "重庆市政府采购云平台",
                "总价": good.get('stockLimit'),
                "中标供应商": info["中标公司"],
                "设备名称": good.get('stockDirName'),
                "创建时间": self.get_time(),
                "品牌": '',
                "型号": good.get('stockDirCode'),
                "数量": good.get('goodsNum')
            })

        run_func(self.ecnu_cursor.execute,
                 self.insert_bid_result.format(**info))

        run_func(
            self.ecnu_cursor.execute,
            self.insert_tr_json.format(json.dumps(tr_json, ensure_ascii=False),
                                       info["path"]))

    def main(self):
        for page in range(1, 31):
            resp = run_func(self.request,
                            self.bid_path.format(page),
                            header=self.header)

            data = json.loads(resp)["packages"]

            for item in data:
                path = f'https://www.gec123.com/enquiry/notice!enquiryNotice.action?notic_seq={item.get("noticeId")}'
                info = {}
                result = item.get('result')
                if result == -1:
                    self.bid_type = 'bid'
                    run_func(self.deal_detail, path, item)
                elif result == 1:
                    self.bid_type = "bidResult"
                    run_func(self.deal_result, path, item)


if __name__ == "__main__":
    os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    DealGec().main()

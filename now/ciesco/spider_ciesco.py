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


class DealCiesco(object):
    def __init__(self):
        self.bid_path = "https://dzzb.ciesco.com.cn/xjcg/xjcgList"
        self.bid_detail = "https://www.gec123.com/xcjenquiry/notice!enquiryNotice.action?notic_seq={}"
        self.result_path = "https://dzzb.ciesco.com.cn/xjcg/jgggList"
        self.result_detail = "https://www.gec123.com/xcj-gateway/api/v1/notices/stable/{}"
        self.header = {
            'Origin': 'https://dzzb.ciesco.com.cn',
            'Content-Type': 'application/x-www-form-urlencoded',
            'User-Agent':
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.100 Safari/537.36',
            'Accept':
            'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'Referer': 'https://dzzb.ciesco.com.cn/xjcg/xjcgList',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'zh-CN,zh;q=0.9',
        }

        self.insert_tb_bid = "INSERT INTO `bidpython`.`tb_bid` ( `title`, `inviter_number`, `announce_time`, `end_time`, `budget_money`, `platform_id`, `url`, `company` ) VALUES ( '{网上竞价名称}', '{网上竞价编号}', '{竞价开始时间}', '{竞价截止时间}', '{金额上限}', 22, '{path}', '{采购人}' );"
        self.insert_bid_result = "INSERT INTO `bidpython`.`tb_bid_result` ( `title`, `inviter_number`, `announce_time`, `end_time`, `announce_date`, `platform_id`, `url`, `company`, `budget_money`, `announce_company` ) VALUES ( '{网上竞价名称}', '{网上竞价编号}', '{竞价开始时间}', '{竞价截至时间}', '{成交公告时间}', 22, '{path}', '{采购人}', '{中标总额}', '{中标公司}' );"
        self.insert_bid_json = "INSERT INTO `bidpython`.`tb_bid_json` ( `shot`, `platform_name`, `inviter_number`, `url`, `json_kv`, `create_time` ) VALUES ( '', '招商局集团电子招标采购交易网', '{}', '{}', '{}', '{}');"
        self.insert_tr_json = "INSERT INTO `bidpython`.`tb_tr_json` ( `platform_id`, `platform_name`, `tr_json`, `url` ) VALUES ( 22, '招商局集团电子招标采购交易网', '{}', '{}');"
        self.request = Query().run
        self.soup = DealSoup().judge
        self.init_sql()
        self.pattern = re.compile(
            r'"fenXiangName":"金额","fenXiangValue":"([0-9]*)"')

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
            sql = "SELECT `id` FROM `bidpython`.`tb_bid` WHERE `inviter_number` = '{}' and `platform_id` = 22 LIMIT 1;"
        elif self.bid_type == "bidResult":
            sql = "SELECT `id` FROM `bidpython`.`tb_bid_result` WHERE `inviter_number` = '{}' and `platform_id` = 22 LIMIT 1;"

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
        resp = run_func(
            self.request,
            self.bid_path,
            header=self.header,
            data=
            f'currentPage={page}&caiGouType=0&xiangMuBianHao=&xiangMuName=&caiGouRenName=&danWeiName='
        )
        table = self.soup(resp, attr={'class': 'zbgg_table'})
        trs = self.soup(table, 'tr', all_tag=True)[2:]

        for tr in trs:
            info = {}
            tds = self.soup(tr, 'td', all_tag=True)
            _id = tds[1].a.get('onclick').split(',')[-1].replace(')',
                                                                 '').replace(
                                                                     '\'', '')

            info[
                'path'] = f'https://dzzb.ciesco.com.cn/xjcg/xjcgDetail?guid={_id}'

            info["网上竞价编号"] = tds[1].a.text
            info["网上竞价名称"] = tds[2].a.text

            if not self.judge_already(info["网上竞价编号"]):
                continue

            info["采购人"] = tds[3].a.text

            resp = run_func(
                self.request,
                f'https://common.dzzb.ciesco.com.cn/xunjia/common/nofilter/queryXiangMuByGuid.do?guid={_id}',
                header=self.header)

            detail = json.loads(resp)

            info["竞价开始时间"] = detail.get('gongGaoStartTimeTextDeleteSecond')
            info["竞价截止时间"] = detail.get('baoJiaEndTimeTextDeleteSecond')
            info['金额上限'] = ''

            if detail.get('lsBaoJian'):
                data = detail.get('lsBaoJian')[0].get('lsMingXiData')
                tr_json = []
                for index, item in enumerate(data):
                    tr_json.append({
                        "参数": "",
                        "单位": item.get('danWei'),
                        "招标编号": info["网上竞价编号"],
                        "序号": index + 0,
                        "产品名称": item.get('mingCheng'),
                        "产品类别": "",
                        "产品单价": '',
                        "合计": '',
                        "品牌": "",
                        "数量": item.get('shuLiang'),
                        "标配": "",
                        "型号": '',
                        "url": info['path'],
                        "招标平台": "招商局集团电子招标采购交易网",
                        "售后服务": "",
                    })
            else:
                tr_json = [{
                    "参数": "",
                    "单位": '',
                    "招标编号": info["网上竞价编号"],
                    "序号": 1,
                    "产品名称": '',
                    "产品类别": "",
                    "产品单价": '',
                    "合计": '',
                    "品牌": "",
                    "数量": '',
                    "标配": "",
                    "型号": '',
                    "url": info['path'],
                    "招标平台": "招商局集团电子招标采购交易网",
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
        resp = run_func(
            self.request,
            self.result_path,
            header=self.header,
            data=
            f'currentPage={page}&caiGouType=0&xiangMuBianHao=&xiangMuName=&caiGouRenName=&danWeiName='
        )

        table = self.soup(resp, attr={'class': 'zbgg_table'})
        trs = self.soup(table, 'tr', all_tag=True)[2:]

        for tr in trs:
            info = {}
            tds = self.soup(tr, 'td', all_tag=True)
            href = tds[1].a.get('href')

            info['path'] = f'https://dzzb.ciesco.com.cn{href}'

            info["网上竞价编号"] = tds[1].a.text
            info["网上竞价名称"] = tds[2].a.text

            if not self.judge_already(info["网上竞价编号"]):
                continue

            info["采购人"] = tds[4].a.text

            resp = run_func(
                self.request,
                f'https://common.dzzb.ciesco.com.cn/xunjia/common/nofilter/queryCGGLJieGuoByGuid.do?guid={href.split("=")[-1]}',
                header=self.header)

            detail = json.loads(resp)

            info["竞价开始时间"] = detail.get('gongGaoStartTimeTextDeleteSecond')
            info["竞价截止时间"] = detail.get('baoJiaEndTimeTextDeleteSecond')
            info['金额上限'] = ''

            info["成交公告时间"] = detail.get('gongShiStartTimeText')
            info["竞价开始时间"] = ''
            info["竞价截至时间"] = ''

            result = re.search(self.pattern, resp)
            if result:
                info["中标总额"] = result.group(1)
            else:
                info["中标总额"] = ''
            info['中标公司'] = detail.get('gongYingShangNameOne')

            tr_json = [{
                "成交时间": "",
                "招标编号": info["网上竞价编号"],
                "规格配置": '',
                "详情url": info["path"],
                "平台名称": "招商局集团电子招标采购交易网",
                "总价": info["中标总额"],
                "中标供应商": info['中标公司'],
                "设备名称": '',
                "创建时间": self.get_time(),
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

    def run(self, path):
        resp = run_func(self.request, path, header=self.header)
        data = json.loads(resp)
        for item in data["aaData"]:
            if run_func(self.judge_already, item["reverseAuctionCode"]):
                if self.bid_type == "bidNeed":
                    run_func(self.deal_detail, item["id"])
                elif self.bid_type == "bidResult":
                    run_func(self.deal_result, item["id"])
            else:
                logger.info("--->Info: existed already")

    def main(self):
        for page in range(5, 11):
            self.bid_type = "bid"
            run_func(self.deal_detail, page)
            self.bid_type = "bidResult"
            run_func(self.deal_result, page)


if __name__ == "__main__":
    os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    DealCiesco().main()

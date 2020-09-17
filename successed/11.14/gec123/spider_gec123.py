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
        self.bid_path = "https://www.gec123.com/xcjenquiry/api/v1/packages?pi={}&ps=12&publishSite=1"
        self.bid_detail = "https://www.gec123.com/xcjenquiry/notice!enquiryNotice.action?notic_seq={}"
        self.result_path = "https://www.gec123.com/xcjenquiry/api/v1/packages?pi={}&ps=12&states=7"
        self.result_detail = "https://www.gec123.com/xcj-gateway/api/v1/notices/stable/{}"
        self.header = {
            "Host":
            "www.gec123.com",
            "Sec-Fetch-Mode":
            "cors",
            "X-Requested-With":
            "XMLHttpRequest",
            "User-Agent":
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.120 Safari/537.36",
            "Accept":
            "*/*",
            "Sec-Fetch-Site":
            "same-origin",
            "Referer":
            "https://www.gec123.com/notices/list",
            # "https://www.gec123.com/enquiries/list",
            "Accept-Encoding":
            "gzip, deflate, br",
            "Accept-Language":
            "zh-CN,zh;q=0.9",
            "Cookie":
            "Hm_lvt_b9a59f93d355dbc81937a9a9ae094db0=1573036848; JSESSIONID=0A60DD7AFA7CAC04861EAEA4EEA63FB2-n2; Hm_lpvt_b9a59f93d355dbc81937a9a9ae094db0=1573098974"
        }

        self.insert_tb_bid = "INSERT INTO `bidpython`.`tb_bid` ( `title`, `inviter_number`, `announce_time`, `end_time`, `budget_money`, `platform_id`, `url`, `company` ) VALUES ( '{网上竞价名称}', '{网上竞价编号}', '{竞价开始时间}', '{竞价截止时间}', '{金额上限}', 16, '{path}', '{采购人}' );"
        self.insert_bid_result = "INSERT INTO `bidpython`.`tb_bid_result` ( `title`, `inviter_number`, `announce_time`, `end_time`, `announce_date`, `platform_id`, `url`, `company`, `budget_money`, `announce_company` ) VALUES ( '{网上竞价名称}', '{网上竞价编号}', '{竞价开始时间}', '{竞价截至时间}', '{成交公告时间}', 16, '{path}', '{采购人}', '{中标总额}', '{中标公司}' );"
        self.insert_bid_json = insert_sql = "INSERT INTO `bidpython`.`tb_bid_json` ( `shot`, `platform_name`, `inviter_number`, `url`, `json_kv`, `create_time` ) VALUES ( '', '行采家', '{}', '{}', '{}', '{}');"
        self.insert_tr_json = insert_sql = "INSERT INTO `bidpython`.`tb_tr_json` ( `platform_id`, `platform_name`, `tr_json`, `url` ) VALUES ( 16, '行采家', '{}', '{}');"
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

    def ergodic_tr(self, tr_objs: BeautifulSoup, item_code=""):
        tr_list = tr_objs.contents
        index = 1
        info = []
        for tr_obj in tr_list:
            if isinstance(tr_obj, str):
                continue
            else:
                text = tr_obj.text
                if "商品名称" not in text and "计量单位" not in text:
                    temp_good = text.split("\n")
                    if self.bid_type == "bidNeed":
                        info.append({
                            "参数": "",
                            "单位": "",
                            "招标编号": item_code,
                            "序号": index + 1,
                            "产品名称": temp_good[1],
                            "产品类别": "",
                            "产品单价": temp_good[4],
                            "合计": temp_good[5],
                            "品牌": "",
                            "数量": temp_good[3],
                            "标配": "",
                            "型号": temp_good[2],
                            "url": self.path,
                            "招标平台": "行采家",
                            "售后服务": "",
                        })
                    elif self.bid_type == "bidResult":
                        info.append({
                            "规格配置": "",
                            "中标供应商": temp_good[6],
                            "设备名称": temp_good[1],
                            "品牌": "",
                            "售后服务": "",
                            "中标总价": temp_good[5],
                            "型号": "",
                            "数量": temp_good[3],
                        })
                    index += 1

        return info

    def judge_already(self, item_code):
        if self.bid_type == "bid":
            sql = "SELECT `id` FROM `bidpython`.`tb_bid` WHERE `inviter_number` = '{}' and `platform_id` = 16 LIMIT 1;"
        elif self.bid_type == "bidResult":
            sql = "SELECT `id` FROM `bidpython`.`tb_bid_result` WHERE `inviter_number` = '{}' and `platform_id` = 16 LIMIT 1;"

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

    def deal_detail(self, page):
        resp = run_func(self.request,
                        self.bid_path.format(page),
                        header=self.header)
        data = json.loads(resp)["packages"]

        for item in data:
            info = {}
            path = self.bid_detail.format(item["noticeId"])
            resp = run_func(self.request, path, header=self.header)
            raw_obj = run_func(self.soup, resp)
            item_id = run_func(self.soup,
                               raw_obj,
                               attr={
                                   "class": "enquiry-no"
                               }).text

            info["网上竞价编号"] = self.remove_character(item_id)

            if not self.judge_already(info["网上竞价编号"]):
                continue

            info["网上竞价名称"] = item["noticeName"]
            info["金额上限"] = item["totalLimit"]
            info["path"] = path

            info["采购人"] = self.soup(resp, {
                'id': 'center_left_wrap'
            }).text.replace('\n', '')

            info["竞价开始时间"] = time.strftime(
                '%Y-%m-%d %H:%M:%S',
                time.localtime(int(item['enqStartTime']) / 1000))
            info["竞价截止时间"] = time.strftime(
                '%Y-%m-%d %H:%M:%S',
                time.localtime(int(item['enqEndTime']) / 1000))

            tr_json = []
            binding = self.soup(resp, {'class': 'text-bold ng-binding'}, True)

            tr_json.append({
                "参数": "",
                "单位": self.remove_character(binding[1].text.split('(')[-1]),
                "招标编号": info["网上竞价编号"],
                "序号": 1,
                "产品名称": item.get('goodsDirectory'),
                "产品类别": "",
                "产品单价": self.remove_character(binding[0].text[1:]),
                "合计": self.remove_character(binding[2].text[1:]),
                "品牌": "",
                "数量": self.remove_character(binding[1].text.split('(')[0]),
                "标配": "",
                "型号": '',
                "url": path,
                "招标平台": "行采家",
                "售后服务": "",
            })

            run_func(self.ecnu_cursor.execute,
                     self.insert_tb_bid.format(**info))

            run_func(
                self.ecnu_cursor.execute,
                self.insert_bid_json.format(
                    info["网上竞价编号"], info["path"],
                    json.dumps(tr_json, ensure_ascii=False), self.get_time()))
            # info = {
            #     "网上竞价编号": item_id,
            #     "网上竞价名称": item["noticeName"],
            #     "采购人": data["collegeName"],
            #     "竞价开始时间": data["startBidtime"],
            #     "竞价截止时间": data["endBidtime"],
            #     "金额上限": data["budget"],
            #     "path": page_path
            # }

    def deal_result(self, page):
        path = self.result_path.format(page)
        resp = run_func(self.request, path, header=self.header)
        data = json.loads(resp)["packages"]

        for item in data:
            if item['result'] != 1:
                continue

            info = {}
            path = f'https://www.gec123.com/xcjenquiry/notice!enquiryNotice.action?notic_seq={item.get("noticeId")}'
            resp = run_func(self.request, path, header=self.header)

            no = self.soup(resp, {'class': 'enquiry-no'})

            info["网上竞价编号"] = self.remove_character(no.text)

            if not self.judge_already(info["网上竞价编号"]):
                continue

            info["网上竞价名称"] = item["noticeName"]
            info["采购人"] = self.soup(resp, {
                'id': 'center_left_wrap'
            }).text.replace('\n', '')
            info["path"] = path

            info["中标公司"] = item.get('providerOrgName')

            info["成交公告时间"] = time.strftime(
                '%Y-%m-%d %H:%M:%S',
                time.localtime(int(item.get('publishTime')) / 1000))
            info["竞价开始时间"] = ""
            info["竞价截至时间"] = ""

            info["中标总额"] = item.get('totalLimit')

            tr_json = []
            binding = self.soup(resp, {'class': 'text-bold ng-binding'}, True)

            tr_json.append({
                "成交时间": "",
                "招标编号": info["网上竞价编号"],
                "规格配置": '',
                "详情url": info["path"],
                "平台名称": "重庆市政府采购云平台",
                "总价": self.remove_character(binding[2].text[1:]),
                "中标供应商": info["中标公司"],
                "设备名称": item.get('goodsDirectory'),
                "创建时间": self.get_time(),
                "品牌": '',
                "型号": '',
                "数量": self.remove_character(binding[1].text.split('(')[0])
            })

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
        for page in range(1, 15):
            self.bid_type = "bid"
            self.deal_detail(page)
            self.bid_type = "bidResult"
            self.deal_result(page)


if __name__ == "__main__":
    os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    DealGec().main()

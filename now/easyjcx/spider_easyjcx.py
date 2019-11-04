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


class DealEasyjcx(object):
    def __init__(self):

        self.result_path = "http://sdzfcg.shunde.gov.cn/sdcgpt/front/front!{type}Info.action?id={id}"
        self.header = {
            "Host": "api.easyjcx.com",
            "Accept": "application/json, text/plain, */*",
            "Origin": "https://www.easyjcx.com",
            "User-Agent":
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.120 Safari/537.36",
            "Sec-Fetch-Mode": "cors",
            "Content-Type": "application/json;charset=UTF-8",
            "Sec-Fetch-Site": "same-site",
            "Referer": "https://www.easyjcx.com/",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "zh-CN,zh;q=0.9"
        }

        self.insert_tb_bid = "INSERT INTO `bidpython`.`tb_bid` ( `title`, `inviter_number`, `announce_time`, `end_time`, `budget_money`, `platform_id`, `url`, `company` ) VALUES ( '{网上竞价名称}', '{网上竞价编号}', '{竞价开始时间}', '{竞价截止时间}', '{金额上限}', 15, '{path}', '{采购人}' );"
        self.insert_bid_result = "INSERT INTO `bidpython`.`tb_bid_result` ( `title`, `inviter_number`, `announce_time`, `end_time`, `announce_date`, `platform_id`, `url`, `company`, `count`, `announce_company` ) VALUES ( '{网上竞价名称}', '{网上竞价编号}', '{竞价开始时间}', '{竞价截至时间}', '{成交公告时间}', 15, '{path}', '{采购人}', '{中标总额}', '{中标公司}' );"
        self.insert_bid_json = insert_sql = "INSERT INTO `bidpython`.`tb_bid_json` ( `shot`, `platform_name`, `inviter_number`, `url`, `json_kv`, `create_time` ) VALUES ( '', '竞采星 竞价采购网', '{}', '{}', '{}', '{}');"
        self.insert_tr_json = insert_sql = "INSERT INTO `bidpython`.`tb_tr_json` ( `platform_id`, `platform_name`, `tr_json`, `url` ) VALUES ( 15, '竞采星 竞价采购网', '{}', '{}');"
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
                    if self.bid_type is "bidNeed":
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
                            "招标平台": "竞采星 竞价采购网",
                            "售后服务": "",
                        })
                    elif self.bid_type is "bidResult":
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
        if self.bid_type is "bidNeed":
            sql = "SELECT `id` FROM `bidpython`.`tb_bid` WHERE `inviter_number` = '{}' LIMIT 1;"
        elif self.bid_type is "bidResult":
            sql = "SELECT `id` FROM `bidpython`.`tb_bid_result` WHERE `inviter_number` = '{}' LIMIT 1;"

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

    def deal_detail(self, item_id):
        path = "https://api.easyjcx.com/api/portalCli/{}/detail".format(
            self.bid_type)
        resp = run_func(
            self.request,
            path,
            header=self.header,
            data={"orderMainId": item_id})
        data = json.loads(resp)["data"]

        page_path = "https://www.easyjcx.com/#/purchase/detail/{}".format(
            item_id)

        info = {
            "网上竞价编号":
            data["orderCode"],
            "网上竞价名称":
            "{} - 竞价公告 ({})".format(data["collegeName"], data["orderCode"]),
            "采购人":
            data["collegeName"],
            "竞价开始时间":
            data["startBidtime"],
            "竞价截止时间":
            data["endBidtime"],
            "金额上限":
            data["budget"],
            "path":
            page_path
        }

        tr_json = []
        for index, item in enumerate(data["detailList"]):
            tr_json.append({
                "参数": "",
                "单位": "",
                "招标编号": data["orderCode"],
                "序号": index,
                "产品名称": item["deviceName"],
                "产品类别": "",
                "产品单价": item["detailBudget"],
                "合计": "",
                "品牌": item["deviceBrand"],
                "数量": item["orderNum"],
                "标配": "",
                "型号": item["deviceModel"],
                "url": page_path,
                "招标平台": "竞采星 竞价采购网",
                "售后服务": "",
            })

        run_func(self.ecnu_cursor.execute, self.insert_tb_bid.format(**info))

        run_func(
            self.ecnu_cursor.execute,
            self.insert_bid_json.format(
                data["orderCode"], path, json.dumps(
                    tr_json, ensure_ascii=False), self.get_time()))

    def deal_result(self, item_id):
        path = "https://api.easyjcx.com/api/portalCli/{}/detail".format(
            self.bid_type)
        resp = run_func(
            self.request,
            path,
            header=self.header,
            data={"orderMainId": item_id})
        data = json.loads(resp)["data"]

        page_path = "https://www.easyjcx.com/#/auction/detail/{}".format(
            item_id)

        info = {
            "网上竞价名称":
            "{} - 竞价结果公告 ({})".format(data["collegeName"], data["orderCode"]),
            "网上竞价编号":
            data["orderCode"],
            "采购人":
            data["collegeName"],
            "中标公司":
            data["detailList"][0]["companyName"],
            "path":
            page_path,
            "成交公告时间":
            data["publishBidresultTime"],
            "竞价开始时间":
            data["startBidtime"],
            "竞价截至时间":
            data["endBidtime"],
            "中标总额":data["bidAmount"]
        }

        tr_json = []
        for item in data["detailList"]:
            tr_json.append({
                "成交时间": info["成交公告时间"],
                "招标编号": data["orderCode"],
                "规格配置": item["deviceSpec"],
                "详情url": page_path,
                "平台名称": "竞采星 竞价采购网",
                "总价": item["bidAmount"],
                "中标供应商": item["companyName"],
                "设备名称": item["deviceName"],
                "创建时间": self.get_time(),
                "品牌": "",
                "型号": "",
                "数量": item["orderNum"]
            })

        run_func(self.ecnu_cursor.execute,
                 self.insert_bid_result.format(**info))

        run_func(
            self.ecnu_cursor.execute,
            self.insert_tr_json.format(
                json.dumps(tr_json, ensure_ascii=False), path))

    def run(self, path):
        resp = run_func(self.request, path, header=self.header)
        data = json.loads(resp)
        for item in data["aaData"]:
            if run_func(self.judge_already, item["reverseAuctionCode"]):
                if self.bid_type is "bidNeed":
                    run_func(self.deal_detail, item["id"])
                elif self.bid_type is "bidResult":
                    run_func(self.deal_result, item["id"])
            else:
                logger.info("--->Info: existed already")

    def main(self):
        for self.bid_type in ["bidNeed", "bidResult"]:
            for page in range(1, 2):
                data = {
                    "keyword": "",
                    "current": page,
                    "size": 10,
                    "condition": {
                        "areaScope": "",
                        "procurementType": "",
                        "sourceType": "",
                        "collegeNameList": [],
                        "startBidresultTime": "",
                        "endBidresultTime": ""
                    }
                }

                resp = run_func(
                    self.request,
                    "https://api.easyjcx.com/api/portalCli/{}".format(
                        self.bid_type),
                    header=self.header,
                    data=data)
                data = json.loads(resp)

                for item in data["data"]["records"]:
                    if run_func(self.judge_already, item["orderCode"]):
                        if self.bid_type is "bidNeed":
                            run_func(self.deal_detail, item["orderMainId"])
                        elif self.bid_type is "bidResult":
                            run_func(self.deal_result, item["orderMainId"])


if __name__ == "__main__":
    os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    DealEasyjcx().main()

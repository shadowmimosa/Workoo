import os
import re
import time
import json
import pymysql
from bs4 import BeautifulSoup

from config import DEBUG, logger
from utils.run import run_func
from utils.request import Query
from utils.soup import DealSoup


class DealZcy(object):
    def __init__(self):
        self.path = "https://sourcing.zhengcaiyun.cn/api/inquiry/external/seekSource/announcement/page"
        self.bid_path = "https://reversehall.zcygov.cn/api/reverse/announcement/salaQuotePaging"
        self.bid_detail = "https://reversehall.zcygov.cn/detail?id={}"
        self.result_path = "https://reversehall.zcygov.cn/api/reverse/announcement/salaResultPaging"
        self.result_detail = "https://reversehall.zcygov.cn/detail?id={}"
        self.header = {
            'Accept': "application/json, text/javascript, */*; q=0.01",
            "User-Agent":
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.120 Safari/537.36",
            "Content-Type": "application/json;charset=UTF-8",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "zh-CN,zh;q=0.9",
        }
        self.detail_header = {
            'Accept': "application/json, text/javascript, */*; q=0.01",
            "User-Agent":
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.120 Safari/537.36",
            "Content-Type": "application/json;charset=UTF-8",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "zh-CN,zh;q=0.9",
        }

        self.insert_tb_bid = "INSERT INTO `bidpython`.`tb_bid` ( `title`, `inviter_number`, `announce_time`, `end_time`, `budget_money`, `platform_id`, `url`, `company` ) VALUES ( '{网上竞价名称}', '{网上竞价编号}', '{竞价开始时间}', '{竞价截止时间}', '{金额上限}', 17, '{path}', '{采购人}' );"
        self.insert_bid_result = "INSERT INTO `bidpython`.`tb_bid_result` ( `title`, `inviter_number`, `announce_time`, `end_time`, `announce_date`, `platform_id`, `url`, `company`, `budget_money`, `announce_company` ) VALUES ( '{网上竞价名称}', '{网上竞价编号}', '{竞价开始时间}', '{竞价截止时间}', '{成交公告时间}', 17, '{path}', '{采购人}', '{中标总额}', '{中标公司}' );"
        self.insert_bid_json = insert_sql = "INSERT INTO `bidpython`.`tb_bid_json` ( `shot`, `platform_name`, `inviter_number`, `url`, `json_kv`, `create_time` ) VALUES ( '', '政府采购云', '{}', '{}', '{}', '{}');"
        self.insert_tr_json = insert_sql = "INSERT INTO `bidpython`.`tb_tr_json` ( `platform_id`, `platform_name`, `tr_json`, `url` ) VALUES ( 17, '政府采购云', '{}', '{}');"

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
                            "招标平台": "政府采购云",
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
        if self.bid_type == "PUBLISHING":
            sql = "SELECT `id` FROM `bidpython`.`tb_bid` WHERE `inviter_number` = '{}' and `platform_id` = 17 LIMIT 1;"
        elif self.bid_type == "RESULT":
            sql = "SELECT `id` FROM `bidpython`.`tb_bid_result` WHERE `inviter_number` = '{}' and `platform_id` = 17 LIMIT 1;"

        if run_func(self.ecnu_cursor.execute, sql.format(item_code)) == 0:
            return True
        else:
            return

    def get_time(self, timestamps=0):
        if timestamps == 1:
            return int(time.time() * 1000)
        return time.strftime('%Y-%m-%d %H:%M:%S',
                             time.localtime(int(time.time())))

    def to_date(self, timestamps):
        return time.strftime('%Y-%m-%d %H:%M:%S',
                             time.localtime(timestamps / 1000))

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
                               "").replace("\r",
                                           "").replace(" ",
                                                       "").replace(")", "")

    def deal_detail(self, item):
        path = self.bid_detail.format(item["id"])

        uri = f'https://reversehall.zcygov.cn/api/reverse/announcement/queryRequireNotice?requireId={item["id"]}&_={self.get_time(1)}'
        resp = run_func(self.request, uri, header=self.detail_header)

        data = json.loads(resp)
        info = {}

        info["网上竞价编号"] = data.get("code")
        info["网上竞价名称"] = data.get("title")

        info["竞价开始时间"] = self.to_date(data.get("startTime"))
        info["竞价截止时间"] = self.to_date(data.get("endTime"))
        info["采购人"] = data.get("orgName")
        info["金额上限"] = data.get("startMoney") / 100
        info["path"] = path

        tr_json = []

        for index, good in enumerate(data.get("raItemDto")):

            tr_json.append({
                "参数": good.get("mainAttributes"),
                "单位": good.get("unit"),
                "招标编号": info["网上竞价编号"],
                "序号": index + 1,
                "产品名称": good.get("productCatalogName"),
                "产品类别": "",
                "产品单价": "",
                "合计": good.get("controllerPrice"),
                "品牌": good.get("brand"),
                "数量": good.get("quantity"),
                "标配": "",
                "型号": good.get("model"),
                "url": path,
                "招标平台": "政府采购云",
                "售后服务": "",
            })

        run_func(self.ecnu_cursor.execute, self.insert_tb_bid.format(**info))

        run_func(
            self.ecnu_cursor.execute,
            self.insert_bid_json.format(
                info["网上竞价编号"], info["path"],
                json.dumps(tr_json, ensure_ascii=False), self.get_time()))

    def deal_result(self, item):
        path = self.result_detail.format(item["id"])

        uri = f'https://reversehall.zcygov.cn/api/reverse/announcement/queryRequireQuoteResult?requireId={item["id"]}&_={self.get_time(1)}'
        resp = run_func(self.request, uri, header=self.detail_header)

        data = json.loads(resp)

        info = {}

        info["网上竞价名称"] = data.get("title")
        info["成交公告时间"] = self.to_date(data.get("endTime"))

        info["网上竞价编号"] = data.get("code")
        info["竞价开始时间"] = self.to_date(data.get("startTime"))
        info["竞价截止时间"] = self.to_date(data.get("endTime"))

        info["采购人"] = data.get("orgName")
        info["path"] = path

        info["中标公司"] = data.get("raSupplierDtoList")[0].get("supName")
        info["中标总额"] = data.get("raSupplierDtoList")[0].get("totalPrice") / 100

        tr_json = []

        for good in data.get("raItemDto"):
            tr_json.append({
                "成交时间": "",
                "招标编号": info["网上竞价编号"],
                "规格配置": good.get("mainAttributes"),
                "详情url": info["path"],
                "平台名称": "政府采购云",
                "单价": good.get("controllerPrice"),
                "中标供应商": info["中标公司"],
                "设备名称": good.get("productCatalogName"),
                "创建时间": self.get_time(),
                "品牌": good.get("brand"),
                "型号": good.get("model"),
                "数量": good.get("quantity")
            })

        run_func(self.ecnu_cursor.execute,
                 self.insert_bid_result.format(**info))

        run_func(
            self.ecnu_cursor.execute,
            self.insert_tr_json.format(json.dumps(tr_json, ensure_ascii=False),
                                       info["path"]))

    def run(self, data):
        if self.bid_type == "PUBLISHING":
            path = self.bid_path
        else:
            path = self.result_path

        resp = run_func(self.request, path, header=self.header, data=data)
        data = json.loads(resp)
        for item in data["result"]["result"]:
            if run_func(self.judge_already, item["id"]):
                if self.bid_type == "PUBLISHING":
                    run_func(self.deal_detail, item)
                elif self.bid_type == "RESULT" and item["state"] == 11:
                    run_func(self.deal_result, item)
            else:
                logger.info("--->Info: existed already")

    def main(self):
        for page in range(1, 15):
            for self.bid_type in ["PUBLISHING", "RESULT"]:
                data = {"pageSize": "10", "title": "", "pageNo": page}
                self.run(data)


if __name__ == "__main__":
    os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    DealZcy().main()

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


class DealShunde(object):
    def __init__(self):
        self.page_path = "http://sdzfcg.shunde.gov.cn/sdcgpt/front/front!listMore{type}.action?draw={draw}&columns[0][data]=id&columns[0][name]=&columns[0][searchable]=true&columns[0][orderable]=false&columns[0][search][value]=&columns[0][search][regex]=false&start={start}&length=10&search[value]=&search[regex]=false&sname=&begin=&end=&_={timestamps}"
        self.detail_path = "http://sdzfcg.shunde.gov.cn/sdcgpt/front/front!{type}Info.action?id={id}"
        self.header = {
            "Host":
            "sdzfcg.shunde.gov.cn",
            "Upgrade-Insecure-Requests":
            "1",
            "User-Agent":
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36",
            "Accept":
            "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3",
            # "Accept": "application/json, text/javascript, */*; q=0.01",
            "Referer":
            "http://sdzfcg.shunde.gov.cn/sdcgpt/front/front!moreSuccess.action",
            "Accept-Encoding":
            "gzip, deflate",
            "Accept-Language":
            "zh-CN,zh;q=0.9",
            "Cookie":
            "JSESSIONID=450C2DEFD69EC1D27362191456483C0E; safedog-flow-item="
        }

        self.insert_tb_bid = "INSERT INTO `bidpython`.`tb_bid` ( `title`, `inviter_number`, `announce_time`, `end_time`, `budget_money`, `platform_id`, `url`, `company` ) VALUES ( '{网上竞价名称}', '{网上竞价编号}', '{竞价开始时间}', '{竞价截止时间}', '{金额上限}', 14, '{path}', '{采购人}' );"
        self.insert_bid_result = "INSERT INTO `bidpython`.`tb_bid_result` ( `title`, `inviter_number`, `announce_date`, `platform_id`, `url`, `company`, `announce_result` ) VALUES ( '{网上竞价名称}', '{网上竞价编号}', '{成交公告时间}', 14, '{path}', '{采购人}', '{中标公司}' );"
        self.insert_bid_json = insert_sql = "INSERT INTO `bidpython`.`tb_bid_json` ( `shot`, `platform_name`, `inviter_number`, `url`, `json_kv`, `create_time` ) VALUES ( '', '顺德电子化采购平台', '{}', '{}', '{}', '{}');"
        self.insert_tr_json = insert_sql = "INSERT INTO `bidpython`.`tb_tr_json` ( `platform_id`, `platform_name`, `tr_json`, `url` ) VALUES ( 14, '顺德电子化采购平台', '{}', '{}');"

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
                    info["金额上限"] = text.split(("："))[-1]

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
                    if self.bid_type is "Notice":
                        info.append({
                            "参数": "",
                            "单位": temp_good[1],
                            "招标编号": item_code,
                            "序号": index,
                            "产品名称": temp_good[0],
                            "产品类别": "",
                            "品牌": temp_good[2],
                            "数量": temp_good[3],
                            "标配": "",
                            "型号": temp_good[2],
                            "url": self.path,
                            "招标平台": "顺德电子化采购平台",
                            "售后服务": "",
                        })
                    elif self.bid_type is "Success":
                        info.append({
                            "规格配置": "",
                            "中标供应商": temp_good[4],
                            "设备名称": temp_good[0],
                            "品牌": "",
                            "售后服务": "",
                            "中标单价": temp_good[3],
                            "型号": "",
                            "数量": temp_good[2],
                        })
                    index += 1

        return info

    def judge_already(self, item_code):
        if self.bid_type is "Notice":
            sql = "SELECT `id` FROM `bidpython`.`tb_bid` WHERE `inviter_number` = '{}' LIMIT 1;"
        elif self.bid_type is "Success":
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
        self.path = self.detail_path.format(**{
            "type": self.bid_type.lower(),
            "id": item_id
        })
        resp = run_func(self.request, self.path, header=self.header)

        raw_obj = run_func(self.soup, resp)
        a112_obj = run_func(self.soup, raw_obj, attr={"id": "all2"})
        t1_obj = run_func(self.soup, raw_obj, attr={"id": "t1"})
        a113_obj = run_func(self.soup, raw_obj, attr={"id": "all3"})

        info = run_func(self.ergodic_p, a112_obj)
        info["path"] = self.path
        item_code = info["网上竞价编号"]

        # if run_func(self.judge_already, item_code):

        # self.info = {
        #     "网上竞价编号": "",
        #     "网上竞价名称": "",
        #     "采购人": "",
        #     "联系人": "",
        #     "联系电话": "",
        #     "竞价开始时间": "",
        #     "竞价截止时间": "",
        #     "品目类型": "",
        #     "金额上限": "",
        # }
        tr_json = json.dumps(
            self.ergodic_tr(t1_obj, item_code), ensure_ascii=False)
        run_func(self.ecnu_cursor.execute,
                    self.insert_tb_bid.format(**info))

        run_func(
            self.ecnu_cursor.execute,
            self.insert_bid_json.format(item_code, self.path, tr_json,
                                        self.get_time()))

    def deal_result(self, item_id):
        self.path = self.detail_path.format(**{
            "type": self.bid_type.lower(),
            "id": item_id
        })
        resp = run_func(self.request, self.path, header=self.header)

        raw_obj = run_func(self.soup, resp)
        a112_obj = run_func(self.soup, raw_obj, attr={"id": "all2"})
        t1_obj = run_func(self.soup, raw_obj, attr={"id": "t1"})
        a113_obj = run_func(self.soup, raw_obj, attr={"id": "all3"})
        temp_tr_json = run_func(self.ergodic_tr, t1_obj)

        info = {
            "网上竞价名称":
            re.search(r'<p style="text-align:center;font-size:30px;">.*</p>',
                      resp).group().replace(
                          r'<p style="text-align:center;font-size:30px;">',
                          "").replace(r'</p>', ""),
            "网上竞价编号":
            re.search("（网上竞价编号：.*）", a112_obj.text).group().replace(
                "（网上竞价编号：", "").replace("）", ""),
            "采购人":
            a112_obj.text.split("（以下简称“采购人”）")[0],
            "成交公告时间":
            re.search(
                r"([0-9]{3}[1-9]|[0-9]{2}[1-9][0-9]{1}|[0-9]{1}[1-9][0-9]{2}|[1-9][0-9]{3})-.*-.* .*:.*:.*",
                resp).group(),
            "中标公司":
            json.dumps(temp_tr_json, ensure_ascii=False),
            "path":
            self.path
        }
        item_code = info["网上竞价编号"]

        # if run_func(self.judge_already, item_code):
        tr_json = []
        for temp_ in temp_tr_json:
            tr_json.append({
                "成交时间": info["成交公告时间"],
                "招标编号": item_code,
                "规格配置": "",
                "详情url": self.path,
                "平台名称": "顺德电子化采购平台",
                "单价": temp_["中标单价"],
                "中标供应商": temp_["中标供应商"],
                "设备名称": temp_["设备名称"],
                "创建时间": self.get_time(),
                "品牌": "",
                "型号": "",
                "数量": temp_["数量"]
            })

        run_func(self.ecnu_cursor.execute,
                    self.insert_bid_result.format(**info))

        run_func(
            self.ecnu_cursor.execute,
            self.insert_tr_json.format(
                json.dumps(tr_json, ensure_ascii=False), self.path))

    def main(self, path):
        resp = run_func(self.request, path, header=self.header)
        data = json.loads(resp)
        for item in data["aaData"]:
            if run_func(self.judge_already, item["reverseAuctionCode"]):
                if self.bid_type is "Notice":
                    run_func(self.deal_detail, item["id"])
                elif self.bid_type is "Success":
                    run_func(self.deal_result, item["id"])
            else:
                logger.info("--->Info: existed already")

    def run(self):
        for self.bid_type in ["Notice", "Success"]:
            for page in range(0, 1):
                run_func(
                    self.main,
                    self.page_path.format(
                        **{
                            "type": self.bid_type,
                            "draw": 1,
                            "start": page * 10,
                            "timestamps": 1569649897414
                        }))


if __name__ == "__main__":
    os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    DealShunde().run()
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


class DealZcy(object):
    def __init__(self):
        self.path = "https://sourcing.zhengcaiyun.cn/api/inquiry/external/seekSource/announcement/page"
        self.bid_path = "https://www.gec123.com/xcjenquiry/api/v1/packages?pi={}&ps=12&publishSite=1"
        self.bid_detail = "https://www.gec123.com/xcjenquiry/notice!enquiryNotice.action?notic_seq={}"
        self.result_path = "https://www.gec123.com/xcj-gateway/api/v1/notices/stable?pi={}&projectPurchaseWay=6003&ps=12&publishSite=1&sourceType=2&type=306,300,307"
        self.result_detail = "https://www.gec123.com/xcj-gateway/api/v1/notices/stable/{}"
        self.header = {
            "Host":
            "sourcing.zhengcaiyun.cn",
            "Accept":
            "application/json, text/plain, */*",
            "Origin":
            "https://sourcing.zhengcaiyun.cn",
            "X-Requested-With":
            "XMLHttpRequest",
            "User-Agent":
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.120 Safari/537.36",
            "Sec-Fetch-Mode":
            "cors",
            "Content-Type":
            "application/json;charset=UTF-8",
            "Sec-Fetch-Site":
            "same-origin",
            "Referer":
            "https://sourcing.zhengcaiyun.cn/luban/sourcing/inquiry?utm=a0017.2ef5001f.cl15.2.91aedb1006be11ea875633e233d0737d&typeEnum=PUBLISHING",
            "Accept-Encoding":
            "gzip, deflate, br",
            "Accept-Language":
            "zh-CN,zh;q=0.9",
            "Cookie":
            "_zcy_log_client_uuid=a4ec4b60-053b-11ea-ab1d-d559326808ef; portalDistrictCode=339900; portalDistrictName=%E6%B5%99%E6%B1%9F%E7%9C%81%E6%9C%AC%E7%BA%A7; acw_tc=76b20ff815735566251203293e7e599c2188b5eb736c7e93ab3e1da70a2022; districtCode=901901; districtName=%E6%B5%99%E6%B1%9F%E7%9C%81%E5%86%9B%E5%8C%BA; UM_distinctid=16e5fb593f79e-0ef6185d9c79a3-b363e65-1fa400-16e5fb593f816c; _dg_check.bbc15f7dfd2de351.2fc2=-1; _dg_playback.bbc15f7dfd2de351.2fc2=1; _dg_id.bbc15f7dfd2de351.2fc2=aae8067d49aa5ead%7C%7C%7C1573556432%7C%7C%7C1%7C%7C%7C1573786993%7C%7C%7C1573786977%7C%7C%7C%7C%7C%7C128d8f4ca43f292c%7C%7C%7C%7C%7C%7C%7C%7C%7C0%7C%7C%7Cundefined"
        }
        self.detail_header = {
            "Host":
            "inquiryhall.zcygov.cn",
            "Upgrade-Insecure-Requests":
            "1",
            "User-Agent":
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.120 Safari/537.36",
            "Sec-Fetch-Mode":
            "navigate",
            "Accept":
            "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3",
            "Sec-Fetch-Site":
            "none",
            "Accept-Encoding":
            "gzip, deflate, br",
            "Accept-Language":
            "zh-CN,zh;q=0.9",
            "Cookie":
            "_zcy_log_client_uuid=06589ac0-0082-11ea-bfd3-2debdde2a0cb; acw_tc=76b20ff115735563250257125e5e63ae9e8c36192d14ba588620155ec76154; districtCode=330199; districtName=%E6%9D%AD%E5%B7%9E%E5%B8%82%E6%9C%AC%E7%BA%A7; _dg_check.bbc15f7dfd2de351.63bf=-1; _dg_playback.bbc15f7dfd2de351.63bf=1; UM_distinctid=16e6933510014f-096c6098199cba-b363e65-1fa400-16e693351011b5; CNZZDATA1259303436=1940456832-1573719707-%7C1573783376; _dg_id.bbc15f7dfd2de351.63bf=1949869e0a57864c%7C%7C%7C1573036904%7C%7C%7C0%7C%7C%7C1573788693%7C%7C%7C1573787174%7C%7C%7C%7C%7C%7C9f284b487ef9c1da%7C%7C%7C%7C%7C%7C%7C%7C%7C0%7C%7C%7Cundefined"
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
                            "招标平台": "政府采购云",
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
        if self.bid_type is "PUBLISHING":
            sql = "SELECT `id` FROM `bidpython`.`tb_bid` WHERE `inviter_number` = '{}' and `platform_id` = 17 LIMIT 1;"
        elif self.bid_type is "RESULT":
            sql = "SELECT `id` FROM `bidpython`.`tb_bid_result` WHERE `inviter_number` = '{}' and `platform_id` = 17 LIMIT 1;"

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
        return content.replace("\n", "").replace("\r", "").replace(" ",
                                                                   "").replace(
                                                                       ")", "")

    def deal_detail(self, path):
        resp = run_func(self.request, path, header=self.detail_header)

        inquiry_detail = run_func(
            self.soup, resp, attr={"class": "inquiry-detail-container"})

        inquiry_info = run_func(
            self.soup,
            run_func(
                self.soup, inquiry_detail, attr={"class": "inquiry-info"}),
            attr="section",
            all_tag=True)

        inquiry_base = run_func(
            self.soup,
            run_func(self.soup, inquiry_info[0], attr="table"),
            attr="tr",
            all_tag=True)

        info = {}
        info["网上竞价名称"] = run_func(
            self.soup,
            run_func(
                self.soup, inquiry_detail, attr={"class": "inquiry-title"}),
            attr="h1").text

        info["网上竞价编号"] = inquiry_base[0].text.strip('\n').split('\n')[1]

        info_temp = inquiry_base[1].text.strip('\n').split('\n')

        info["竞价开始时间"] = info_temp[1]
        info["竞价截止时间"] = info_temp[3]
        info["采购人"] = info_temp[5]
        info["金额上限"] = inquiry_base[3].text.strip('\n').split('\n')[-1]
        info["path"] = path

        goods_list = run_func(
            self.soup, inquiry_info[2], attr="table", all_tag=True)
        tr_json = []

        for index, good_obj in enumerate(goods_list):
            good = run_func(self.soup, good_obj, attr="td", all_tag=True)

            if index == len(goods_list) - 1:
                continue

            sign = 1 if len(good) == 5 else 0
            param = self.remove_character(
                good[1].text) if len(good) == 5 else ""

            unit = re.search(r'[\u4e00-\u9fa5]+',good[sign + 2].text).group()
            tr_json.append({
                "参数": param,
                "单位": unit,
                "招标编号": info["网上竞价编号"],
                "序号": index + 1,
                "产品名称": good[0].text,
                "产品类别": "",
                "产品单价": "",
                "合计": good[sign + 3].text,
                "品牌": good[sign + 1].text,
                "数量": good[sign + 2].text.replace(unit, ''),
                "标配": "",
                "型号": '',
                "url": path,
                "招标平台": "政府采购云",
                "售后服务": "",
            })

        run_func(self.ecnu_cursor.execute,
                    self.insert_tb_bid.format(**info))

        run_func(
            self.ecnu_cursor.execute,
            self.insert_bid_json.format(
                info["网上竞价编号"], info["path"],
                json.dumps(tr_json, ensure_ascii=False), self.get_time()))

    def deal_result(self, path):
        resp = run_func(self.request, path, header=self.detail_header)


        inquiry_detail = run_func(
            self.soup, resp, attr={"class": "inquiry-result-container"})

        inquiry_info = run_func(
            self.soup,
            run_func(
                self.soup, inquiry_detail, attr={"class": "inquiry-info"}),
            attr="section",
            all_tag=True)

        inquiry_base = run_func(
            self.soup,
            run_func(self.soup, inquiry_info[0], attr="table"),
            attr="tr",
            all_tag=True)

        info = {}

        title_temp = run_func(
            self.soup, inquiry_detail, attr={"class": "inquiry-title"})

        info["网上竞价名称"] = run_func(self.soup, title_temp, attr="h1").text
        info["成交公告时间"] = run_func(self.soup, title_temp, attr="span").text

        info["网上竞价编号"] = inquiry_base[0].text.strip('\n').split('\n')[1]

        info_temp = inquiry_base[1].text.strip('\n').split('\n')

        info["竞价开始时间"] = info_temp[1]
        info["竞价截止时间"] = info_temp[3]

        info["采购人"] = info_temp[5]
        info["path"] = path

        deal_info = run_func(
            self.soup, inquiry_info[5], attr="table", all_tag=True)

        info["中标公司"] = deal_info[0].text.strip('\n').split('\n')[1]
        info["中标总额"] = deal_info[0].text.strip('\n').split('\n')[3]

        goods_list = run_func(
            self.soup,
            run_func(self.soup, deal_info[1], attr="tbody"),
            attr="tr",
            all_tag=True)

        tr_json = []

        for good_obj in goods_list:
            good = run_func(self.soup, good_obj, attr="td", all_tag=True)

            tr_json.append({
                "成交时间": "",
                "招标编号": info["网上竞价编号"],
                "规格配置": "",
                "详情url": info["path"],
                "平台名称": "政府采购云",
                "单价": good[5].text,
                "中标供应商": info["中标公司"],
                "设备名称": good[1].text,
                "创建时间": self.get_time(),
                "品牌": good[2].text,
                "型号": good[3].text,
                "数量": good[4].text
            })

        run_func(self.ecnu_cursor.execute,
                    self.insert_bid_result.format(**info))

        run_func(
            self.ecnu_cursor.execute,
            self.insert_tr_json.format(
                json.dumps(tr_json, ensure_ascii=False), info["path"]))

    def run(self, data):
        a = time.time()
        resp = run_func(self.request, self.path, header=self.header, data=data)
        print("run_func time is {}".format(time.time() - a))
        data = json.loads(resp)
        for item in data["result"]["data"]:
            if run_func(self.judge_already, item["orderId"]):
                if self.bid_type is "PUBLISHING":
                    run_func(self.deal_detail, item["announcementDetailUrl"])
                elif self.bid_type is "RESULT" and item["stateStr"] == "询价完成":
                    run_func(self.deal_result, item["announcementDetailUrl"])
            else:
                logger.info("--->Info: existed already")

    def main(self):
        for page in range(1, 2):
            for self.bid_type in ["PUBLISHING", "RESULT"]:
                data = {
                    "districtCodeList": [],
                    "pageSize": 20,
                    "pageNo": page + 1,
                    "typeEnum": self.bid_type
                }
                self.run(data)


if __name__ == "__main__":
    os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    DealZcy().main()

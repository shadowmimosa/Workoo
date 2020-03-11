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




class DealZhuhai(object):
    def __init__(self):
        self.bid_path = "http://ggzy.zhuhai.gov.cn/exchangeinfo/govbuy/cggg/index_{}.jhtml"
        self.bid_detail = "https://www.gec123.com/xcjenquiry/notice!enquiryNotice.action?notic_seq={}"
        self.result_path = "http://ggzy.zhuhai.gov.cn/exchangeinfo/govbuy/zczbgg/index_{}.jhtml"
        self.result_detail = "https://www.gec123.com/xcj-gateway/api/v1/notices/stable/{}"
        self.header = {
            'User-Agent':
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.100 Safari/537.36',
            'Accept':
            'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'Referer':
            'http://ggzy.zhuhai.gov.cn/exchangeinfo/govbuy/cggg/index.jhtml',
            # 'Cookie':
            # 'HttpOnly; JSESSIONID=CA80CF517E09B3F3AED560FEC05D09FD; clientlanguage=zh_CN; Hm_lvt_6b2130bd5d1b180308be7cb1bce4aa33=1583718693; Hm_lpvt_6b2130bd5d1b180308be7cb1bce4aa33=1583718693'
        }

        self.insert_tb_bid = "INSERT INTO `bidpython`.`tb_bid` ( `title`, `inviter_number`, `announce_time`, `end_time`, `budget_money`, `platform_id`, `url`, `company` ) VALUES ( '{网上竞价名称}', '{网上竞价编号}', '{竞价开始时间}', '{竞价截止时间}', '{金额上限}', 18, '{path}', '{采购人}' );"
        self.insert_bid_result = "INSERT INTO `bidpython`.`tb_bid_result` ( `title`, `inviter_number`, `announce_time`, `end_time`, `announce_date`, `platform_id`, `url`, `company`, `budget_money`, `announce_company` ) VALUES ( '{网上竞价名称}', '{网上竞价编号}', '{竞价开始时间}', '{竞价截至时间}', '{成交公告时间}', 18, '{path}', '{采购人}', '{中标总额}', '{中标公司}' );"
        self.insert_bid_json = "INSERT INTO `bidpython`.`tb_bid_json` ( `shot`, `platform_name`, `inviter_number`, `url`, `json_kv`, `create_time` ) VALUES ( '', '珠海市公共资源交易中心', '{}', '{}', '{}', '{}');"
        self.insert_tr_json = "INSERT INTO `bidpython`.`tb_tr_json` ( `platform_id`, `platform_name`, `tr_json`, `url` ) VALUES ( 18, '珠海市公共资源交易中心', '{}', '{}');"
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
            # for tr in tr_list:
            #     td_list = self.soup(tr, attr=sign, all_tag=True)
            #     for index, td in enumerate(td_list):
            #         text = td.text
            #         if '需求' in text:
            #             info['产品名称'] = text
            #         elif '单价上限' in text:
            #             info['产品单价'] = td_list[index + 1].text.replace('¥', '')
            #         elif '数量' in text:
            #             temp = td_list[index + 1].text.split(' ')
            #             info['数量'] = temp[0]
            #             info['单位'] = temp[-1]
            #         elif '预算金额' in text:
            #             info['金额上限'] = td_list[index + 1].text.replace('¥', '')
            #         elif '数量' in text:
            #             info['数量'] = td_list[index + 1].text

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

    # def ergodic_div(self, div_list: list):
    #     info = {}

    #     info['中标供应商'] = self.soup(div_list[-7],{'style':'text-decoration:underline'}).text

    #     table = self.soup(
    #     {
    #                     "成交时间": "",
    #                     "招标编号": info["网上竞价编号"],
    #                     "规格配置": details[1].split("：")[-1],
    #                     "详情url": info["path"],
    #                     "平台名称": "行采家",
    #                     "总价": good["count"],
    #                     "中标供应商": good["providerName"],
    #                     "设备名称": details[0].split("：")[-1],
    #                     "创建时间": self.get_time(),
    #                     "品牌": details[2].split("：")[-1],
    #                     "型号": details[3].split("：")[-1],
    #                     "数量": good["amount"]
    #                 }

    #     return info

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
        box_right = self.soup(resp, attr={'class': 'rl-box-right'})
        li_obj = self.soup(box_right, attr='li', all_tag=True)

        for li in li_obj:
            info = {}
            a_obj = self.soup(li, attr='a')
            title = a_obj.get('title')
            if '网上询价采购公告' not in title:
                continue

            info["网上竞价编号"] = title.split('：')[-1].replace(')',
                                                          '').replace('）', '')

            if not self.judge_already(info["网上竞价编号"]):
                continue
            info["网上竞价名称"] = title.split(']')[-1].split('(')[0]

            path = a_obj.get('href')
            resp = run_func(self.request, path, header=self.header)

            title = remove_character(
                self.soup(resp, attr={
                    'class': 'contentttit'
                }).text)
            info["网上竞价名称"] = title.replace('[网上询价采购公告]', '').replace(
                '[网上询价采购公告(重新询价)]', '').split('(')[0].split('（')[0]

            tables = self.soup(resp, attr='table', all_tag=True)
            result_0 = self.ergodic_tr(
                self.soup(tables[-1], attr='tr', all_tag=True))
            result_1 = self.ergodic_tr(self.soup(tables[-2],
                                                 attr='tr',
                                                 all_tag=True),
                                       sign='p')

            info["采购人"] = result_1['采购人']
            info["竞价开始时间"] = clean_date(result_1['竞价开始时间'])
            info["竞价截止时间"] = clean_date(result_1['竞价截止时间'])
            info['金额上限'] = result_0.get('金额上限')
            info["path"] = path

            tr_json = [{
                "参数": "",
                "单位": result_0.get('单位'),
                "招标编号": info["网上竞价编号"],
                "序号": 1,
                "产品名称": result_0.get('产品名称'),
                "产品类别": "",
                "产品单价": result_0.get('产品单价'),
                "合计": '',
                "品牌": "",
                "数量": result_0.get('数量'),
                "标配": "",
                "型号": '',
                "url": path,
                "招标平台": "珠海市公共资源交易中心",
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
        box_right = self.soup(resp, attr={'class': 'rl-box-right'})
        li_obj = self.soup(box_right, attr='li', all_tag=True)

        for li in li_obj:
            info = {}
            a_obj = self.soup(li, attr='a')
            title = a_obj.get('title')
            if '网上询价结果公告' not in title:
                continue

            info["网上竞价编号"] = title.split('：')[-1].replace(')',
                                                          '').replace('）', '')
            if not self.judge_already(info["网上竞价编号"]):
                continue
            info["网上竞价名称"] = title.split(']')[-1].split('(')[0]
            path = a_obj.get('href')
            resp = run_func(self.request, path, header=self.header)

            # info['中标供应商'] = self.soup(resp, {
            #     'style': 'text-decoration:underline'
            # }).text
            table = self.soup(resp, {'class': 'unify_table'})
            td_list = self.soup(resp, 'td', all_tag=True)

            info["path"] = path

            info["成交公告时间"] = self.soup(self.soup(resp, {'class': 'titshare'}),
                                       'span').text
            info["竞价开始时间"] = ""
            info["竞价截至时间"] = ""

            info["中标总额"] = td_list[-4].text
            info['中标公司'] = td_list[-5].text
            info["采购人"] = td_list[-3].text

            tr_json = [{
                "成交时间": "",
                "招标编号": info["网上竞价编号"],
                "规格配置": '',
                "详情url": info["path"],
                "平台名称": "珠海市公共资源交易中心",
                "总价": td_list[-4].text,
                "中标供应商": td_list[-5].text,
                "设备名称": td_list[-7].text,
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
        for page in range(5, 6):
            self.bid_type = "bid"
            run_func(self.deal_detail, page)
            self.bid_type = "bidResult"
            run_func(self.deal_result, page)


if __name__ == "__main__":
    os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    DealZhuhai().main()

import os
import re
import time
import json
import urllib
import urllib3
import requests
import random
import pymysql

from bs4 import BeautifulSoup


class Query(object):
    def get_session(self):
        """创建 session 示例，以应对多线程"""

        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

        # 设置重连次数
        requests.adapters.DEFAULT_RETRIES = 10
        # 设置连接活跃状态为False
        session = requests.session()
        session.keep_alive = False
        session.verify = False

        adapter = requests.adapters.HTTPAdapter(max_retries=3)
        # 将重试规则挂载到http和https请求
        session.mount('http://', adapter)
        session.mount('https://', adapter)

        return session

    def deal_re(self, byte=False, need_header=False, **kwargs):
        """requests of get"""

        url = kwargs.get("url")
        header = kwargs.get("header")
        try:
            data = kwargs.get("data")
        except:
            data = None
        files = kwargs.get("files")

        sesscion_a = self.get_session()

        print("---> 开始请求网址：{}".format(url))
        start_time = time.time()
        retry_count = 5
        while retry_count > 0:
            try:

                if isinstance(data, dict):
                    resp = sesscion_a.post(
                        url,
                        headers=header,
                        data=json.dumps(data),
                        timeout=(10, 60))
                elif isinstance(files, dict):
                    resp = sesscion_a.post(url, files=files, timeout=(10, 60))
                elif data:
                    resp = sesscion_a.post(
                        url, headers=header, data=data, timeout=(10, 60))
                else:
                    resp = sesscion_a.get(
                        url,
                        headers=header,
                        allow_redirects=False,
                        timeout=(10, 60))
                retry_count = 0
            except Exception as exc:
                retry_count -= 1

        end_time = time.time()

        try:
            if resp.status_code == 200:
                magic_time = end_time - start_time
                return resp
            else:
                print("--->Info {} 请求失败！状态码为{}，共耗时{:.3}秒".format(
                    url, resp.status_code, end_time - start_time))
        except UnboundLocalError as exc:
            print("--->Error: deal re is error, the error is {}".format(exc))
            return None

    def run(self, path, sign=None, header={}, **kwargs):
        resp = self.deal_re(url=path, header=header, **kwargs)
        if sign:
            return resp.content
        else:
            return resp.text


class DealGhzrzyw(object):
    def __init__(self):
        self.page_path = "http://www.choicelink.cn:8888/AgentApi/EProject/PageNotice2?rows=30&page={}&Mode={}"
        self.detail_path = "http://oa.chinapsp.cn:8099/WebReport/ReportServer?_=1567872893275&__boxModel__=true&op=fr_write&cmd=read_w_content&sessionID=84218&reportIndex=0&browserWidth=788&iid=0.6669620362773621&__cutpage__=&pn=0&__webpage__=true&_paperWidth=788&_paperHeight=572&__fit__=false"
        self.header = {
            "Host": "www.choicelink.cn:8888",
            "Accept": "application/json, text/plain, */*",
            "Origin": "http://www.choicelink.cn",
            "User-Agent":
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.90 Safari/537.36",
            "Referer": "http://www.choicelink.cn/channels/3014.html",
            "Accept-Encoding": "gzip, deflate",
            "Accept-Language": "zh-CN,zh;q=0.9",
        }

        self.insert_tb_bid = "INSERT INTO `bidpython`.`tb_bid` ( `title`, `inviter_number`, `announce_time`, `end_time`, `budget_money`, `platform_id`, `url`, `company` ) VALUES ( '{}', '{}', '{}', '{}', '{}', 13, '{}', '{}' );"
        self.insert_bid_result = "INSERT INTO `bidpython`.`tb_bid_result` ( `title`, `inviter_number`, `announce_date`, `budget_money`, `platform_id`, `url`, `company`, `announce_company` ) VALUES ( '{}', '{}', '{}', '{}', 13, '{}', '{}', '{}');"
        self.insert_bid_json = insert_sql = "INSERT INTO `bidpython`.`tb_bid_json` ( `shot`, `platform_name`, `inviter_number`, `url`, `json_kv`, `create_time` ) VALUES ( '', '云采链采购一体化平台', '{}', '{}', '{}', '{}');"
        self.insert_tr_json = insert_sql = "INSERT INTO `bidpython`.`tb_tr_json` ( `platform_id`, `platform_name`, `tr_json`, `url` ) VALUES ( 13, '云采链采购一体化平台', '{}', '{}');"

        self.request = Query()
        self.pattarn = re.compile(r"FR.SessionMgr.register\(.*contentPane\);")
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

    def get_session_id(self, project_id):
        if self.item_type == 1:
            path = "http://oa.chinapsp.cn:8099/WebReport/ReportServer?reportlet=newcailian/gonggao/zhaobiaoReport.cpt&__pi__=false&Id={}".format(
                project_id)
        elif self.item_type == 2:
            path = "http://oa.chinapsp.cn:8099/WebReport/ReportServer?reportlet=newcailian/gonggao/YunCailian/resultReport.cpt&Id={}".format(
                project_id)

        # Host: oa.chinapsp.cn:8099
        # Proxy-Connection: keep-alive
        # Upgrade-Insecure-Requests: 1
        # User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.90 Safari/537.36
        # Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3
        # Referer: http://e.chinapsp.cn/zsdq/single-pages/notice-content.html?Id=44427
        # Accept-Encoding: gzip, deflate
        # Accept-Language: zh-CN,zh;q=0.9
        # Cookie: JSESSIONID=87B9C3ECF3021D50AFC633D3BDF7F837
        resp = self.request.run(path, header=self.header)
        session_id = re.search(self.pattarn, resp).group().replace(
            "FR.SessionMgr.register('", "").replace("', contentPane);", "")
        print(session_id)
        self.session_id = session_id

    def close_session(self):
        header = {
            "Host": "oa.chinapsp.cn:8099",
            "Accept": "*/*",
            "X-Requested-With": "XMLHttpRequest",
            "User-Agent":
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.90 Safari/537.36",
            # "Referer":
            # "http://oa.chinapsp.cn:8099/WebReport/ReportServer?reportlet=newcailian%2Fgonggao%2FzhaobiaoReport.cpt&__pi__=false&Id=ff7a744a-29ba-4273-b81b-fcc9cea2189c",
            "Accept-Encoding": "gzip, deflate",
            "Accept-Language": "zh-CN,zh;q=0.9",
        }
        path = "http://oa.chinapsp.cn:8099/WebReport/ReportServer?op=closesessionid&sessionID={}".format(
            self.session_id)

        resp = self.request.run(path, header=header)

    def get_time(self, content):
        content = content.replace("T", " ")
        return time.mktime(time.strptime(content, '%Y-%m-%d %H:%M:%S'))

    def get_status(self):
        """获取竞价公告的各个时间段"""

        currentTime = int(time.time())
        applyTimeBegin = self.get_time(self.item.get("ApplyFromTime"))
        applyTimeEnd = self.get_time(self.item.get("ApplyToTime"))
        uppriceTimeBegin = self.get_time(self.item.get("UppriceFromTime"))
        uppriceTimeEnd = self.get_time(self.item.get("UppriceToTime"))

        if currentTime < applyTimeBegin:
            return 0
        elif applyTimeBegin < currentTime and currentTime <= applyTimeEnd:
            return 1
        elif applyTimeEnd < currentTime and currentTime <= uppriceTimeBegin:
            return 2
        elif uppriceTimeBegin < currentTime and currentTime <= uppriceTimeEnd:
            return 3
        elif currentTime > uppriceTimeEnd:
            return 4

    def get_type(self):
        """获取公告类型
        
        :param return: 1: 竞价公告 2: 结果公告
        """
        status = self.get_status()
        if self.mode == 0:
            # 竞价公告
            if status == 0 and self.item.get("NoticeType") == "0":
                # 即将报名
                return 1
            elif status == 1 and self.item.get("NoticeType") == "0":
                # 正在报名
                return 1
            elif status == 2 and self.item.get("NoticeType") == "0":
                # 即将报价
                return 1
            elif status == 3 and self.item.get("NoticeType") == "0":
                # 正在报价
                return 1
            elif status == 4 and self.item.get("NoticeType") == "0":
                # 竞价公告
                return 1

            # 竞价——结果公告 更正公告 废标公告
            elif self.item.get("NoticeType") == "5":
                # 结果公告
                return 2
            elif self.item.get("NoticeType") == "1":
                # 更正公告 不要
                return
            elif self.item.get("NoticeType") == "6":
                # 废标公告 不要
                return

        elif self.mode == 1:
            # 调研公告 不要
            return
            if status == 0 and self.item.get("NoticeType") == "7":
                # 即将报名
                return
            elif status == 1 and self.item.get("NoticeType") == "7":
                # 正在报名
                return
            elif status == 4 and self.item.get("NoticeType") == "7":
                # 报名结束
                return

            # 调研——结果公告 更正公告 废标公告
            elif self.item.get("NoticeType") == "1":
                # 更正公告
                return
            elif self.item.get("NoticeType") == "3":
                # 结果公告
                return
            elif self.item.get("NoticeType") == "8":
                # 废标公告
                return

    def judge_type(self):
        item_type = self.get_type()
        if item_type == 1:
            self.item_type = 1
            return True
        elif item_type == 2:
            self.item_type = 2
            return True
        else:
            return

    def ergodic_td(self, tr_obj):
        td_list = tr_obj.contents
        for td_obj in td_list:
            text = td_obj.text
            if "项目编号：" in text:
                return text.split("：")
            elif "采购单位：" in text:
                return text.split("：")
            elif "项目最高限价金额：" in text:
                return text.split("：")
            elif "采购单位:" in text:
                return_list = text.split(":")
                return_list.append(td_list[-1].text.split(": ")[-1])
                return return_list
            elif "采购项目编号:" in text:
                return text.split(":")
            elif "报名开始时间" in text:
                return ["报名开始时间", td_list[3].text, td_list[5].text]
            elif "采购品目名称" in text:
                return 1
            elif "采购内容" in text:
                return 2

    def judge_already(self, item_code):
        if self.item_type == 1:
            sql = "SELECT `inviter_number` FROM `bidpython`.`tb_bid` WHERE `inviter_number` = '{}' LIMIT 1;"
        else:
            sql = "SELECT `inviter_number` FROM `bidpython`.`tb_bid_result` WHERE `inviter_number` = '{}' LIMIT 1;"

        if self.ecnu_cursor.execute(sql.format(item_code)) == 0:
            return
        else:
            return True

    def get_text(self, content):
        if content is None:
            return
        else:
            text = content.text
            if text is None:
                return
            else:
                return text

    def deal_detail(self):
        header = self.header
        item_code = ""
        path = "http://oa.chinapsp.cn:8099/WebReport/ReportServer?_=1568021925180&__boxModel__=true&op=page_content&sessionID={}&pn=1&__webpage__=true&_paperWidth=788&_paperHeight=572&__fit__=false".format(
            self.session_id)

        resp = self.request.run(path, header=self.header)
        soup = BeautifulSoup(resp, "lxml")
        tr_list = soup.find("tbody").contents
        for index, tr_item in enumerate(tr_list):
            if index == 1:
                item_name = tr_item.text
            else:
                item_in_td = self.ergodic_td(tr_item)

                if item_in_td == 1:
                    tr_item_index = index + 1

                elif isinstance(item_in_td, list):
                    if "采购项目编号" in item_in_td[0]:
                        item_code = item_in_td[-1].replace(" ", "")
                    elif "采购单位" in item_in_td[0]:
                        if len(item_code) >= 0 and len(item_code) < 50:
                            item_subject, item_code = item_in_td[
                                1], item_in_td[2]
                    elif "报名开始时间" in item_in_td[0]:
                        item_starttime = item_in_td[1]
                        item_endtime = item_in_td[2]

            # elif index == 3:
            #     for index_td, subject in enumerate(tr_item.find_all("td")):
            #         if index_td == 2:
            #             item_subject = subject.text.split(":")[-1].replace(
            #                 " ", "")
            #         elif index_td == 3:
            #             item_code = subject.text.split(":")[-1].replace(
            #                 " ", "")
            # elif index == 7:
            #     for index_td, times in enumerate(tr_item.find_all("td")):
            #         if index_td == 3:
            #             item_starttime = times.text
            #         elif index_td == 5:
            #             item_endtime = times.text
            # elif index == 14:
            #     for index_td, goods in enumerate(tr_item.find_all("td")):
            #         if index_td == 2:
            #             item_goods_index = times.text
            #         elif index_td == 3:
            #             item_goods_name = times.text
            #         elif index_td == 4:
            #             item_goods_brand = times.text
            #         elif index_td == 5:
            #             item_goods_xinghao = times.text
            #         elif index_td == 6:
            #             item_goods_number = times.text
            #         elif index_td == 7:
            #             item_goods_unti = times.text
            #         elif index_td == 8:
            #             item_budget = times.text

        if self.judge_already(item_code):
            return

        tr_json = []
        while True:
            tr_item = tr_list[tr_item_index]
            td_list = tr_item.contents
            try:
                item_goods_index = int(self.get_text(td_list[2]))
                item_goods_name = self.get_text(td_list[3])
                item_goods_brand = self.get_text(td_list[4])
                item_goods_type = self.get_text(td_list[5])
                item_goods_number = self.get_text(td_list[6])
                item_goods_unti = self.get_text(td_list[7])
                item_budget = self.get_text(td_list[8])
            except AttributeError as exc:
                break
            except ValueError as exc:
                break
            except Exception as exc:
                print("--->Info: Not goods, the error is {}".format(exc))
                break
            else:
                tr_item_index += 1

                tr_json.append({
                    "参数": "",
                    "单位": item_goods_unti,
                    "招标编号": item_code,
                    "序号": item_goods_index,
                    "产品名称": item_goods_name,
                    "产品类别": "",
                    "品牌": item_goods_brand,
                    "数量": item_goods_number,
                    "标配": "",
                    "型号": item_goods_type,
                    "url": self.page_url,
                    "招标平台": "云采链采购一体化平台",
                    "售后服务": "",
                })

        self.ecnu_cursor.execute(
            self.insert_tb_bid.format(item_name, item_code, item_starttime,
                                      item_endtime, item_budget, self.page_url,
                                      item_subject))

        self.ecnu_cursor.execute(
            self.insert_bid_json.format(
                item_code, self.page_url,
                json.dumps(tr_json, ensure_ascii=False),
                time.strftime('%Y-%m-%d %H:%M:%S',
                              time.localtime(int(time.time())))))

    def result_detail(self):
        header = self.header
        path = "http://oa.chinapsp.cn:8099/WebReport/ReportServer?_=1568021925180&__boxModel__=true&op=page_content&sessionID={}&pn=1&__webpage__=true&_paperWidth=788&_paperHeight=572&__fit__=false".format(
            self.session_id)

        resp = self.request.run(path, header=self.header)
        soup = BeautifulSoup(resp, "lxml")
        tr_list = soup.find("tbody").contents
        item_time = self.item.get("NoticeDate").replace("T", " ")
        for index, tr_item in enumerate(tr_list):
            if index == 1:
                item_name = tr_item.text
            else:
                item_in_td = self.ergodic_td(tr_item)

                if item_in_td == 2:
                    tr_item_index = index + 1

                elif isinstance(item_in_td, list):
                    if "项目编号" in item_in_td[0]:
                        item_code = item_in_td[-1]
                    elif "采购单位" in item_in_td[0]:
                        item_subject = item_in_td[-1]

        if self.judge_already(item_code):
            return

        tr_json = []
        create_time = time.strftime('%Y-%m-%d %H:%M:%S',
                                    time.localtime(int(time.time())))
        while True:
            tr_item = tr_list[tr_item_index]
            # int(tr_item.find(attrs={"colspan": "5"}))
            try:
                item_good_name = tr_item.find(attrs={"colspan": "10"}).text
                item_winner = tr_item.find(attrs={"colspan": "6"}).text
                item_budget = tr_item.find(attrs={
                    "colspan": "4"
                }).text.replace("人民币", "").replace("元", "")
            except AttributeError as exc:
                break
            except Exception as exc:
                print("--->Info: Not goods, the error is {}".format(exc))
                break
            else:
                tr_item_index += 1
                good_ = {
                    "成交时间": item_time,
                    "招标编号": item_code,
                    "规格配置": "",
                    "详情url": self.page_url,
                    "平台名称": "云采链采购一体化平台",
                    "单价": item_budget,
                    "中标供应商": item_winner,
                    "设备名称": item_good_name,
                    "创建时间": create_time,
                    "品牌": "",
                    "型号": "",
                    "数量": ""
                }
                tr_json.append(good_)

        self.ecnu_cursor.execute(
            self.insert_bid_result.format(item_name, item_code, item_time,
                                          item_budget, self.page_url,
                                          item_subject, item_winner))

        self.ecnu_cursor.execute(
            self.insert_tr_json.format(
                json.dumps(tr_json, ensure_ascii=False), self.page_url))

    def main(self, path):
        resp = self.request.run(path, header=self.header)
        data = json.loads(resp)
        for self.item in data["rows"]:
            try:
                if self.judge_type() == True:
                    self.page_url = "http://ex.chinapsp.cn/gzhydz/single-pages/notice-content.html?Id={}".format(
                        self.item.get("Id"))
                    self.get_session_id(self.item["ProjectId"])

                    # if self.item_type == 1:
                    #     self.deal_detail()
                    # elif self.item_type == 2:
                    #     self.result_detail()

                    try:
                        if self.item_type == 1:
                            self.deal_detail()
                        elif self.item_type == 2:
                            self.result_detail()
                    except Exception as exc:
                        print("--->Error: the error is {}".format(exc))

                    self.close_session()
                    time.sleep(random.randint(1, 3))
                else:
                    print("--->Info: 类型不符")
            except Exception as exc:
                print("--->Error: the error is {}".format(exc))

    def run(self, pages):
        for self.mode in [0]:  # mode in [0, 1]
            for page in range(1, pages):
                try:
                    self.main(self.page_path.format(page, self.mode))
                except Exception as exc:
                    print("--->Error: the error is {}".format(exc))


DEBUG = False
if __name__ == "__main__":
    os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    pages = 10
    DealGhzrzyw().run(pages)
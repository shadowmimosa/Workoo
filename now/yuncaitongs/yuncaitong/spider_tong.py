import os
import time
import json
import urllib
import urllib3
import requests
import random
import pymysql


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
        self.page_path = "https://www.yuncaitong.cn/api/publish/solr/demand?&page={}&rows=25"
        self.result_path = "https://www.yuncaitong.cn/api/publish/solr/result?&page={}&rows=25"
        self.detail_path = "https://www.yuncaitong.cn/publish/{}/{}.sson?v=201804280000"
        self.header = {
            "Host":
            "www.yuncaitong.cn",
            "Accept":
            "application/json, text/plain, */*",
            "User-Agent":
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.90 Safari/537.36",
            "Referer":
            "https://www.yuncaitong.cn/publish/demand.shtml",
            "Accept-Encoding":
            "gzip, deflate, br",
            "Accept-Language":
            "zh-CN,zh;q=0.9",
            "Cookie":
            "Hm_lvt_1bc76dfca6bb918d1565157a53195637=1567563502; Hm_lpvt_1bc76dfca6bb918d1565157a53195637=1567748738"
        }
        self.insert_tb_bid = "INSERT INTO `bidpython`.`tb_bid` ( `title`, `inviter_number`, `announce_time`, `end_time`, `budget_money`, `platform_id`, `url`, `company` ) VALUES ( '{}', '{}', '{}', '{}', '{}', 12, '{}', '{}' );"
        self.insert_bid_result = "INSERT INTO `bidpython`.`tb_bid_result` ( `title`, `inviter_number`, `announce_date`, `budget_money`, `platform_id`, `url`, `company`, `announce_company` ) VALUES ( '{}', '{}', '{}', '{}', 12, '{}', '{}', '{}');"
        self.insert_tr_json = insert_sql = "INSERT INTO `bidpython`.`tb_bid_json` ( `shot`, `platform_name`, `inviter_number`, `url`, `json_kv`, `create_time` ) VALUES ( '', '云采通 高校采购联盟', '{}', '{}', '{}', '{}');"
        self.init_sql()
        self.request = Query()

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
        if self.sign == 0:
            sql = "SELECT `inviter_number` FROM `bidpython`.`tb_bid` WHERE `inviter_number` = '{}' LIMIT 1;"
        else:
            sql = "SELECT `inviter_number` FROM `bidpython`.`tb_bid_result` WHERE `inviter_number` = '{}' LIMIT 1;"

        if self.ecnu_cursor.execute(sql.format(item_code)) == 0:
            return True
        else:
            return

    def get_path(self, create_time, id):
        create_time = str(create_time)
        if len(create_time) == 13:
            create_time = int(create_time) / 1000
        elif len(create_time) != 10:
            print("--->Error: the timestamps is wrong, the time is {}".format(
                create_time))
        return self.detail_path.format(
            time.strftime("%Y/%m/%d", time.localtime(int(create_time))), id)

    def tr_json_to_sql(self):
        pass

    def get_remark(self, tech):
        for item in tech:
            return item.get("remark")

    def get_service(self, content):
        if content == None:
            return
        else:
            return content.replace("'", "").replace('"', '')

    def deal_detail(self, path):
        # path = "https://www.yuncaitong.cn/publish/{}.sson?v=201804280000".format(path)
        header = self.header
        header["Referer"] = path.replace("sson?v=201804280000", "shtml")
        resp = self.request.run(path, header=header)

        data = json.loads(resp)
        itme_name = data.get("publish").get("subject")
        item_code = data.get("enquiry").get("code")

        item_starttime = time.strftime(
            '%Y-%m-%d %H:%M:%S',
            time.localtime(int(data.get("publish").get("timeBegin")) / 1000))
        item_endtime = time.strftime(
            '%Y-%m-%d %H:%M:%S',
            time.localtime(int(data.get("publish").get("timeEnd")) / 1000))

        item_subject = data.get("publish").get("depName")
        if item_subject is None:
            item_subject = data.get("org").get("name")
        if data.get("enquiry").get("budgetOpen") == True:
            item_budget = data.get("enquiry").get("budget")
        else:
            item_budget = "未公布"

        self.ecnu_cursor.execute(
            self.insert_tb_bid.format(itme_name, item_code, item_starttime,
                                      item_endtime, item_budget,
                                      header["Referer"], item_subject))
        tr_json = []
        for index, item in enumerate(data.get("enquiry").get("items")):
            tr_json.append({
                "参数": self.get_remark(item.get("tech")),
                "单位": item.get("unit"),
                "招标编号": item_code,
                "序号": "{}".format(index + 1),
                "产品名称": item.get("name"),
                "产品类别": item.get("categoryName"),
                "品牌": item.get("brand"),
                "数量": item.get("applyNums"),
                "标配": "",
                "型号": item.get("model"),
                "url": header["Referer"],
                "招标平台": "云采通 高校采购联盟",
                "售后服务": self.get_service(item.get("service")),
            })
        self.ecnu_cursor.execute(
            self.insert_tr_json.format(
                item_code, header["Referer"],
                json.dumps(tr_json, ensure_ascii=False),
                time.strftime('%Y-%m-%d %H:%M:%S',
                              time.localtime(int(time.time())))))

    def result_detail(self, path):
        header = self.header
        header["Referer"] = path.replace("sson?v=201804280000", "shtml")
        resp = self.request.run(path, header=header)

        data = json.loads(resp)
        itme_name = data.get("publish").get("subject")
        item_code = data.get("enquiry").get("code")
        item_subject = data.get("publish").get("depName")

        item_starttime = time.strftime(
            '%Y-%m-%d %H:%M:%S',
            time.localtime(int(data.get("publish").get("timeBegin")) / 1000))

        if data.get("enquiry").get("winPriceOpen") == True:
            item_price = data.get("enquiry").get("win").get("price")
        else:
            item_price = "未公布"

        if data.get("enquiry").get("winnerOpen") == True:
            item_winner = data.get("enquiry").get("win").get("providerName")
        else:
            item_winner = "未公布"

        self.ecnu_cursor.execute(
            self.insert_bid_result.format(itme_name, item_code, item_starttime,
                                          item_price, header["Referer"],
                                          item_subject, item_winner))

    def run(self, pages):
        command = "self.{}(self.get_path(item['createTime'], item['id']))"

        for index, path in enumerate([self.page_path, self.result_path]):
            if index == 0:
                deal_command = command.format("deal_detail")
                self.sign = 0
            else:
                self.sign = 1
                deal_command = command.format("result_detail")

            for page in range(0, pages):
                resp = self.request.run(path.format(page), header=self.header)
                for item in json.loads(resp):
                    if item.get("projectTypeName") == "网上竞价":
                        # time.sleep(random.randint(1, 4))
                        time.sleep(1)
                        if self.judge_already(item.get("projectCode")):
                            # eval(deal_command)
                            try:
                                eval(deal_command)
                                print(item.get("projectCode"))
                            except Exception as exc:
                                print("--->Error: the error is {}".format(exc))

                        else:
                            print("--->Info: the {} in database alreadly".format(item.get("projectCode")))


DEBUG = False
if __name__ == "__main__":
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    pages = 10
    DealGhzrzyw().run(pages)
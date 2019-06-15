import requests
import urllib3
import time
import sys
import random
import os
import json
import xlwt


class Query(object):
    def __init__(self):
        self.url = "http://repair.salt.ch/CaseWizard/StepSerialNumberPreregisteredOrange/GetFmiPInfos?imei={}&productId={}"
        self.header = {
            "Host": "121.199.72.208:8081",
            "Accept": "*/*",
            "X-Requested-With": "XMLHttpRequest",
            "User-Agent":
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36",
            "Referer":
            "http://121.199.72.208:8081/SGHWeb/Page/GroundWater/MonitoringDataShow.aspx?pkiaa={}",
            "Accept-Encoding": "gzip, deflate",
            "Accept-Language": "zh-CN,zh;q=0.9",
            "Cookie": "ASP.NET_SessionId=0azjapfudnbyxbkzu1rjff0a"
        }
        self.url = "http://121.199.72.208:8081/SGHWeb/AjaxHandler.ashx?class=AjaxGroundWater&method="

        self.data_dict = {
            "PKIAA": "统一编号",
            "TKALB": "监测点位置",
            "CHAHBA": "经度",
            "CHAHBB": "纬度",
            "TKCAH": "地面高程",
            "GCJCBL": "井口高程",
            "GCKKJ": "井口直径",
            "GCDKJ": "井底直径",
            "TKCBCL": "成井深度",
            "SWEFBP": "监测频率",
            "SWJCSD": "监测深度",
            "CDGC": "测点高程",
            "SWAMN": "水文地质单元名称",
            "SWAMB": "水文地质单元类型",
            "SWAE": "含水层类型",
            "SWAF": "地下水动力类型",
            "SWAG": "钻井结构类型",
            "SWEB": "监测内容",
            "SWEFC": "监测点类型",
            "SWEFBU": "监测手段",
            "HJY": "监测目的",
            "SWEFBX": "监测井(点)状况",
            "SWEFBR": "监测点级别",
            "SWEFBQ": "保护措施",
            "SWEFBB": "监测起始时间",
            "SWEFBA": "建井(点)时间",
            "SWEFBC": "监测点变更时间",
            "SWEFBB": "变更前统一编号",
            "ZJDW": "钻井施工单位",
            "TKALA": "原始编号"
        }
        if sys.platform == "win32":
            # self.proxies = False
            self.init_pool()
        else:
            self.init_pool()
        self.init_sheet()

    def init_sheet(self):
        self.wbk = xlwt.Workbook()
        self.sheet_1 = self.wbk.add_sheet("sheet1")
        self.sheet_1.write(0, 0, "统一编号")
        self.sheet_1.write(0, 1, "监测时间")
        self.sheet_1.write(0, 2, "监测值(m)")
        self.sheet_1_x = 1
        self.sheet_1_y = 0
        self.sheet_2 = self.wbk.add_sheet("sheet2")
        index = 0
        for key, value in self.data_dict.items():
            self.sheet_2.write(0, index, value)
            index += 1
        self.sheet_2_x = 1
        self.sheet_2_y = 0

    def init_pool(self):
        proxyHost = "http-dyn.abuyun.com"
        proxyPort = "9020"
        # 代理隧道验证信息
        proxyUser = "H23W005A02J5V10D"
        proxyPass = "CB31E09182BA20C4"

        proxyMeta = "http://%(user)s:%(pass)s@%(host)s:%(port)s" % {
            "host": proxyHost,
            "port": proxyPort,
            "user": proxyUser,
            "pass": proxyPass,
        }
        self.proxies = {
            "http": proxyMeta,
            "https": proxyMeta,
        }

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

    def deal_re(self, byte=False, **kwargs):
        """requests of get"""

        url = kwargs.get("url")
        header = kwargs.get("header")
        try:
            data = kwargs.get("data")
        except:
            data = None

        sesscion_a = self.get_session()

        print("---> 开始请求网址：{}".format(url))
        start_time = time.time()

        if self.proxies:
            try:
                retry_count = 3

                while retry_count > 0:
                    try:
                        if not data:
                            resp = sesscion_a.get(
                                url,
                                headers=header,
                                timeout=(3.2, 10),
                                proxies=self.proxies)
                        else:
                            resp = sesscion_a.post(
                                url,
                                headers=header,
                                data=data,
                                timeout=(3.2, 10),
                                proxies=self.proxies)
                        retry_count = 0
                        print(resp)
                    except Exception as exc:
                        print(
                            "---> The error is {}, and the website is {}. Now try again just one time."
                            .format(exc, url))
                        retry_count -= 1

            except ValueError as exc:
                if exc.args[0] == "no proxy":
                    print("no proxy now, run deal re without proxy")

                    try:
                        if not data:
                            resp = sesscion_a.get(
                                url, headers=header, timeout=(3.2, 30))
                        else:
                            resp = sesscion_a.post(
                                url,
                                headers=header,
                                data=data,
                                timeout=(3.2, 30))
                    except Exception as exc:
                        print(
                            "---> The error is {}, and the website is {}. Now try again just one time."
                            .format(exc, url))
                        self.deal_re(url=url, header=header, data=data)
        else:
            try:
                if not data:
                    resp = sesscion_a.get(
                        url, headers=header, timeout=(3.2, 30))
                else:
                    resp = sesscion_a.post(
                        url, headers=header, data=data, timeout=(3.2, 30))
            except Exception as exc:
                print(
                    "---> The error is {}, and the website is {}. Now try again just one time."
                    .format(exc, url))
                self.deal_re(url=url, header=header, data=data)

        end_time = time.time()
        try:
            if resp.status_code == 200:
                magic_time = end_time - start_time
                print("---> {} 请求成功！共耗时{:.3}秒\n".format(url, magic_time))
                if magic_time <= 6:
                    random_time = random.randint(1, 3)
                    # print("---> 现在开始睡眠 {} 秒\n".format(random_time))
                    # time.sleep(random_time)
                if byte:
                    return resp.content
                else:
                    return resp.text
            elif resp.status_code == 401:
                print("---> Retrying because 401")
                self.init_request()
                resp = self.deal_re(
                    byte=byte, url=url, header=header, data=data)
            elif resp.status_code == 503:
                print(resp.text)
            else:
                print("---> {} 请求失败！状态码为{}，共耗时{:.3}秒\n".format(
                    url, resp.status_code, end_time - start_time))
        except UnboundLocalError as exc:
            print("deal re is error, the error is {}".format(exc))
            return None

    def get_timestamp(self):
        return int(time.time() * 1000)

    def query_data(self):
        url = "http://121.199.72.208:8081/SGHWeb/AjaxHandler.ashx?class=AjaxGroundWater&method=QueryWaterLevelByPkiaaAndTime&pkiaa={}&dTimeStart=2012-07-01+00%3A00%3A00&dTimeEnd=2019-05-28+00%3A00%3A00&unit=%E6%97%A5&cmbCode=%E6%B0%B4%E4%BD%8D&_={}"
        resp = self.deal_re(
            url=url.format(self.id, self.get_timestamp()), header=self.header)
        try:
            data = json.loads(resp)[1]
        except IndexError as exc:
            print("--->{} 该监测站没有数据".format(self.id))
            return

        for value in data:
            self.sheet_1.write(self.sheet_1_x, self.sheet_1_y, value['Pkiaa'])
            self.sheet_1_y += 1
            self.sheet_1.write(self.sheet_1_x, self.sheet_1_y, value['Swnaad'])
            self.sheet_1_y += 1
            self.sheet_1.write(self.sheet_1_x, self.sheet_1_y,
                               value['MonitorValue'])
            self.sheet_1_x += 1
            self.sheet_1_y = 0

    def query_info(self):
        url = "http://121.199.72.208:8081/SGHWeb/AjaxHandler.ashx?class=AjaxGroundWater&method=FetchByID&id={}&_={}"
        resp = self.deal_re(
            url=url.format(self.id, self.get_timestamp()), header=self.header)
        data = json.loads(resp)

        for key in self.data_dict:
            self.sheet_2.write(self.sheet_2_x, self.sheet_2_y, data[key])
            self.sheet_2_y += 1
        self.sheet_2_x += 1
        self.sheet_2_y = 0

    def main(self):
        for filename in os.listdir("./code_data"):
            with open(
                    "./code_data/{}".format(filename), "r",
                    encoding="utf-8") as fn:
                data = json.loads(fn.read())
            for value in data:
                self.id = value["统一编号"]
                self.header["Referer"] = self.header["Referer"].format(self.id)
                self.query_data()
                self.query_info()
                # break

    def run(self):
        self.main()
        try:
            self.wbk.save("./data/data.xls")

        except FileNotFoundError as exc:
            print("---> The error is {}".format(exc))
            os.makedirs("./data/")
            self.wbk.save("./data/data.xls")


def main():
    Query().run()


if __name__ == "__main__":
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    main()
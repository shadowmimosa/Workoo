import requests
import time
import os
import random
import urllib
import json
import xlwt
import re


class GetInfo(object):
    def __init__(self):
        self.family_url = "http://x.kuwo.cn/KuwoLive/lb/GetNewFamilyList?srot=3&page={}&pagesize=20&type=0"
        self.detail_url = "http://x.kuwo.cn/KuwoLive/GetNewFamilyById?id={}"

    def get_session(self):
        """创建 session 示例，以应对多线程"""

        #设置重连次数
        requests.adapters.DEFAULT_RETRIES = 15
        # 设置连接活跃状态为False
        session = requests.session()
        session.keep_alive = False
        session.verify = False

        adapter = requests.adapters.HTTPAdapter(max_retries=3)
        #将重试规则挂载到http和https请求
        session.mount('http://', adapter)
        session.mount('https://', adapter)

        return session

    def deal_re(self, url):
        """requests of get"""

        import urllib3
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

        sesscion_a = self.get_session()

        print("---> 开始请求网址：{}".format(url))
        start_time = time.time()
        try:
            resp = sesscion_a.get(url, timeout=(3.2, 30))
        except UnicodeEncodeError as exc:
            print(
                "---> The error is {}, and the website is {}. Now try again just one time."
                .format(exc, url))
            deal_re(url)
        end_time = time.time()

        if resp.status_code == 200:
            print("---> [{}]请求成功！共耗时{:.3}秒\n".format(url,
                                                     end_time - start_time))
            return resp
        else:
            print("---> [{}]请求失败！状态码为{}，共耗时{:.3}秒\n".format(
                url, resp.status_code, end_time - start_time))

    def get_id(self):
        for index in range(1, 125):
            resp = self.deal_re(self.family_url.format(index))

            with open("./faimly_id.json", 'a+', encoding='utf-8') as fn:
                fn.write(resp.text + '\n')

            # random_time = random.randint(1, 5)
            # print("---> 现在开始睡眠 {} 秒\n".format(random_time))
            # time.sleep(random_time)
    def data_clean(self):
        data = {"name": "", "notice": ""}
        with open("./faimly_id.json", 'r', encoding='utf-8') as fn:
            data_list = fn.readlines()

        for value in data_list:
            value = json.loads(value)
            for flist in value["flist"]:
                data["name"] = flist["name"]
                data["notice"] = flist["notice"]

                for key, item in data.items():
                    data[key] = urllib.parse.unquote(item, 'utf-8')
                print(data)
                with open("./final_data.json", "a+", encoding='utf-8') as fn:
                    fn.write(json.dumps(data, ensure_ascii=False) + '\n')

    def re_clean(self, content):
        wechat = r"[Vv微薇威卫星]{1}"
        qq = r"[加+企鹅ＱＱQQqq扣扣球球]{1}.*\d{5,12}"
        qq_bl = r"(?:[加qQ企鹅号码\s]{2,}|[群号]{1,})(?:[\u4e00-\u9eff]*)(?:[:，：]?)([\d\s]{6,})"
        tel = r""

        pattern = re.compile(qq_bl)
        data = re.findall(pattern, content)
        print(data)

    def excel(self):
        wbk = xlwt.Workbook()
        sheet = wbk.add_sheet('sheet 1')
        sheet.write(0, 0, "家族")
        sheet.write(0, 1, "需求")

        with open("./final_data.json", "r", encoding='utf-8') as fn:
            data_list = fn.readlines()

        index = 1
        for value in data_list:
            value = json.loads(value)
            sheet.write(index, 0, value["name"])
            sheet.write(index, 1, value["notice"])
            index += 1

        wbk.save("./finally.xls")

    def run(self):
        self.get_id()


def main():
    # GetInfo().run()
    # GetInfo().data_clean()
    GetInfo().excel()


if __name__ == "__main__":
    import os
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    # main()
    GetInfo().re_clean("实力传媒公司，专业培训。高扶持高薪资，只为更好的你！商务合作qq:3543118+++qq:916171834")
    GetInfo().re_clean("线上工会诚招合作，扣：742386642.主播纯线上待遇，不抽水不揩油，诚信经营，扶持到位。")
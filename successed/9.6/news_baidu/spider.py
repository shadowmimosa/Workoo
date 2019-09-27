import requests
import urllib3
import time
import os
import json
import pymysql

import pandas as pd
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

try:
    ecnu_mysql = pymysql.connect(
        host='127.0.0.1',
        port=3306,
        user='root',
        passwd='shadow',
        database="baidu_news",
        use_unicode=True,
        charset="utf8mb4",
        autocommit=True)
except pymysql.err.OperationalError as exc:
    print(exc)
    print('登录失败！TimeoutError!')
    os._exit(0)
else:
    ecnu_cursor = ecnu_mysql.cursor()


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

        # print("---> 开始请求网址：{}".format(url))
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
                print(
                    "---> The error is {}, and the website is {}. Now try again just one time."
                    .format(exc, url))
                # self.deal_re(url=url, header=header, data=data)

        end_time = time.time()

        try:
            if resp.status_code == 200:
                magic_time = end_time - start_time
                print("--->Info: Request successful. It takes {:.3} seconds".
                      format(magic_time))
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


class OperaChrome(object):
    def __init__(self):
        # self.option = "window.open('{}')"
        self.info_ = pd.DataFrame()
        self.init_mysql()
        self.run()

    def init_chrome(self):
        url = "http://www.baidu.com/s?ie=utf-8&cl=2&medium=1&rtt=4&bsst=1&rsv_dl=news_t_sk&tn=news&wd={}&tfflag=0".format(
            self.keyword)
        options = webdriver.ChromeOptions()
        options.add_argument("disable-infobars")
        options.add_argument("disable-web-security")
        options.add_argument("--headless")
        options.add_argument("--start-maximized")
        options.add_argument('--log-level=3')
        options.add_argument('--ignore-certificate-errors')
        # driver = webdriver.Chrome(
        #     executable_path="./chromedriver.exe", chrome_options=options)
        driver = webdriver.Chrome(chrome_options=options)
        driver.get(url)
        WebDriverWait(driver, 90, 0.25).until(
            EC.presence_of_element_located((By.ID, "content_left")))

        self.driver = driver

    def extract_data(self):
        if len(self.info_) == 0:
            self.info_ = pd.read_html(self.driver.page_source)[1]
        else:
            self.info_ = pd.concat(
                [self.info_,
                 pd.read_html(self.driver.page_source)[1]],
                ignore_index=True)

    def init_mysql(self):
        try:
            ecnu_mysql = pymysql.connect(
                host='127.0.0.1',
                port=3306,
                user='root',
                passwd='shadow',
                database="baidu_news",
                use_unicode=True,
                charset="utf8mb4",
                autocommit=True)
        except pymysql.err.OperationalError as exc:
            print(exc)
            print('登录失败！TimeoutError!')
            os._exit(0)
        else:
            self.ecnu_cursor = ecnu_mysql.cursor()

    def sql_opea(self):
        insert = 'INSERT INTO `baidu_news`.`news`(`city`, `year`, `keyword`, `count`) VALUES ("{}", {}, "{}", {});'
        self.ecnu_cursor.execute(
            insert.format(self.city, self.year, self.word, self.count))

    def deal_detail(self):
        items = self.driver.find_elements_by_class_name("c-author")
        for value in items:
            # self.driver.execute_script("arguments[0].scrollIntoView(true);",
            #                            value)

            year = int(value.text.split(" ")[-2].split("年")[0])

            if year < 2007:
                break

            if self.year == 0:
                self.year = year
                self.count = 1
            elif self.year > year:
                self.sql_opea()
                self.year = year
                self.count = 1
            elif self.year == year:
                self.count += 1

    def auto_page(self):
        self.deal_detail()
        item = self.driver.find_element_by_id("page")
        self.driver.execute_script("arguments[0].scrollIntoView(true);", item)
        item.find_elements_by_class_name("n")[-1].click()
        # time.sleep(5)
        WebDriverWait(self.driver, 90, 0.25).until(
            EC.presence_of_element_located((By.ID, "content_left")))

        while True:
            item = self.driver.find_element_by_id("page")
            self.driver.execute_script("arguments[0].scrollIntoView(true);",
                                       item)
            click_obj = item.find_elements_by_class_name("n")
            if len(click_obj) < 2:
                self.deal_detail()
                self.sql_opea()
                break
            else:
                self.deal_detail()
                click_obj[-1].click()

    def run(self):
        # [
        #         "河北", "宁夏", "内蒙古", "江西", "广西", "江苏", "云南 ", "河南", "黑龙江", "山东",
        #         "重庆", "湖北", "陕西", "广东", "上海", "北京", "甘肃", "福建", "湖南", "辽宁",
        #         "贵州", "安徽", "山西", "天津", "四川", "青海", "海南", "吉林", "浙江", "新疆",
        #         "西藏"
        # ]
        for self.city in [
                "山东", "重庆", "湖北", "陕西", "广东", "上海", "北京", "甘肃", "福建", "湖南",
                "辽宁", "贵州", "安徽", "山西", "天津", "四川", "青海", "海南", "吉林", "浙江",
                "新疆", "西藏"
        ]:

            for self.word in ["雾霾", "大气污染"]:
                self.year = 0
                self.keyword = "{} {}".format(self.city, self.word)
                self.init_chrome()
                self.auto_page()
                self.driver.close()


def spider_main():
    # path = "http://www.baidu.com/s?ie=utf-8&cl=2&medium=1&rtt=4&bsst=1&rsv_dl=news_t_sk&tn=news&wd={}&tfflag=0".format("雾霾")
    path = "http://www.baidu.com/s?ie=utf-8&cl=2&medium=1&rtt=4&bsst=1&rsv_dl=news_b_pn&tn=news&wd={}&tfflag=0&x_bfe_rqs=03E80&x_bfe_tjscore=0.003541&tngroupname=organic_news&ac_drop=[drop_gs_ws][drop_gs_qos][drop_gs_sched_scatter][drop_ac2bc_word_hash]&pn=20".format(
        "雾霾")

    header = {
        "User-Agent":
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.90 Safari/537.36",
        "Host": "www.baidu.com",
        "Accept":
        "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "zh-CN,zh;q=0.9",
        "Referer": "https://www.baidu.com/"
    }
    resp = Query().run(path=path, header=header)
    print(resp)


def data_clean():
    ecnu_cursor.execute("select * from `baidu_news`.`news`;")
    data = ecnu_cursor.fetchall()
    for value in data:
        if value[3] == "雾霾":
            ecnu_cursor.execute(
                'INSERT INTO `baidu_news`.`data`(`省份`, `时间`, `雾霾`) VALUES ("{}", {}, {});'
                .format(value[1], value[2], value[4]))
        elif value[3] == "大气污染":
            count = ecnu_cursor.execute(
                "select * from `baidu_news`.`data` where `省份`='{}' and `时间`={}"
                .format(value[1], value[2]))
            if count == 0:
                ecnu_cursor.execute(
                    'INSERT INTO `baidu_news`.`data`(`省份`, `时间`, `大气污染`) VALUES ("{}", {}, {});'
                    .format(value[1], value[2], value[4]))
            else:
                ecnu_cursor.execute(
                    "UPDATE `baidu_news`.`data` SET `大气污染` = '{}' WHERE `省份` = '{}' AND `时间` = {} LIMIT 1;"
                    .format(value[4], value[1], value[2]))


def to_excel():

    data = pd.read_sql("select * from `baidu_news`.`data`;", ecnu_mysql)
    data.sort_values(by=["省份", "时间"], inplace=True)
    # data = data.reindex(range(1, 1000))
    # data.drop(['id'], axis=1, inplace=True)
    # data.rename(
    #     columns={
    #         'city': '省份',
    #         'year': '时间',
    #     },
    #     inplace=True)
    data.to_excel("./data.xlsx", index=False)
    # info_ = pd.DataFrame(columns=["省份","时间","雾霾","大气污染"])
    # for city in          [
    #             "河北", "宁夏", "内蒙古", "江西", "广西", "江苏", "云南 ", "河南", "黑龙江", "山东",
    #             "重庆", "湖北", "陕西", "广东", "上海", "北京", "甘肃", "福建", "湖南", "辽宁",
    #             "贵州", "安徽", "山西", "天津", "四川", "青海", "海南", "吉林", "浙江", "新疆",
    #             "西藏"
    #     ]:


def selenium_main():
    start_time = time.time()
    OperaChrome()
    print("time is {}".format(time.time() - start_time))


if __name__ == "__main__":
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    # selenium_main()
    to_excel()

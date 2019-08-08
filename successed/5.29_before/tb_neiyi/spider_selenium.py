import json
import time
import xlwt
import pandas as pd
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def login():
    login_url_tm = "https://login.tmall.com/?spm=875.7931836/B.a2226mz.1.66144265sckIUN&redirectURL=https%3A%2F%2Fwww.tmall.com%2F"
    options = Options()
    dirver = webdriver.Chrome()
    # dirver.get('https://login.taobao.com/member/login.jhtml?redirectURL=http%3A%2F%2Fbuyertrade.taobao.com%2Ftrade%2Fitemlist%2Flist_bought_items.htm%3Fspm%3D875.7931836%252FB.a2226mz.4.66144265Vdg7d5%26t%3D20110530')
    dirver.get(login_url_tm)
    input("请回车登录")
    dictCookies = dirver.get_cookies()
    jsonCookies = json.dumps(dictCookies)

    with open("cookies_tm.json", "w") as fp:
        fp.write(jsonCookies)


def login_with_cookies():

    options = Options()
    options.add_argument("--headless")
    dirver = webdriver.Chrome()
    dirver.get('http://www.taobao.com')
    dirver.delete_all_cookies()
    with open("cookies_tao.json", "r", encoding="utf8") as fp:
        ListCookies = json.loads(fp.read())

    for cookie in ListCookies:
        dirver.add_cookie({
            'domain': '.taobao.com',
            'name': cookie['name'],
            'value': cookie['value'],
            'path': '/',
            'expires': None
        })
    try:
        dirver.get("https://www.tmall.com")
        time.sleep(3)
        dirver.save_screenshot("./tmall.png")
        return dirver
    except Exception as exc:
        print("login failed, the error is {}".format(Exception))


class UnderWear(object):
    def __init__(self):
        # self.shoplist = [
        #     "都市丽人官方旗舰店", "浪莎官方旗舰店", "安莉芳官方旗舰店", "奥丽侬官方旗舰店", "黛安芬官方旗舰店",
        #     "https://dushiliren.tmall.com/search.htm?spm=a1z10.3-b-s.0.0.15817191N5vpnX&search=y",
        #     "https://embryform.tmall.com/category-1325352900.htm?spm=a1z10.1-b-s.w12012752-16996982169.7.10f03608JRsXXN&search=y&parentCatId=951852586&parentCatName=%C8%AB%B2%BF%B1%A6%B1%B4&catName=%CE%C4%D0%D8%D7%A8%C7%F8&scene=taobao_shop#bd"
        # ]
        self.shop_url = [
            {
                "shop_name": "都市丽人官方旗舰店",
                "url":
                "https://dushiliren.tmall.com/category-1444868252.htm?spm=a1z10.3-b-s.w4011-17964102365.2.4eca7191L0ea0j&tsearch=y&orderType=hotsell_desc#TmshopSrchNav",
                "class_name": "item5line1"
            },
            {
                "shop_name": "浪莎官方旗舰店",
                "url":
                "https://langsha.tmall.com/category-746322913.htm?spm=a1z10.5-b-s.w4011-14903041178.54.804a6a9crFknF6&catId=746322913&search=y&orderType=",
                "class_name": "item4line1"
            },
            {
                "shop_name": "安莉芳官方旗舰店",
                "url":
                "https://embryform.tmall.com/category-1325352900.htm?spm=a1z10.5-b-s.w4011-16991628392.120.7ee13328dSyrEl&parentCatId=951852586&parentCatName=%C8%AB%B2%BF%B1%A6%B1%B4&catName=%CE%C4%D0%D8%D7%A8%C7%F8&scene=taobao_shop&catId=1325352900&search=y&orderType=hotsell_desc",
                "class_name": "item4line1"
            },
            {
                "shop_name": "奥丽侬官方旗舰店",
                "url":
                "https://oleno.tmall.com/search.htm?spm=a1z10.1-b-s.0.0.68d64be9Dsmjvi&search=y&orderType=hotsell_desc",
                "class_name": "item5line1"
            },
            {
                "shop_name": "黛安芬官方旗舰店",
                "url":
                "https://triumph.tmall.com/category-1342251415.htm?spm=a1z10.3-b-s.w4011-14455904009.107.125343d2OBlE74&catId=1342251415&scene=taobao_shop&search=y&orderType=&tsearch=y",
                "class_name": "item5line1"
            }
        ]
        self.columns = ["商品名", "详情链接", "图片", "总销量", "评价数"]
        self.option = "window.open('{}')"
        self.run()

    def login(self):
        login_url_tm = "https://login.tmall.com/?spm=875.7931836/B.a2226mz.1.66144265sckIUN&redirectURL=https%3A%2F%2Fwww.tmall.com%2F"
        options = webdriver.ChromeOptions()
        options.add_argument("disable-infobars")
        options.add_argument("disable-web-security")
        # options.add_argument("--headless")
        options.add_argument("--start-maximized")
        options.add_argument('--log-level=3')
        # options.add_argument('--ignore-certificate-errors')
        driver = webdriver.Chrome(chrome_options=options)
        # driver.maximize_window()
        driver.get(login_url_tm)
        print("---> 90 秒内完成登录")
        WebDriverWait(driver, 90, 0.5).until(
            EC.presence_of_element_located((By.CLASS_NAME, "slider-content")))
        self.driver = driver

    def details(self, url):
        self.driver.execute_script(self.option.format(url))
        windows = self.driver.window_handles
        self.driver.switch_to_window(windows[-1])

        while True:
            try:
                WebDriverWait(self.driver, 15, 0.5).until(
                    EC.presence_of_element_located((By.CLASS_NAME,
                                                    "tm-count")))
                WebDriverWait(self.driver, 15, 0.5).until(
                    EC.presence_of_element_located((By.CLASS_NAME,
                                                    "tm-indcon")))

                count = self.driver.find_elements_by_class_name("tm-indcon")
                self.info_goods["月销量"] = count[0].find_element_by_class_name(
                    "tm-count").text
                self.info_goods["评价数"] = count[1].find_element_by_class_name(
                    "tm-count").text
                # self.info_goods["月销量"] = count[0].text
                # self.info_goods["评价数"] = count[1].text
                break
            # except IndexError as exc:
            except IndexError as exc:
                print("---> Waiting for tm-indcon")
                continue

            except StaleElementReferenceException as exc:
                print("---> Waiting for count monthly")
                continue

        element = self.driver.find_element_by_id("J_AttrUL")
        element = element.find_elements_by_tag_name("li")
        for value in element:
            data = value.text
            if "：" in data:
                data = data.split("：")
            elif ":" in data:
                data = data.split(":")
            else:
                print("data error, the data is {}".format(value))
            self.info_goods[data[0]] = data[-1].replace(" ", "").replace(
                "&nbsp;", "")
        self.driver.close()
        self.driver.switch_to_window(windows[0])

    def main(self, content):
        self.driver.get(content["url"])

        while True:
            if self.judge_length():
                break
            WebDriverWait(self.driver, 15, 0.5).until(
                EC.presence_of_element_located((By.CLASS_NAME,
                                                content["class_name"])))
            index = 0
            # self.driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")
            elements = self.driver.find_elements_by_class_name(
                content["class_name"])
            length = len(elements)
            for itme5 in elements:
                sign = True
                if self.judge_length():
                    break
                if index > length - 3:
                    break
                self.driver.execute_script(
                    "arguments[0].scrollIntoView(true);", itme5)
                for item_ in itme5.find_elements_by_tag_name("dl"):
                    if self.judge_length():
                        break
                    info_goods = {}
                    detail = item_.find_element_by_tag_name("a")
                    info_goods["详情链接"] = detail.get_attribute("href")
                    detail_img = detail.find_element_by_tag_name("img")
                    info_goods["图片"] = detail_img.get_attribute("src").replace(
                        "_180x180.jpg", "")
                    info_goods["商品名"] = detail_img.get_attribute("alt")
                    try:
                        info_goods["总销量"] = item_.find_element_by_class_name(
                            "sale-num").text
                    except NoSuchElementException as exc:
                        print("---> Can't find sale_num")

                    # try:
                    #     info_goods["评价数"] = item_.find_element_by_class_name(
                    #         "rates").find_element_by_tag_name(
                    #             "span").text.split(": ")[-1]
                    # except NoSuchElementException as exc:
                    #     print("---> Can't find rates")

                    self.info_goods = info_goods
                    # self.details(info_goods["详情链接"])
                    try:
                        self.details(info_goods["详情链接"])
                    except Exception as exc:
                        print(
                            "---> The detail page was failed, the error is {}".
                            format(exc))
                    self.info_csv = self.info_csv.append(
                        self.info_goods, ignore_index=True)
                index += 1

            next_page = self.driver.find_elements_by_class_name("pagination")
            try:
                if sign:
                    next_button = self.driver.find_element_by_class_name(
                        "pagination").find_element_by_css_selector(
                            ".J_SearchAsync.next")
                    if next_button:
                        next_button.click()
                    sign = False
                else:
                    self.driver.refresh()
                    print("---> Refreshing page now")

                    # self.driver.find_element_by_link_text("下一页").click()
            # except UnboundLocalError as exc:
            #     print("the error is {}".format(exc))
            #     self.driver.refresh()
            except Exception as exc:
                print("---> The error No.3 is {}".format(exc))
                break

    def to_excel(self):
        info_csv = pd.DataFrame(columns=self.columns)

    def judge_length(self):
        return self.info_csv.shape[0] > 210

    def run(self):
        self.login()
        for value in self.shop_url:
            self.info_csv = pd.DataFrame(columns=self.columns)
            # self.main(value)

            try:
                self.main(value)
            except Exception as exc:
                print("---> The error No.4 is {}".format(exc))
                self.info_csv.to_csv("error_data.csv")

            self.info_csv.drop_duplicates(
                subset=["商品名"], keep='first', inplace=True)
            # try:
            #     self.info_csv.to_excel("{}.xls".format(value["shop_name"]) +
            #                         time.ctime())
            try:
                try:
                    self.info_csv.to_excel("./data/{}.xls".format(
                        value["shop_name"]))
                except ValueError as exc:
                    print("---> The error No.5 is {}".format(exc))
                except Exception as exc:
                    print("---> The error No.6 is {}".format(exc))
                    self.info_csv.to_csv("./data/error_data.csv")
            except FileNotFoundError as exc:
                print("---> The error No.6 is {}".format(exc))
                os.makedirs("./data/")
                self.info_csv.to_excel("./data/{}.xls".format(
                    value["shop_name"]))


def main():
    # login()
    # driver = login_with_cookies()
    # if driver:
    #     UnderWear(driver)
    UnderWear()


if __name__ == "__main__":
    import os
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    main()

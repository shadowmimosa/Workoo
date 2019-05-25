import json
import time
import xlwt
import pandas as pd
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.common.exceptions import NoSuchElementException


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
    def __init__(self, driver=None):
        self.shoplist = [
            "都市丽人官方旗舰店", "浪莎官方旗舰店", "安莉芳官方旗舰店", "奥丽侬官方旗舰店", "黛安芬官方旗舰店"
        ]
        self.shop_url = [
            "https://dushiliren.tmall.com/search.htm?spm=a1z10.3-b-s.0.0.15817191N5vpnX&search=y",
            "https://embryform.tmall.com/category-1325352900.htm?spm=a1z10.1-b-s.w12012752-16996982169.7.10f03608JRsXXN&search=y&parentCatId=951852586&parentCatName=%C8%AB%B2%BF%B1%A6%B1%B4&catName=%CE%C4%D0%D8%D7%A8%C7%F8&scene=taobao_shop#bd"
        ]
        self.driver = driver
        self.info_csv = pd.DataFrame(
            columns=["商品名", "详情链接", "图片", "总销量", "评价数"])
        self.option = "window.open('{}')"
        self.run()

    def login(self):
        login_url_tm = "https://login.tmall.com/?spm=875.7931836/B.a2226mz.1.66144265sckIUN&redirectURL=https%3A%2F%2Fwww.tmall.com%2F"
        options = webdriver.ChromeOptions()
        options.add_argument("disable-infobars")
        options.add_argument("disable-web-security")
        driver = webdriver.Chrome(chrome_options=options)
        driver.maximize_window()
        driver.get(login_url_tm)
        input("请回车登录")
        return driver

    def main(self, url):
        # new_page = self.driver.execute_script(self.option.format(url))
        new_page = self.driver.get(url)
        info_goods = {}

        while True:
            time.sleep(5)
            index = 0
            # self.driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")
            for itme5 in self.driver.find_elements_by_class_name("item5line1"):
                sign = True
                if index > 11:
                    break
                self.driver.execute_script(
                    "arguments[0].scrollIntoView(true);", itme5)
                for item_ in itme5.find_elements_by_tag_name("dl"):
                    detail = item_.find_element_by_tag_name("a")
                    href = detail.get_attribute("href")
                    detail_img = detail.find_element_by_tag_name("img")
                    img = detail_img.get_attribute("src")
                    title = detail_img.get_attribute("alt")

                    sale_num = item_.find_element_by_class_name(
                        "sale-num").text
                    try:
                        evaluate_num = item_.find_element_by_class_name(
                            "rates").find_element_by_tag_name("span").text
                    except NoSuchElementException as exc:
                        print("the error is {}".format(exc))
                        break

                    self.info_csv = self.info_csv.append({
                        "商品名": title,
                        "详情链接": href,
                        "图片": img,
                        "总销量": sale_num,
                        "评价数": evaluate_num
                    },
                                                         ignore_index=True)
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

                    # self.driver.find_element_by_link_text("下一页").click()
            # except UnboundLocalError as exc:
            #     print("the error is {}".format(exc))
            #     self.driver.refresh()
            except Exception as exc:
                print("the error is {}".format(exc))
                break

    def run(self):
        self.driver = self.login()
        for value in self.shop_url:
            self.main(value)

        self.info_csv.drop_duplicates(
            subset=["商品名"], keep='first', inplace=True)
        self.info_csv.to_excel("{}.xls".format(time.time()))


def main():
    # login()
    # driver = login_with_cookies()
    # if driver:
    #     UnderWear(driver)
    UnderWear()


if __name__ == "__main__":
    main()

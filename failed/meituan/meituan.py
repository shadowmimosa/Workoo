import xlwt
from selenium import webdriver
from bs4 import BeautifulSoup
import time

import appium
from appium.webdriver.common.touch_action import TouchAction


class GetInfo(object):
    def __init__(self):
        self.list_url = "http://www.chinaisa.org.cn/gxportal/DispatchAction.do?efFormEname=ECTM40&key=VjVbZAxnAGEFZA45AmVQMVA0UDMDZ1BnUmEJPFg6BDMEF1oVARoCMFFAUBcFElY2"
        self.filename = "./{}.xls"

    def excel_opera(self, i, j, value):
        wbk = xlwt.Workbook()
        sheet = wbk.add_sheet('sheet 1')
        sheet.write(i, j, value)
        wbk.save(self.filename)

    def one_page(self, url):
        browser = webdriver.Chrome()
        # browser = webdriver.Edge()
        browser.get(url)
        browser.implicitly_wait(15)
        time.sleep(10)
        browser.find_element_by_xpath(
            "/html/body/div[2]/div[2]/div/div[2]/div[1]/ul/li[3]/a/h3/div"
        ).click()
        time.sleep(5)
        browser.find_element_by_id("citylist").click()
        time.sleep(10)
        
        search_city = browser.find_element_by_css_selector(
            ".input-city.fl").click()
        search_city = browser.find_element_by_css_selector(
            ".input-city.fl").clear()
        search_city = browser.find_element_by_css_selector(
            ".input-city.fl").send_keys("广州")
        search_city = browser.find_element_by_css_selector(
            ".ca-deepgrey.city-target.active").click()

        search_city = browser.find_element_by_id(
            "searchKeywords").click()
        search_city = browser.find_element_by_id(
            "searchKeywords").clear()
        search_city = browser.find_element_by_id(
            "searchKeywords").send_keys("广州")
        search_city = browser.find_element_by_id(
            "search").click()

        search_city = browser.find_element_by_class_name(
            "input-city fl").click()
        search_city = browser.find_element_by_class_name(
            "input-city fl").clear()
        search_city = browser.find_element_by_class_name(
            "input-city fl").send_keys("广州")
        search_city = browser.find_element_by_class_name(
            "ca-deepgrey city-target active").click()

        browser.switch_to_frame('mframe')
        browser.switch_to_frame('frSheet')
        html = browser.page_source
        browser.close()

        soup = BeautifulSoup(html, 'lxml')
        soup = soup.findAll('tr')

        wbk = xlwt.Workbook()
        sheet = wbk.add_sheet('sheet 1')

        for i, tr in enumerate(soup):
            soup_td = tr.findAll('td')
            for j, td in enumerate(soup_td):
                if i == 0:
                    filename = self.filename.format(td.text)
                sheet.write(i, j, td.text)

        wbk.save(filename)

    def run(self, url):
        self.one_page(url)


class MeituanApp(object):
    def __init__(self):
        self.mix = {
            "platformName":
            "Android",
            "deviceName":
            "d19b1585",
            "platformVersion":
            "9",
            "noReset":
            "true",
            "appPackage":
            "com.sankuai.meituan.takeoutnew",
            "appActivity":
            "com.sankuai.meituan.takeoutnew.ui.page.boot.WelcomeActivity"
        }
        self.yeshen ={
            "platformName":
            "Android",
            "deviceName":
            "127.0.0.1:62025",
            "platformVersion":
            "5",
            "noReset":
            "true",
            "appPackage":
            "com.sankuai.meituan.takeoutnew",
            "appActivity":
            "com.sankuai.meituan.takeoutnew.ui.page.boot.WelcomeActivity"
        }

    # def TouchAction(self,driver):

    def driver_app(self):
        driver = appium.webdriver.Remote("http://127.0.0.1:4723/wd/hub",
                                         self.yeshen)
        time.sleep(10)

        size = driver.get_window_size()
        width = size["width"]
        height = size["height"]
        x1 = width * 0.5
        y1 = height * 0.9
        x2 = width * 0.5
        y2 = height * 0.75
        try:
            el1 = driver.find_element_by_id(
                "com.sankuai.meituan.takeoutnew:id/wm_upgrade_force_cancel")
            el1.click()
        except Exception as exc:
            print(exc)
        try:
            el2 = driver.find_element_by_id("com.sankuai.meituan.takeoutnew:id/close")
            el2.click()
        except Exception as exc:
            print(exc)

        time.sleep(2)

        TouchAction(driver).press(
            x=x1, y=y1).move_to(
                x=x2, y=y1*0.2).release().perform()
        time.sleep(2)

        while True:
            driver.swipe(x1, y1, x2, y2, 500)
            time.sleep(2)
        while True:
            TouchAction(driver).press(
                x=677, y=1581).move_to(
                    x=677, y=1538).release().perform()

            time.sleep(2)


def main(url="http://waimai.meituan.com"):
    import os
    os.chdir(os.path.dirname(os.path.abspath(__file__)))

    run = GetInfo()
    run.run(url)

    # run = MeituanApp()
    # run.driver_app()


if __name__ == "__main__":
    main()
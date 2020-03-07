import time
from appium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pymongo import MongoClient
from time import sleep
from configure import *
import re
from appium.webdriver.common.touch_action import TouchAction


class XianYu():
    def __init__(self):
        """
        初始化
        """
        # 驱动配置
        self.desired_caps = {
            "platformName": "Android",
            "deviceName": "33c5c21a",
            "platformVersion": "9",
            "noReset": "true",
            "newCommandTimeout" : 900,
            "appPackage": "com.taobao.idlefish",
            "appActivity": "com.taobao.fleamarket.home.activity.MainActivity"
        }
        # caps = {}
        # caps["platformName"] = "Android"
        # caps["deviceName"] = "33c5c21a"
        # caps["platformVersion"] = "9"
        # caps["noReset"] = "true"
        # caps["appPackage"] = "com.taobao.idlefish"
        # caps["appActivity"] = "com.taobao.fleamarket.home.activity.MainActivity"
        self.driver = webdriver.Remote(DRIVER_SERVER, self.desired_caps)
        self.wait = WebDriverWait(self.driver, TIMEOUT)

    def crawl(self):
        """
        爬取
        :return:
        """

        while True:
            time.sleep(5)
            # 点击二手
            TouchAction(self.driver).tap(x=145, y=481).perform()
            # 划到列表
            TouchAction(self.driver).press(x=530, y=1879).move_to(
                x=573, y=792).release().perform()
            #
            # xpath = '//android.view.View[@content-desc="Apple苹果iPhone7128G玫瑰金色全网通快递正"]'
            xpath = '/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.RelativeLayout/android.widget.FrameLayout/android.widget.FrameLayout[1]/android.widget.FrameLayout[1]/android.widget.FrameLayout[2]/android.widget.FrameLayout/android.support.v7.widget.RecyclerView'
            '/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.RelativeLayout/android.widget.FrameLayout/android.widget.FrameLayout[1]/android.widget.FrameLayout[1]/android.widget.FrameLayout[2]/android.widget.FrameLayout/android.support.v7.widget.RecyclerView/android.widget.FrameLayout[6]/android.widget.FrameLayout'
            self.driver.f
            a = self.driver.find_element_by_xpath(xpath)
            b = self.driver.find_element_by_class_name('android.support.v7.widget.RecyclerView')
            self.driver.page_source
            c = b.find_element_by_class_name('android.widget.FrameLayout')
            
            [{
                "key": "elementId",
                "value": "31a4ed28-1afa-4e2a-968c-a3b295c3bda4",
                "name": "elementId"
            }, {
                "key": "index",
                "value": "0",
                "name": "index"
            }, {
                "key": "package",
                "value": "com.taobao.idlefish",
                "name": "package"
            }, {
                "key": "class",
                "value": "android.view.View",
                "name": "class"
            }, {
                "key": "text",
                "value": "",
                "name": "text"
            }, {
                "key": "content-desc",
                "value": "Apple苹果iPhone7128G玫瑰金色全网通快递正",
                "name": "content-desc"
            }, {
                "key": "checkable",
                "value": "false",
                "name": "checkable"
            }, {
                "key": "checked",
                "value": "false",
                "name": "checked"
            }, {
                "key": "clickable",
                "value": "false",
                "name": "clickable"
            }, {
                "key": "enabled",
                "value": "true",
                "name": "enabled"
            }, {
                "key": "focusable",
                "value": "false",
                "name": "focusable"
            }, {
                "key": "focused",
                "value": "false",
                "name": "focused"
            }, {
                "key": "long-clickable",
                "value": "false",
                "name": "long-clickable"
            }, {
                "key": "password",
                "value": "false",
                "name": "password"
            }, {
                "key": "scrollable",
                "value": "false",
                "name": "scrollable"
            }, {
                "key": "selected",
                "value": "false",
                "name": "selected"
            }, {
                "key": "bounds",
                "value": "[58,1344][504,1458]",
                "name": "bounds"
            }, {
                "key": "displayed",
                "value": "true",
                "name": "displayed"
            }]
            print()
            # 当前页面显示的所有状态
            # items = self.wait.until(
            #     EC.presence_of_all_elements_located((
            #         By.XPATH,
            #         '/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.RelativeLayout/android.widget.RelativeLayout[2]/android.widget.RelativeLayout/android.widget.RelativeLayout/android.widget.FrameLayout/com.uc.webview.export.WebView/com.uc.webkit.aw/android.webkit.WebView/android.view.View[1]/android.view.View/android.view.View[3]/android.view.View[2]/android.view.View[1]'
            #     )))
            # 上滑
            # a = self.wait.until(
            #     EC.presence_of_all_elements_located((
            #         By.XPATH,
            #         '/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.RelativeLayout/android.widget.RelativeLayout[2]/android.widget.RelativeLayout/android.widget.RelativeLayout/android.widget.FrameLayout/com.uc.webview.export.WebView/com.uc.webkit.aw/android.webkit.WebView/android.view.View[1]/android.view.View/android.view.View[3]/android.view.View[3]'
            #     )))
            # for b in a:
            #     pass
            # c = self.wait.until(
            #     EC.presence_of_all_elements_located((
            #         By.XPATH,
            #         '/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.RelativeLayout/android.widget.RelativeLayout[2]/android.widget.RelativeLayout/android.widget.RelativeLayout/android.widget.FrameLayout/com.uc.webview.export.WebView/com.uc.webkit.aw/android.webkit.WebView/android.view.View[1]/android.view.View/android.view.View[3]/android.view.View[3]'
            #     )))
            # d = self.wait.until(
            #     EC.presence_of_all_elements_located((
            #         By.XPATH,
            #         '/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.RelativeLayout/android.widget.RelativeLayout[2]/android.widget.RelativeLayout/android.widget.RelativeLayout/android.widget.FrameLayout/com.uc.webview.export.WebView/com.uc.webkit.aw/android.webkit.WebView/android.view.View[1]/android.view.View/android.view.View[3]/android.view.View'
            #     )))
            e = self.wait.until(
                EC.presence_of_all_elements_located((
                    By.XPATH,
                    '/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.RelativeLayout/android.widget.RelativeLayout[2]/android.widget.RelativeLayout/android.widget.RelativeLayout/android.widget.FrameLayout/com.uc.webview.export.WebView/com.uc.webkit.aw/android.webkit.WebView/android.view.View[1]/android.view.View/android.view.View[3]/android.view.View[3]/android.view.View'
                )))
            # for item in e:
            #     # g = self.wait.until(
            #     #     EC.presence_of_all_elements_located((
            #     #         By.XPATH,
            #     #         '/android.view.View'
            #     #     )))
            #     g = item.find_elements_by_xpath("/android.view.View")
            #     h = item.find_elements_by_tag_name("android.view.View")
            # f = WebDriverWait(c[0], TIMEOUT).until(
            #     EC.presence_of_all_elements_located((By.XPATH,
            #                                          '/android.view.View')))
            # .find_element_by_id('cn.neoclub.uki:id/tv_gender').get_attribute('text')
            print(len(e))
            # 遍历每条状态
            # for item in items:
            #     try:
            #         # 昵称
            #         nickname = item.find_element_by_id(
            #             'cn.neoclub.uki:id/tv_name').get_attribute('text')

            #         print("nk", nickname)

            #         age = item.find_element_by_id(
            #             'cn.neoclub.uki:id/tv_gender').get_attribute('text')

            #         print("age", age)

            #         content = item.find_element_by_id(
            #             'cn.neoclub.uki:id/expandable_text').get_attribute(
            #                 'text')

            #         print("content", content)

            #         data = {
            #             'nickname': nickname,
            #             'content': content,
            #             'age': age,
            #         }
            #         # 插入MongoDB
            #         result = self.table.update({'nickname': nickname},
            #                                    {'$set': data}, True)
            #         if result["ok"] == 1:
            #             print("sucess insert")
            #         sleep(SCROLL_SLEEP_TIME)
            #     except NoSuchElementException:
            #         print("element not found")
            self.driver.swipe(FLICK_START_X, FLICK_START_Y + FLICK_DISTANCE,
                              FLICK_START_X, FLICK_START_Y)

    def main(self):
        """
        入口
        :return:
        """
        self.crawl()


if __name__ == '__main__':
    xy = XianYu()
    xy.main()
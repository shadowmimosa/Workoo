from appium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pymongo import MongoClient
from time import sleep
from configure import *
import re


class UKI():
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
            "appPackage": "com.eg.android.AlipayGphone",
            "appActivity": "com.eg.android.AlipayGphone.AlipayLogin"
        }
        self.driver = webdriver.Remote(DRIVER_SERVER, self.desired_caps)
        self.wait = WebDriverWait(self.driver, TIMEOUT)

    def crawl(self):
        """
        爬取
        :return:
        """

        while True:
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
        #     # 登录
        #     self.login()
        #     # 进入动态广场
        #     self.enter()
        # 爬取
        self.crawl()


if __name__ == '__main__':
    uki = UKI()
    uki.main()
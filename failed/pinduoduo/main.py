import json
import time
import pandas as pd
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException, TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class UnderWear(object):
    """这是一个类注释，不想写了 XD
    """

    def __init__(self):
        """初始化类变量"""

        # 存放店铺名、网址、class name(商品列表每行的 class 名)
        self.shop_url = [
            # {
            #     "shop_name": "都市丽人官方旗舰店",
            #     "url":
            #     "https://dushiliren.tmall.com/category-1444868252.htm?spm=a1z10.3-b-s.w4011-17964102365.2.4eca7191L0ea0j&tsearch=y&orderType=hotsell_desc#TmshopSrchNav",
            #     "class_name": "item5line1"
            # },
            # {
            #     "shop_name": "浪莎官方旗舰店",
            #     "url":
            #     "https://langsha.tmall.com/category-746322913.htm?spm=a1z10.5-b-s.w4011-14903041178.54.804a6a9crFknF6&catId=746322913&search=y&orderType=",
            #     "class_name": "item4line1"
            # },
            # {
            #     "shop_name": "安莉芳官方旗舰店",
            #     "url":
            #     "https://embryform.tmall.com/category-1325352900.htm?spm=a1z10.5-b-s.w4011-16991628392.120.7ee13328dSyrEl&parentCatId=951852586&parentCatName=%C8%AB%B2%BF%B1%A6%B1%B4&catName=%CE%C4%D0%D8%D7%A8%C7%F8&scene=taobao_shop&catId=1325352900&search=y&orderType=hotsell_desc",
            #     "class_name": "item4line1"
            # },
            # {
            #     "shop_name": "奥丽侬官方旗舰店",
            #     "url":
            #     "https://oleno.tmall.com/search.htm?spm=a1z10.1-b-s.0.0.68d64be9Dsmjvi&search=y&orderType=hotsell_desc",
            #     "class_name": "item5line1"
            # },
            {
                "shop_name": "黛安芬官方旗舰店",
                "url":
                "https://triumph.tmall.com/category-1342251415.htm?spm=a1z10.3-b-s.w4011-14455904009.107.125343d2OBlE74&catId=1342251415&scene=taobao_shop&search=y&orderType=&tsearch=y",
                "class_name": "item5line1"
            }
        ]
        self.columns = ["商品名", "价格", "详情链接", "图片", "总销量", "评价数"]

        # 运行入口
        self.run()

    def login(self):
        # login_url_tm = "https://login.tmall.com/?spm=875.7931836/B.a2226mz.1.66144265sckIUN&redirectURL=https%3A%2F%2Fwww.tmall.com%2F"
        login_url_tm = "http://mobile.yangkeduo.com/search_result.html?search_key=%E5%B0%8F%E7%86%8A%E9%9E%8B%E5%BA%95%E5%A5%B3%E8%80%81%E7%88%B9%E9%9E%8B%E5%A5%B3%E7%BD%91%E9%9D%A2%E8%BF%90%E5%8A%A8%E9%9E%8B%E5%AD%A6%E7%94%9F%E9%9F%A9%E7%89%88%E7%99%BE%E6%90%AD%E4%BC%91%E9%97%B2%E9%80%8F%E6%B0%94%E5%B0%8F%E7%99%BD%E9%9E%8B%E5%A5%B3%E5%8D%95%E9%9E%8B&search_src=history&search_met=history_sort&search_met_track=history&refer_page_name=search&refer_page_id=10031_1557901491321_NNX4m2WhpX&refer_page_sn=10031"

        # selenium 启动参数
        options = webdriver.ChromeOptions()
        options.add_argument("disable-infobars")
        options.add_argument("disable-web-security")
        # options.add_argument("--headless")
        options.add_argument("--start-maximized")
        options.add_argument("--log-level=3")
        options.add_experimental_option('excludeSwitches', ['enable-automation'])

        driver = webdriver.Chrome(chrome_options=options)
        driver.get("http://mobile.yangkeduo.com/classification.html?refer_page_name=index&refer_page_id=10002_1555207365815_0AHDgZbiS9&refer_page_sn=10002")

        self.driver = driver
        WebDriverWait(driver, 15, 0.5).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR,
                                                    "._2E7OKz5i.inline-flex")))
        driver.find_element_by_css_selector("._2E7OKz5i.inline-flex").click()
        WebDriverWait(driver, 15, 0.5).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR,
                                                    "._3jYwhMbl")))
        driver.find_element_by_css_selector("._3jYwhMbl").send_keys("电脑")
        WebDriverWait(driver, 15, 0.5).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR,
                                                    "._1fALnEid")))
        driver.find_element_by_css_selector("._1fALnEid").click()
        WebDriverWait(driver, 15, 0.5).until(
                    EC.presence_of_element_located((By.CLASS_NAME,
                                                    "nN9FTMO2")))
        goods = driver.find_elements_by_class_name("nN9FTMO2")
        for good in goods:
            sales = good.find_element_by_class_name("_2KLtl24M")

            if "万" not in sales:
                sale =int(sales.text.replace("已拼","").repalce("件",""))
                driver.execute_script(
                    "arguments[0].scrollIntoView(true);", itme5)
                if sale <5000:
                    sales.click()
                    WebDriverWait(driver, 15, 0.5).until(
                                EC.presence_of_element_located((By.CLASS_NAME,
                                                                "goods-mall-btn")))
                    driver.find_element_by_class_name("goods-mall-btn").click()


            
        
        # 等待登录，90 秒超时；超时后将退出
        print("---> 90 秒内完成登录")
        index = 0
        while True:
            try:
                WebDriverWait(driver, 15, 0.5).until(
                    EC.presence_of_element_located((By.CLASS_NAME,
                                                    "slider-content")))
                break
            except TimeoutException as exc:
                index += 1
                if index >= 6:
                    print("登录超时")
                    driver.quit()
                    return False

                # try:
                #     self.driver.switch_to.frame(
                #         self.driver.find_element_by_tag_name("iframe"))
                #     WebDriverWait(self.driver, 5, 0.5).until(
                #         EC.presence_of_element_located((By.ID, "J_Other")))
                #     self.login_judge()
                # except TimeoutException as exc:
                #     self.login_judge()

                print("已经等待 {} 秒，90 秒后将超时".format(index * 15))

        return True

    def login_judge(self):
        """模拟登录时，手机验证"""
        # element = self.driver.switch_to_frame(self.driver.find_element_by_tag_name("iframe"))
        element = self.driver.find_element_by_id("J_Other")
        tel_num = element.find_element_by_class_name(
            "new-phone-current").text  # 手机号
        element.find_element_by_css_selector(
            ".act-btn-gray.act-btn-gray-hover.send-code-btn.send-code-btn-securityPhone.J_SendCodeBtn_SecurityPhone"
        ).click()  # 点击 获取验证码

        safe_code = input("请输入验证码")
        element.find_element_by_css_selector(
            ".new-phone-input.safe-code.J_SafeCode").clear()
        element.find_element_by_css_selector(
            ".new-phone-input.safe-code.J_SafeCode").send_keys(safe_code)
        element.find_element_by_css_selector(
            ".act-btn-gray.act-btn-gray-hover.submit-btn").click()

        # 等待短信验证，60 秒超时
        print("---> 90 秒内短信验证")
        index = 0
        while True:
            try:
                WebDriverWait(driver, 15, 0.5).until(
                    EC.presence_of_element_located((By.CLASS_NAME,
                                                    "slider-content")))
                break
            except TimeoutException as exc:
                index += 1
                print("已经等待 {} 秒，60 秒后将超时".format(index * 15))
                if index >= 4:
                    print("验证超时")
                    driver.quit()
                    return False
        return True

    def details(self, url):
        """获取商品细节信息"""

        # 新标签页打开，并切换标签页
        self.driver.execute_script("window.open('{}')".format(url))
        windows = self.driver.window_handles
        self.driver.switch_to_window(windows[-1])

        try:
            # 循环等待，直到获取到元素
            while True:
                try:
                    WebDriverWait(self.driver, 15, 0.5).until(
                        EC.presence_of_element_located((By.CLASS_NAME,
                                                        "tm-count")))
                    WebDriverWait(self.driver, 15, 0.5).until(
                        EC.presence_of_element_located((By.CLASS_NAME,
                                                        "tm-indcon")))

                    count = self.driver.find_elements_by_class_name(
                        "tm-indcon")
                    self.info_goods["月销量"] = count[
                        0].find_element_by_class_name("tm-count").text
                    self.info_goods["评价数"] = count[
                        1].find_element_by_class_name("tm-count").text
                    break
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
        except Exception as exc:
            print("1", exc)
            try:
                self.driver.find_elements_by_link_text("无法访问此网站")
                print("刷新")
                self.driver.refresh()
            except Exception as exc:
                print("2", "exc")
                self.driver.refresh()

        # 关闭新标签页，并切回原标签页
        self.driver.close()
        self.driver.switch_to_window(windows[0])

    def find_price(self, element):
        return element.find_element_by_class_name(
            "cprice-area").find_elements_by_tag_name("span")[-1].text

    def main(self, content):
        """爬虫主函数，处理商品列表页"""

        self.driver.get(content["url"])

        # 循环遍历商品列表，自动翻页
        while True:

            # 判断数据长度，大于 210，中止
            if self.judge_length():
                break

            WebDriverWait(self.driver, 15, 0.5).until(
                EC.presence_of_element_located(
                    (By.CLASS_NAME, content["class_name"])))  # 隐式等待 15 秒

            index = 0  # 商品行索引，为了排除推荐行

            elements = self.driver.find_elements_by_class_name(
                content["class_name"])  #在商品列表中按行寻找
            length = len(elements)

            # 遍历每行
            for itme5 in elements:
                sign = True
                if self.judge_length():
                    break

                # 末尾两行为推荐商品，舍弃
                if index > length - 3:
                    break
                self.driver.execute_script(
                    "arguments[0].scrollIntoView(true);", itme5)  # 按行滚动视图

                # 遍历单个商品
                for item_ in itme5.find_elements_by_tag_name("dl"):
                    if self.judge_length():
                        break
                    info_goods = {}  # 初始化

                    # 读取商品数据
                    detail = item_.find_element_by_tag_name("a")
                    info_goods["详情链接"] = detail.get_attribute("href")
                    detail_img = detail.find_element_by_tag_name("img")
                    info_goods["图片"] = detail_img.get_attribute("src").replace(
                        "_180x180.jpg", "")
                    info_goods["商品名"] = detail_img.get_attribute("alt")

                    info_goods["价格"] = self.find_price(item_)

                    # 尝试获取销量
                    try:
                        info_goods["总销量"] = item_.find_element_by_class_name(
                            "sale-num").text
                    except NoSuchElementException as exc:
                        print("---> Can't find sale_num")

                    self.info_goods = info_goods  # 赋值类变量

                    # 获取商品详情
                    try:
                        self.details(info_goods["详情链接"])
                    except Exception as exc:
                        print(
                            "---> The detail page was failed, the error is {}".
                            format(exc))
                    self.info_csv = self.info_csv.append(
                        self.info_goods, ignore_index=True)

                index += 1  # 索引加一

            # 尝试寻找 下一页 并点击，如果失败则表示翻页结束
            try:
                # 判断 sign, True 时尝试加载下一页，否则刷新页面
                if sign:
                    next_button = self.driver.find_element_by_class_name(
                        "pagination").find_element_by_css_selector(
                            ".J_SearchAsync.next")  # 寻找 下一页 标签
                    if next_button:
                        next_button.click()  # 点击 下一页
                    sign = False
                else:
                    self.driver.refresh()  # 刷新
                    print("---> Refreshing page now")

            except Exception as exc:
                print("---> The error No.3 is {}".format(exc))
                break

    def judge_length(self):
        return self.info_csv.shape[0] > 210

    def run(self):
        """运行函数"""

        # 登录，90 秒超时后，程序结束
        if not self.login():
            return

        # 遍历店铺列表，分别处理
        for value in self.shop_url:
            self.info_csv = pd.DataFrame(columns=self.columns)  # 初始化 dataframe

            try:
                self.main(value)  # 进入爬虫程序
            except Exception as exc:
                print("---> The error No.4 is {}".format(exc))
                self.info_csv.to_csv("./data/error_data.csv")

            self.info_csv.drop_duplicates(
                subset=["商品名"], keep='first', inplace=True)

            # 保存
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
                print("---> The error No.7 is {}".format(exc))
                os.makedirs("./data/")
                self.info_csv.to_excel("./data/{}.xls".format(
                    value["shop_name"]))


def main():
    """主函数"""

    UnderWear()


if __name__ == "__main__":
    # 切换运行路径到当前文件路径
    import os
    os.chdir(os.path.dirname(os.path.abspath(__file__)))

    # 主函数入口
    main()

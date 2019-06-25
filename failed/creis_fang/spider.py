import json
import time
import pandas as pd
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException, TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup as bf
import xlwt


class UnderWear(object):
    """这是一个类注释，不想写了 XD
    """

    def __init__(self):
        """初始化类变量"""
        self.url = "https://creis.fang.com/"

        self.columns = ["名称"]

        # 运行入口
        self.run()

    def login(self):
        url_tm = "https://creis.fang.com/"

        # selenium 启动参数
        options = webdriver.ChromeOptions()
        options.add_argument("disable-infobars")
        options.add_argument("disable-web-security")
        # options.add_argument("--headless")
        options.add_argument("--start-maximized")
        options.add_argument("--log-level=3")
        options.add_experimental_option('excludeSwitches',
                                        ['enable-automation'])

        driver = webdriver.Chrome(chrome_options=options)
        driver.get(self.url)

        self.driver = driver

        input("---> 90 秒内完成登录")

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

    def del_info(self):
        windows = self.driver.window_handles
        self.driver.switch_to_window(windows[-1])
        WebDriverWait(self.driver, 15, 0.5).until(
            EC.presence_of_element_located((By.CLASS_NAME, "content")))

        html = self.driver.find_element_by_class_name("content")

        with open(
                "./temp/{}.txt".format(int(time.time())), "w",
                encoding="utf-8") as fn:
            fn.write(html.text)

        self.driver.close()
        self.driver.switch_to_window(windows[0])

    def run(self):
        """运行函数"""

        # 登录，90 秒超时后，程序结束
        if self.login():
            count = 0
            while True:
                time.sleep(10)
                table = self.driver.find_element_by_id("result")
                trs = table.find_elements_by_tag_name("tr")
                for tr in trs:
                    if count >= 15:
                        break
                    # tr.find_element_by_tag_name("td").click()
                    # self.del_info()
                    try:
                        tr.find_element_by_tag_name("td").click()
                        self.del_info()
                        count += 1
                    except NoSuchElementException as exc:
                        continue

                for index in range(1,51):
                    self.driver.find_element_by_css_selector(".f_inpbox.fg_w17").input(str(index))
                    time.sleep(2)
                    self.driver.find_element_by_class_name("but_confirm").click()
                # self.driver.find_element_by_css_selector(
                #     "#listPager > li:nth-child(9) > a").click()

            html = self.driver.page_source
            soup = bf(html, 'lxml')
            table = soup.findAll(
                "table", attrs={"class": ["tbbox01", "tbbox02"]})
            trs = table.findAll("tr", attrs={"name": ["land"]})
            td = trs.find("td")

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

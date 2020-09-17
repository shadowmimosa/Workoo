import csv
import json
import time
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException, TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains

from utils import request, run_func

from skimage import io


def magic_time(during=3):
    def decorator(func):
        def wrapper(*args, **kwargs):
            start_time = time.time()
            # print('函数开始运行的时间为：', time.strftime('%Y:%m:%d %H:%M:%S', start_time))
            result = func(*args, **kwargs)
            magic = time.time() - start_time - during

            if magic < 0:
                time.sleep(-magic)

            return result

        return wrapper

    return decorator


class OperaChrome(object):
    def __init__(self, path=None):
        self.init_chrome(path)

    def get_proxy(self):
        resp = req().run(
            path=
            'http://route.xiongmaodaili.com/xiongmao-web/api/glip?secret=3648c286d4be950dfeb744412178bab8&orderNo=GL20191218133200tOpTjxj6&count=1&isTxt=1&proxyType=1'
        )
        return remove_charater(resp)

    def init_chrome(self, path):
        options = webdriver.ChromeOptions()
        options.add_argument("disable-infobars")
        options.add_argument("disable-web-security")
        options.add_argument("--headless")
        options.add_argument("--start-maximized")
        options.add_argument('--log-level=3')
        options.add_argument('--ignore-certificate-errors')
        options.add_experimental_option('excludeSwitches',
                                        ['enable-automation'])

        # options.add_argument('--proxy-server=http://{}'.format(
        #     self.get_proxy()))

        prefs = {"profile.managed_default_content_settings.images": 2}
        options.add_experimental_option("prefs", prefs)
        driver = webdriver.Chrome(executable_path="./chromedriver.exe",
                                  options=options)
        # driver = webdriver.Edge()
        if path is not None:
            driver.get(path)

        self.driver = driver

    def judge_driver(self, driver):
        if driver is None:
            return self.driver
        else:
            return driver

    @magic_time()
    def waiting_by_xpath(self, xpath, driver=None, timeout=15):
        driver = self.judge_driver(driver)

        while True:
            try:
                WebDriverWait(driver, timeout, 0.1).until(
                    EC.presence_of_element_located((By.XPATH, xpath)))
            except IndexError as exc:
                print("---> Waiting for tm-indcon")
                continue
            except StaleElementReferenceException as exc:
                print("---> Waiting for count monthly")
                continue
            except TimeoutException:
                print('timeout')
                return False
            else:

                return True

    @magic_time()
    def waiting_by_class_name(self, xpath, driver=None, timeout=15):
        driver = self.judge_driver(driver)

        while True:
            try:
                WebDriverWait(driver, timeout, 0.1).until(
                    EC.presence_of_element_located((By.CLASS_NAME, xpath)))
            except IndexError as exc:
                print("---> Waiting for tm-indcon")
                continue
            except StaleElementReferenceException as exc:
                print("---> Waiting for count monthly")
                continue
            except TimeoutException:
                print('timeout')
                return False
            else:

                return True

    def click_by_xpath(self, xpath, driver=None, timeout=15):
        driver = self.judge_driver(driver)

        if self.waiting_by_xpath(xpath, timeout=timeout):
            driver.find_element_by_xpath(xpath).click()

    def click_by_class_name(self, xpath, driver=None, timeout=15):
        driver = self.judge_driver(driver)

        if self.waiting_by_class_name(xpath, timeout=timeout):
            driver.find_element_by_class_name(xpath).click()

    def find_element_by_xpath(self, xpath, driver=None, timeout=15):
        driver = self.judge_driver(driver)

        if self.waiting_by_xpath(xpath, timeout=timeout):
            return driver.find_element_by_xpath(xpath)

    def find_elements_by_xpath(self, xpath, driver=None, timeout=15):
        driver = self.judge_driver(driver)

        if self.waiting_by_xpath(xpath, timeout=timeout):
            return driver.find_elements_by_xpath(xpath)

    def find_element_by_class_name(self, xpath, driver=None, timeout=15):
        driver = self.judge_driver(driver)

        if self.waiting_by_class_name(xpath, timeout=timeout):
            return driver.find_element_by_class_name(xpath)

    def find_elements_by_class_name(self, xpath, driver=None, timeout=15):
        driver = self.judge_driver(driver)

        if self.waiting_by_class_name(xpath, timeout=timeout):
            return driver.find_elements_by_class_name(xpath)

    def input(self, xpath, driver=None, keyword='', timeout=15):
        driver = self.judge_driver(driver)

        if self.waiting_by_xpath(xpath, timeout=timeout):
            driver.find_element_by_xpath(xpath).send_keys(keyword)


def remove_charater(content: str):
    return content.replace('\n', '').replace('\t',
                                             '').replace('\r',
                                                         '').replace(' ', '')


def get_shop_phone(link: str):
    shop_id = link.split('id=')[-1]
    uri = f'https://luban.snssdk.com/shop/info?id={shop_id}'
    header = {
        'User-Agent':
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.102 Safari/537.36',
        'Accept': '*/*',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.9'
    }
    resp = request(uri, header, json=True)
    return resp.get('data').get('company_name'), resp.get('data').get('mobile')


def get_good_phone(link):
    good_id = link.split('id=')[-1]
    uri = f'https://ec.snssdk.com/product/lubanajaxstaticitem?id={good_id}'
    header = {
        'User-Agent':
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.102 Safari/537.36',
        'Accept': 'application/json, text/plain, */*',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.9'
    }
    resp = request(uri, header, json=True)
    return resp.get('data').get('mobile')


@run_func()
def detail(chrome, supplier):

    info = {}
    # 产品价格,支付方式,产品店铺,24小时销量,3天销量,7天销量,产品类别,产品名,抢购电话,公司名,公司电话,产品链接
    info['产品价格'] = chrome.find_element_by_class_name('el-table_1_column_8',
                                                     supplier).text
    info['支付方式'] = chrome.find_element_by_class_name('el-table_1_column_6',
                                                     supplier).text
    info['24小时销量'] = chrome.find_element_by_class_name('el-table_1_column_10',
                                                       supplier).text
    info['3天销量'] = chrome.find_element_by_class_name('el-table_1_column_11',
                                                     supplier).text
    info['7天销量'] = chrome.find_element_by_class_name('el-table_1_column_12',
                                                     supplier).text
    info['产品类别'] = chrome.find_element_by_class_name('el-table_1_column_5',
                                                     supplier).text

    temp = chrome.find_element_by_class_name('el-table_1_column_2', supplier)
    info['产品名'] = temp.text
    info['产品链接'] = temp.find_element_by_xpath('.//div/a[2]').get_attribute(
        'href')

    temp = chrome.find_element_by_class_name('el-table_1_column_3', supplier)
    info['产品店铺'] = temp.text
    shop_link = temp.find_element_by_xpath('.//div/a[2]').get_attribute('href')
    info['公司名'], info['公司电话'] = get_shop_phone(shop_link)

    info['抢购电话'] = get_good_phone(info['产品链接'])

    writer(info)


def writer(row):
    header = [
        '产品价格', '支付方式', '产品店铺', '24小时销量', '3天销量', '7天销量', '产品类别', '产品名',
        '抢购电话', '公司名', '公司电话', '产品链接'
    ]
    with open('data.csv', 'a', encoding='utf-8') as fn:
        f_csv = csv.DictWriter(fn, header)
        f_csv.writerow(row)


def main():
    chrome = OperaChrome('https://www.erlangcha.com/')
    chrome.click_by_xpath(
        '//*[@id="app"]/div/div[2]/section/div/div[2]/div/div[2]/div[2]/table/thead/tr/th[12]/div/span/i[2]'
    )
    while True:
        elements = chrome.find_elements_by_class_name('el-table__row')

        for supplier in elements:
            chrome.driver.execute_script('arguments[0].scrollIntoView(true);',
                                         supplier)
            detail(chrome, supplier)

        chrome.click_by_class_name('el-icon-arrow-right')


if __name__ == "__main__":
    main()

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

from utils.soup import DealSoup


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

    #     self.init_phone(path)

    # def __init__(self):
    #     self.WIDTH = 320
    #     self.HEIGHT = 640
    #     self.PIXEL_RATIO = 3.0
    #     self.UA = 'Mozilla/5.0 (Linux; Android 4.1.1; GT-N7100 Build/JRO03C) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/35.0.1916.138 Mobile Safari/537.36 T7/6.3'

    # def start(self):
    #     mobileEmulation = {
    #         "deviceMetrics": {
    #             "width": self.WIDTH,
    #             "height": self.HEIGHT,
    #             "pixelRatio": self.PIXEL_RATIO
    #         },
    #         "userAgent": self.UA
    #     }
    #     options = webdriver.ChromeOptions()
    #     options.add_experimental_option('mobileEmulation', mobileEmulation)
    #     driver = webdriver.Chrome(chrome_options=options)

    def init_chrome(self, path):
        options = webdriver.ChromeOptions()
        options.add_argument("disable-infobars")
        options.add_argument("disable-web-security")
        # options.add_argument("--headless")
        options.add_argument("--start-maximized")
        options.add_argument('--log-level=3')
        options.add_argument('--ignore-certificate-errors')
        options.add_experimental_option('excludeSwitches',
                                        ['enable-automation'])

        # options.add_argument('--proxy-server=http://121.226.215.242:9999')

        # prefs = {"profile.managed_default_content_settings.images": 2}
        # options.add_experimental_option("prefs", prefs)
        driver = webdriver.Chrome(executable_path="./chromedriver.exe",
                                  options=options)
        if path is not None:
            driver.get(path)

        self.driver = driver

    def judge_driver(self, driver):
        if driver is None:
            return self.driver
        else:
            return driver

    @magic_time()
    def waiting(self, xpath, driver=None, timeout=15):
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

    def click(self, xpath, driver=None, timeout=15):
        driver = self.judge_driver(driver)

        if self.waiting(xpath, timeout=timeout):
            driver.find_element_by_xpath(xpath).click()

    def input(self, xpath, driver=None, keyword='', timeout=15):
        driver = self.judge_driver(driver)

        if self.waiting(xpath, timeout=timeout):
            driver.find_element_by_xpath(xpath).send_keys(keyword)


def remove_charater(content: str):
    return content.replace('\n', '').replace(' ', '')


def login(driver):
    login_xpath = '//*[@id="J_QRCodeLogin"]/div[5]/a[1]'
    account_path = '//*[@id="J_Form"]/div[2]/span'
    password_path = '//*[@id="TPL_password_1"]'
    login_button = '//*[@id="J_SubmitStatic"]'


def good_detail(html, path: str):
    info = {}
    # {'产品名称' '产品价格' '产品评论量' '产品评论等级' '产品交易量' '产品网址'}
    soup = DealSoup()
    # info['产品名称'] = driver.find_element_by_class_name('d-title').text
    # info['产品价格'] = driver.find_element_by_class_name(
    #     'has-discount-sku').find_element_by_class_name('value').text
    # info['产品评论量'] = driver.find_element_by_class_name(
    #     'mod-detail-otabs').find_element_by_tag_name('em')
    info['产品名称'] = soup.judge(html, attr={'class': 'd-title'}).text
    info['产品价格'] = ''
    temp = soup.judge(html,
                      attr={'class': 'd-content static-content'},
                      all_tag=True)[1]
    info['产品评论量'] = soup.judge(soup.judge(html,
                                          attr={'class': 'bargain-number'}),
                               attr='em').text
    info['产品评论等级'] = soup.judge(html, attr={'class': 'star-score'}).text
    info['产品交易量'] = soup.judge(soup.judge(
        html, attr={'class': 'satisfaction-number'}),
                               attr='em').text
    info['产品网址'] = path.split('?')[0]

    return info


def shop_detail(html):
    soup = DealSoup()
    info = {}

    info_box = soup.judge(html, attr={'class': 'info-box'})
    info['供应商名称'] = soup.judge(info_box, attr={'class': 'name-text'}).text
    info['诚信通年数'] = soup.judge(info_box,
                               attr={
                                   'class': 'icon icon-chengxintong'
                               }).text
    info['诚信等级'] = soup.judge(info_box, attr={
        'class': 'icon icon-credit-pm'
    }).text

    li_list = soup.judge(soup.judge(html, attr={'class': 'section-main'}),
                         attr='li',
                         all_tag=True)

    info['累计成交数'] = soup.judge(li_list[0], attr={'class': 'record-num'}).text
    info['累计买家数'] = soup.judge(li_list[1], attr={'class': 'record-num'}).text
    info['重复购买率'] = soup.judge(li_list[2], attr={'class': 'record-num'}).text
    info['退货率'] = soup.judge(li_list[3], attr={'class': 'record-num'}).text

    for key, value in info.items():
        info[key] = remove_charater(value)

    info['诚信通年数'] = info['诚信通年数'].replace('第', '').replace('年', '')

    return info


def write(content=None):
    title_list = [
        '供应商名称', '诚信通年数', '诚信等级', '累计成交数', '累计买家数', '退货率', '产品名称', '产品价格',
        '产品评论量', '产品评论等级', '产品交易量', '产品网址'
    ]
    if content is None:
        need = title_list
    else:
        need = [content[key] for key in title_list]

    with open('./data/data.csv', 'a', encoding='utf-8') as fn:
        writer = csv.writer(fn)
        writer.writerow(need)


def main():
    login_path = 'https://login.1688.com'
    home_path = 'https://auto.1688.com/'
    dropdown_path = '/html/body/div[2]/div[1]/div/div/div/div/div/div/div/div/div[3]/div/form/div/div/div[1]/span/i'
    supplier_path = '/html/body/div[4]/div/div/ul/li[3]'
    input_path = '/html/body/div[2]/div[1]/div/div/div/div/div/div/div/div/div[3]/div/form/div/div/div[1]/div/input'
    button_path = '/html/body/div[2]/div[1]/div/div/div/div/div/div/div/div/div[3]/div/form/div/div/div[2]/button'

    with open('./data/already.txt', 'r', encoding='utf-8') as fn:
        already = fn.readlines()

    write()
    category = [
        '车载mp3', '行车记录仪', 'GPS定位器', '车载空气净化器', '车载吸尘器', '车载摄像头', '车载充电器',
        '车载显示器', '车载手机支架', '车载蓝牙耳机', '车载蓝牙音箱', '车载储物', '车载冰箱', '车载充电器', '车载逆变器'
    ]
    chrome = OperaChrome(login_path)
    time.sleep(10)

    chrome.driver.get(home_path)
    chrome.click(dropdown_path)
    chrome.click(supplier_path)
    chrome.input(input_path, keyword='车载mp3')
    chrome.click(button_path)

    elements = chrome.driver.find_elements_by_class_name('company-list-item')
    for supplier in elements:
        chrome.driver.execute_script('arguments[0].scrollIntoView(true);',
                                     supplier)

        title = supplier.find_element_by_class_name(
            'list-item-title-text').get_attribute("title")
        if title in already:
            continue

        chrome.driver.find_element_by_class_name('list-item-itemsWrap').click()
        chrome.driver.switch_to_window(chrome.driver.window_handles[-1])
        chrome.click('//*[@id="mod-detail-otabs"]/div/ul/li[3]')
        good_info = good_detail(chrome.driver.page_source,
                                chrome.driver.current_url)

        chrome.driver.find_element_by_class_name('creditdetail-page').click()
        chrome.driver.switch_to_window(chrome.driver.window_handles[-1])
        shop_info = shop_detail(chrome.driver.page_source)

        chrome.driver.close()
        chrome.driver.switch_to_window(chrome.driver.window_handles[-1])
        # chrome.driver.close()
        # chrome.driver.switch_to_window(chrome.driver.window_handles[-1])
        write({**good_info, **shop_info})
        print()

    print(chrome)


if __name__ == "__main__":
    main()
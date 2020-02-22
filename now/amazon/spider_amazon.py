'''
Empty
'''
# import warnings
# import matplotlib
# warnings.filterwarnings("ignore",category=matplotlib.MatplotlibDeprecationWarning)

import os
import re
import sys
import json
import time
import hashlib
import requests
from urllib.parse import urlencode
# from skimage import io
from selenium import webdriver
# from seleniumwire import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException, TimeoutException, InvalidSelectorException, ElementNotVisibleException
from utils.excel_opea import ExcelOpea
from utils.request import Query
from utils.soup import DealSoup



def remove_charater(content: str):
    return content.replace('\n', '').replace('\t',
                                             '').replace('\r',
                                                         '').replace(' ', '')


def get_proxy():
    with open('./proxy.txt', 'r', encoding='utf-8') as fn:
        link = remove_charater(fn.readline())
    if link:
        resp = requests.get(link)
        ip = remove_charater(resp.text)

        if 'code' not in ip:
            print('proxy is {}'.format(ip))
            return ip

    print('代理链接错误')
    time.sleep(10)
    sys.exit()


class OperaChrome(object):
    def __init__(self, path=None, proxy=False):
        self.init_chrome(path, proxy)

    def init_chrome(self, path, proxy):
        options = webdriver.ChromeOptions()
        options.add_argument("disable-infobars")
        options.add_argument("disable-web-security")
        # options.add_argument("--headless")
        options.add_argument("--start-maximized")
        options.add_argument('--log-level=3')
        options.add_argument('--ignore-certificate-errors')
        options.add_experimental_option('excludeSwitches',
                                        ['enable-automation'])
        options.add_argument('blink-settings=imagesEnabled=false')
        # options.add_argument(
        #     'proxy-authorization="sign=BB1799024E00CE5146C16B0B7BC51EA9&orderno=DT20200212142348OUNULt4Q&timestamp=1581490008&change=true"'
        # )
        if proxy:
            options.add_argument('--proxy-server={}'.format(get_proxy()))

        prefs = {"profile.managed_default_content_settings.images": 2}
        prefs = {
            'profile.default_content_setting_values': {
                'images': 2,
            }
        }
        # options.add_experimental_option("prefs", prefs)

        # if proxy:
        #     seleniumwire_options = {
        #         'proxy': {
        #             'http': proxy.get('domain'),
        #             'https': 'dynamic.xiongmaodaili.com:8088',
        #             'no_proxy': 'localhost,127.0.0.1,dev_server:8080',
        #             'custom_authorization': proxy.get('auth')
        #         }
        #     }
        # else:
        #     seleniumwire_options = {}

        driver = webdriver.Chrome(
            executable_path="./backup.exe",
            options=options,
        )
        #   seleniumwire_options=seleniumwire_options)
        if path is not None:
            driver.get(path)

        self.driver = driver

    def judge_driver(self, driver):
        return self.driver if driver is None else driver

    def waiting(self,
                xpath=None,
                css=None,
                classname=None,
                tagname=None,
                driver=None,
                timeout=15):
        driver = self.judge_driver(driver)

        if xpath:
            use = By.XPATH
            sign = xpath
        elif css:
            use = By.CSS_SELECTOR
            sign = css
        elif classname:
            use = By.CLASS_NAME
            sign = classname
        elif tagname:
            use = By.TAG_NAME
            sign = tagname
        while True:

            try:
                WebDriverWait(driver, timeout, 0.1).until(
                    EC.presence_of_element_located((use, sign)))
            except IndexError as exc:
                print("---> {}".format(exc))
                continue
            except StaleElementReferenceException as exc:
                print("---> {}".format(exc))
                continue
            except TimeoutException:
                print('timeout: {}'.format(sign))
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

    def find_by_css(self, css, all_tag=False, driver=None, timeout=15):
        driver = self.judge_driver(driver)

        if self.waiting(css=css, timeout=timeout):
            try:
                if all_tag:
                    obj = driver.find_elements_by_css_selector(css)
                else:
                    obj = driver.find_element_by_css_selector(css)
            except InvalidSelectorException:
                return
            except NoSuchElementException:
                return
            except StaleElementReferenceException:
                return
            else:
                return obj

    def find_by_class(self, classname, all_tag=False, driver=None, timeout=15):
        driver = self.judge_driver(driver)

        if self.waiting(classname=classname, timeout=timeout):
            try:
                if all_tag:
                    obj = driver.find_elements_by_class_name(classname)
                else:
                    obj = driver.find_element_by_class_name(classname)
            except InvalidSelectorException:
                return
            except NoSuchElementException:
                return
            except StaleElementReferenceException:
                return
            else:
                return obj

    def find_by_tag(self, tagname, all_tag=False, driver=None, timeout=15):
        driver = self.judge_driver(driver)

        if self.waiting(tagname=tagname, timeout=timeout):
            try:
                if all_tag:
                    obj = driver.find_elements_by_tag_name(tagname)
                else:
                    obj = driver.find_element_by_tag_name(tagname)
            except InvalidSelectorException:
                return
            except NoSuchElementException:
                return
            except StaleElementReferenceException:
                return
            else:
                return obj


class Amazon(object):
    def __init__(self):
        self.excel = ExcelOpea()
        self.req = Query().run
        self.soup = DealSoup().judge

        super().__init__()

    def good_info(self):
        info = {}
        self.excel.init_sheet(sheet='商品信息')

        info['品牌'] = self.chrome.find_by_css('#bylineInfo').text
        # temp = self.chrome.find_by_css('#averageCustomerReviews')
        info['星级'] = self.chrome.find_by_css('#acrPopover').get_attribute(
            'title')
        info['评价'] = self.chrome.find_by_css('#acrCustomerReviewText').text
        info['价格'] = self.chrome.find_by_css('#priceblock_ourprice').text

        if info:
            for key in info:
                self.excel.write([key, info.get(key)])

        result = re.search(r'"dimensionValuesDisplayData" : (\{.*\})',
                           self.chrome.driver.page_source)

        if result:
            data = json.loads(result.group(1))
            self.excel.write(['变体数量', len(data)])
            for key in data:
                need = [key]
                for value in data.get(key):
                    need.append(value)
                self.excel.write(need)

    def page(self, item):
        self.chrome.driver.execute_script("arguments[0].scrollIntoView(true);",
                                          item)

        button = self.chrome.find_by_css(
            '[class="a-button a-button-image a-carousel-button a-carousel-goto-nextpage"]',
            driver=item)
        if button.get_attribute(
                'aria-disabled'
        ) == 'false' or button.get_attribute('aria-disabled') is None:
            while True:
                reloading = self.chrome.find_by_tag('ol', driver=item)
                if reloading.get_attribute('aria-busy') == "true":
                    time.sleep(1)
                else:
                    try:
                        button.click()
                        return
                    except ElementNotVisibleException:
                        time.sleep(1)
        else:
            return True

    def starts_parser(self, css):
        # 4 stars and aboveq
        href_list = []
        while True:
            item = self.chrome.find_by_css(css)
            starts = self.chrome.find_by_class('a-carousel-row-inner',
                                               driver=item)

            if not starts:
                return

            cards = self.chrome.find_by_class('a-carousel-card',
                                              all_tag=True,
                                              driver=item)
            for card in cards:
                div_obj = self.chrome.find_by_tag('div', driver=card)
                count = 0
                while not div_obj and count < 3 and card.text:
                    time.sleep(2)
                    count += 1
                    div_obj = self.chrome.find_by_tag('div', driver=card)
                    print('waiting')

                if not div_obj:
                    return href_list

                # get asin
                try:
                    asin = div_obj.get_attribute('data-asin')
                except StaleElementReferenceException:
                    asin = div_obj.get_attribute('asin')

                if not asin:
                    continue

                href = 'https://www.amazon.com/dp/{}'.format(asin)
                href_list.append(href)

            if self.page(starts):
                break

        return href_list

    def buy_parser(self):
        buys = self.chrome.find_by_css('#view_to_purchase-sims-feature')
        if not buys:
            return

        buys = self.chrome.find_by_class('a-fixed-left-grid p13n-asin',
                                         driver=buys,
                                         all_tag=True)

        asin_list = [
            buy.get_attribute('data-p13n-asin-metadata').split(
                '&quot;asin&quot;:&quot;')[-1].replace('&quot;}')
            for buy in buys
        ]

        return asin_list

    def similar_parser(self):
        similars = self.chrome.find_by_css('#HLCXComparisonTable')
        if not similars:
            return
        similars = self.chrome.find_by_class('comparison_image_title_cell',
                                             driver=similars,
                                             all_tag=True)

        asin_list = [
            similar.get_attribute('data-asin') for similar in similars
        ]

        return asin_list

    def parser(self):
        self.good_info()

        keywords = {
            'sponsored': '#sp_detail',
            'sponsored2': '#sp_detail2',
            'start': '#sp_detail_thematic',
            'buy': '#view_to_purchase-sims-feature',
            'viewed': '#desktop-dp-sims_session-similarities-sims-feature',
            'similar': '#HLCXComparisonTable',
            # 'bought': '#desktop-dp-sims_session-similarities-sims-feature',
        }
        info = []
        for key in keywords:
            if key == 'buy':
                info = self.buy_parser()
            elif key == 'similar':
                info = self.similar_parser()
            else:
                info = self.starts_parser(keywords[key])

            if info:
                self.excel.init_sheet(sheet=key)
                for content in info:
                    self.excel.write(content)

    def get_asin(self, path: str, param: dict, data: list, tot: int):
        param = urlencode(param)
        init_path = f'https://www.amazon.com{path}?{param}'
        cookies = self.chrome.driver.get_cookies()
        cookie = {x['name']: x['value'] for x in cookies}
        header = {
            'Accept': 'text/html,*/*',
            'User-Agent':
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.100 Safari/537.36',
            'Referer': 'https://www.amazon.com/dp/B073FLCFK2?th=1&psc=1',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'zh-CN,zh;q=0.9',
        }
        count = 10
        offset = 10
        for pg in range(2, int(tot / 10) + 2):
            odata = urlencode({'oData': data})
            timestamps = int(time.time() * 1000)
            path = f'{init_path}&count={count}&offset={offset}&pg={pg}&tot={tot}&num={count}&{odata}&_={timestamps}'

            if self.proxy == 1:
                proxy = get_proxy()
                resp = self.req(path,
                                header=header,
                                proxies={
                                    'http': proxy,
                                    'https': proxy
                                },
                                cookies=cookie)
            else:
                resp = self.req(path, header=header, cookies=cookie)

            if isinstance(resp, int):
                return data

            for item in json.loads(resp)['data']:
                data.append(item['oid'])

            time.sleep(self.sleep_time)
        return data

    def parser_by_re(self):
        self.good_info()

        for sheet_name in ['buy', 'similar']:
            # buy similar
            asin = eval(f'self.{sheet_name}_parser()')
            if asin:
                self.excel.init_sheet(sheet=sheet_name)
                for value in asin:
                    value = value.replace('::', '')
                    self.excel.write(f'https://www.amazon.com/dp/{value}')

        html = self.chrome.driver.page_source

        option_list = []

        for id_tag in ['sp_detail_thematic', 'sp_detail', 'sp_detail2']:
            div_obj = self.soup(html, attr={'id': id_tag})
            if div_obj:
                option_list.append(
                    div_obj.attrs.get('data-a-carousel-options'))

        view_obj = self.soup(
            html,
            attr={'id': 'desktop-dp-sims_session-similarities-sims-feature'})
        if view_obj:
            option_list.append(
                view_obj.findChild('div').get('data-a-carousel-options'))

        for item in option_list:
            data = json.loads(item.replace('&quot;', '"'))
            if data.get('name') == 'desktop-dp-sims_session-similarities':
                # also viewed
                asin = data.get('ajax').get('id_list')
                sheet_name = 'viewed'
            elif '':
                pass
            else:
                # Sponsored
                # Sponsored2
                # 4 stars
                try:
                    asin = self.get_asin(
                        data.get('ajax').get('url'),
                        data.get('ajax').get('params'),
                        data.get('initialSeenAsins'), data.get('set_size'))
                except:
                    continue

                sheet_name = sheet = data.get('ajax').get('params').get(
                    'wName')

            self.excel.init_sheet(sheet=sheet_name)
            for value in asin:
                value = value.replace('::', '')
                self.excel.write(f'https://www.amazon.com/dp/{value}')

    def change_code(self):
        timeout = 15
        self.chrome.click('//*[@id="nav-global-location-slot"]/span/a',
                          timeout=timeout)
        self.chrome.input('//*[@id="GLUXZipUpdateInput"]',
                          keyword='90005',
                          timeout=timeout)
        self.chrome.click('//*[@id="GLUXZipUpdate"]/span/input',
                          timeout=timeout)
        self.chrome.click('/html/body/div[7]/div/div/div[2]/span/span/input',
                          timeout=timeout)

        time.sleep(3)
        self.chrome.waiting('//*[@id="bylineInfo"]', timeout=30)

    def run(self):
        with open('./links.txt', 'r', encoding='utf-8') as fn:
            links = fn.readlines()
        for link in links:
            link = link.replace('\n', '').replace('\t', '')
            if 'http' not in link or not link:
                # Text1.insert('insert', 'Error: 网址错误')
                print('网址错误')
            else:
                if self.proxy == 1:
                    self.chrome = OperaChrome(proxy=1)
                else:
                    self.chrome = OperaChrome()

                self.chrome.driver.get(link)

                if self.code_status == 0:
                    self.change_code()
                    self.code_status = 1
                self.parser_by_re()

    def main(self):
        self.code_status = 0
        try:
            self.proxy = int(input('是否使用代理, 1: 使用, 2: 不使用, 默认不使用: '))
        except:
            print('输入错误, 默认不使用')
            self.proxy = 2
        try:
            self.sleep_time = int(input('根据使用情况设置请求间隔时间, 默认 1 秒: '))
        except:
            print('输入错误, 默认 1 秒')
            self.sleep_time = 1

        self.run()

        self.excel.save()
        self.chrome.driver.quit()


if __name__ == "__main__":
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    spider = Amazon()
    spider.main()
'''
Empty
'''
import re
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException, TimeoutException, InvalidSelectorException
from utils.request import Query
from utils.soup import DealSoup
from utils.excel_opea import ExcelOpea


def remove_charater(content: str):
    return content.replace('\n', '').replace('\t',
                                             '').replace('\r',
                                                         '').replace(' ', '')


class OperaChrome(object):
    def __init__(self, path=None):
        self.init_chrome(path)

    def get_proxy(self):
        req = Query().run
        resp = req(
            path=
            'http://route.xiongmaodaili.com/xiongmao-web/api/glip?secret=3648c286d4be950dfeb744412178bab8&orderNo=GL20191218133200tOpTjxj6&count=1&isTxt=1&proxyType=1'
        )
        return remove_charater(resp)

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

        # options.add_argument('--proxy-server=http://{}'.format(
        #     self.get_proxy()))

        prefs = {"profile.managed_default_content_settings.images": 2}
        options.add_experimental_option("prefs", prefs)
        driver = webdriver.Chrome(executable_path="./backup.exe",
                                  options=options)
        if path is not None:
            driver.get(path)

        self.driver = driver

    def judge_driver(self, driver):
        if driver is None:
            return self.driver
        else:
            return driver

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
        self.excel.init_sheet()
        self.chrome = OperaChrome()
        self.soup = DealSoup()

        super().__init__()

    def good_info(self):
        info = {}

        info['品牌'] = self.chrome.find_by_css('#bylineInfo').text
        # temp = self.chrome.find_by_css('#averageCustomerReviews')
        info['星级'] = self.chrome.find_by_css('#acrPopover').get_attribute(
            'title')
        info['评价'] = self.chrome.find_by_css('#acrCustomerReviewText').text
        info['价格'] = self.chrome.find_by_css('#priceblock_ourprice').text

        result = re.search(r'"dimensionToAsinMap" : (\{.*\})',
                           self.chrome.driver.page_source)
        if result:
            data = result.group(1)
            info['变体数量'] = len(data)
            info['变体'] = data

        if info:
            self.excel.write('商品信息')

            for key in info:
                self.excel.write([key, info.get(key)])

    def page(self, item):
        self.chrome.driver.execute_script("arguments[0].scrollIntoView(true);",
                                          item)

        button = self.chrome.find_by_css(
            '[class="a-button a-button-image a-carousel-button a-carousel-goto-nextpage"]',
            driver=item)
        if button.get_attribute(
                'aria-disabled'
        ) == 'false' or button.get_attribute('aria-disabled') is None:
            button.click()
            time.sleep(self.sleep_time)
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

            cards = self.chrome.find_by_class(
                # '[class="a-section sp_offerVertical p13n-asin sp_ltr_offer"]',
                'a-carousel-card',
                all_tag=True,
                driver=item)
            for card in cards:
                div_obj = self.chrome.find_by_tag('div', driver=card)
                count = 0
                while not div_obj and count < 3 and card.text:
                    time.sleep(self.sleep_time)
                    count += 1
                    div_obj = self.chrome.find_by_tag('div', driver=card)
                    print('waiting')

                if not div_obj:
                    return href_list

                href = div_obj.get_attribute('data-viewpixelurl')
                if href is None:
                    href = self.chrome.find_by_tag(
                        'a', driver=div_obj).get_attribute('href')

                if href in href_list:
                    return href_list
                else:
                    href_list.append('https://www.amazon.com{}'.format(href))

            if self.page(starts):
                break

        return href_list

    def buy_parser(self):
        buys = self.chrome.find_by_css('#view_to_purchase-sims-feature')
        if not buys:
            return
        buys = self.chrome.find_by_css(
            '[class="a-fixed-left-grid-col a-col-right"]',
            driver=buys,
            all_tag=True)

        href_list = []

        for buy in buys:
            pref = self.chrome.find_by_class('a-link-normal', driver=buy)
            if pref:
                pref = pref.get_attribute('data-viewpixelurl')
                href_list.append('https://www.amazon.com{}'.format(pref))

        return href_list

    def similar_parser(self):
        similars = self.chrome.find_by_css('#HLCXComparisonTable')
        if not similars:
            return
        similars = self.chrome.find_by_class('comparison_image_title_cell',
                                             driver=similars,
                                             all_tag=True)

        href_list = []

        for similar in similars:
            pref = self.chrome.find_by_class('a-link-normal', driver=similar)
            if pref:
                pref = pref.get_attribute('href')
                href_list.append('https://www.amazon.com{}'.format(pref))

        return href_list

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
            # try:
            #     if key == 'buy':
            #         info = self.buy_parser()
            #     elif key == 'similar':
            #         info = self.similar_parser()
            #     else:
            #         item = self.chrome.driver.find_element_by_css_selector(
            #             keywords[key])
            #         info = self.starts_parser(item)
            # except Exception as exc:
            #     print('error: {}'.format(exc))

            if info:
                self.excel.write(key)
                for content in info:
                    self.excel.write(content)

    def change_code(self):
        timeout = 15
        self.chrome.click('//*[@id="nav-global-location-slot"]/span/a',
                          timeout=timeout)
        self.chrome.input('//*[@id="GLUXZipUpdateInput"]',
                          keyword='90005',
                          timeout=timeout)
        self.chrome.click('//*[@id="GLUXZipUpdate"]/span/input',
                          timeout=timeout)
        self.chrome.click(
            '//*[@id="a-popover-8"]/div/div[2]/span/span/span/button',
            timeout=timeout)
        # chrome.click('//*[@id="GLUXConfirmClose"]', timeout=timeout)
        self.chrome.click('//*[@id="a-popover-7"]/div/div[2]/span/span',
                          timeout=timeout)

    def main(self):
        code_status = 0
        try:
            self.sleep_time = int(input('根据网络及性能情况输入翻页等待时间, 回车确认，默认 2 秒: '))
        except:
            self.sleep_time = 2
        with open('./links.txt', 'r', encoding='utf-8') as fn:
            links = fn.readlines()
        for link in links:
            link = link.replace('\n', '').replace('\t', '')
            if 'http' not in link or not link:
                print('网址错误')
            else:
                self.chrome.driver.get(link)
                # if code_status == 0:
                #     self.change_code()
                #     code_status = 1
                self.parser()

        self.excel.save()


if __name__ == "__main__":
    spider = Amazon()
    spider.main()
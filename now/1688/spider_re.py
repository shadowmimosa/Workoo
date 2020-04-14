from utils.request import Query
from utils.soup import DealSoup
from config import logger, Cookie
from selenium import webdriver
from urllib.parse import quote
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException, TimeoutException

import json
import time
import csv


def magic_time(during=2):
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
    def waiting(self, xpath, driver=None, timeout=25):
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

    def click(self, xpath, driver=None, timeout=15):
        driver = self.judge_driver(driver)

        if self.waiting(xpath, timeout=timeout):
            driver.find_element_by_xpath(xpath).click()

    def input(self, xpath, driver=None, keyword='', timeout=15):
        driver = self.judge_driver(driver)

        if self.waiting(xpath, timeout=timeout):
            driver.find_element_by_xpath(xpath).send_keys(keyword)


class Deal(object):
    def __init__(self, cookie):
        super().__init__()
        self.cookie = cookie
        self.req = Query().run
        self.soup = DealSoup().judge
        self.header = {
            'accept':
            'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'Sec-Fetch-Dest': 'empty',
            'upgrade-insecure-requests': '1',
            'User-Agent':
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.100 Safari/537.36',
            'Sec-Fetch-Site': 'same-origin',
            'Sec-Fetch-Mode': 'cors',
            'Referer':
            'https://www.alibaba.com/sw.js?v=2.13.12&_flasher_manifest_=https://s.alicdn.com/@g/flasher-manifest/icbu-v2/manifestB.json',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Cookie': self.cookie
        }

    @magic_time()
    def good_detail(self, html):
        try:
            href = 'https:' + self.soup(html, attr='a').get('href')
        except AttributeError:
            logger.info('null')
            return
        header = self.header
        header[
            'Referer'] = 'https://www.alibaba.com/sw.js?v=2.13.12&_flasher_manifest_=https://s.alicdn.com/@g/flasher-manifest/icbu-v2/manifestB.json'
        # header = {
        #     'Host':
        #     'www.alibaba.com',
        #     'accept':
        #     'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        #     'Sec-Fetch-Dest':
        #     'empty',
        #     'upgrade-insecure-requests':
        #     '1',
        #     'User-Agent':
        #     'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.100 Safari/537.36',
        #     'Sec-Fetch-Site':
        #     'same-origin',
        #     'Sec-Fetch-Mode':
        #     'cors',
        #     'Referer':
        #     'https://www.alibaba.com/sw.js?v=2.13.12&_flasher_manifest_=https://s.alicdn.com/@g/flasher-manifest/icbu-v2/manifestB.json',
        #     'Accept-Encoding':
        #     'gzip, deflate, br',
        #     'Accept-Language':
        #     'zh-CN,zh;q=0.9',
        #     'Cookie':
        #     'xman_us_f=x_l=1; umdata_=2FB0BDB3C12E491D48332B803256779B4E7F80795B1EDF77B54383E6922E1EE21CAA9486DD171298CD43AD3E795C914C87A8012FF5A0BA5C75DCEAA78C316677; _samesite_flag_=true; cookie2=16bb16a0f9f8cbf8ef979aa9efbbe9b0; t=6469219d5cc984e58fef4d9d07678f34; _tb_token_=5d5e9e3544de6; ali_apache_id=11.81.187.9.1586769769752.188300.8; XSRF-TOKEN=0d1463fc-b1d5-4d0e-8b2f-ef74fda25f16; acs_usuc_t=acs_rt=949c836cc6d04c6293f94fe8990accb1; cna=VYrvFuCa23gCAXqPyNo34007; xman_t=s/wZCnrucntu1QsQzLJ+EsZuwZOR1Edol+pKl8pSgXzmiVW0y0usR5fQSl7HE1BjdP/OYpBn72oYhznEyUYgjexwNoP9SVnm; atm-whl=-1%260%260%260; atm-x=__ll%3D-1; v=0; _csrf_token=1586771823152; sc_g_cfg_f=sc_b_locale=en_US; gangesweb-buckettest=122.143.200.218.1586771826362.4; _bl_uid=18kgj8dpy20apFzkk65et4U73v0w; xman_f=/4nKqoRx1OMVabfBxseMc6h/e66pmyzrwsOD/dHSayx8HDXcceP4x+Fwh8ku2Sb1XQIGvWL4nFYHzhVCwzI95SedcW+lxn7IvZmll3fRlSL0KfhUq+cvSw==; JSESSIONID=9FE13AAFCF8C07483103DDCB0CB2A193; ali_apache_track=""; ali_apache_tracktmp=""; l=eBrr37CeQpr4_acsBOfMd4mjgrQ9sIRAIukoGqHHiT5P_PsB58SOWZX-Lpp6CnhVh6LB-3JaCe1pBeYBqGAPaqKXRrbMgIDmn; isg=BPDwDx_mWmcsXAZjtVqiJPIzwb5COdSDUZ7y7OpBvcsepZBPkEsfEhnf-K3FFYxb'

        # }
        html = self.req(path=href, header=header)
        # html = self.req(path='https:' + html, header=header)

        temp = self.soup(html, attr={'data-aui': 'supplier-card'})

        self.info['供应商名称'] = self.soup(temp,
                                       attr={
                                           'class':
                                           'company-name company-name-lite-vb'
                                       }).text
        self.info['金牌会员年数'] = self.soup(temp, attr={'class': 'join-year'}).text

        levels_temp = self.soup(self.soup(temp, attr={'class': 'no-line'}),
                                'i',
                                all_tag=True)
        level_count = 0
        for level in levels_temp:
            if 'ui2-icon-svg-diamond-level-one' in level.attrs['class']:
                level_count += 1
            elif 'ui2-icon-svg-diamond-level-half' in level.attrs['class']:
                level_count += 0.5

        self.info['交易等级'] = level_count

        trans = self.soup(temp, attr={'id': 'transactionAmountTrigger'})
        if not trans:
            self.info['交易量'] = None
        else:
            self.info['交易量'] = self.soup(trans, 'b', all_tag=True)[1].text

        reponse_temp = self.soup(temp,
                                 attr={'class': 'performance-value-wrap'})
        if not reponse_temp:
            self.info['回复率'] = None
        else:
            self.info['回复率'] = reponse_temp.b.text

        score_temp = self.soup(temp, attr={'class': 'score-lite'})
        if not score_temp:
            self.info['供应商评论等级'] = None
        else:
            self.info['供应商评论等级'] = score_temp.b.text

        self.info['产品名称'] = self.soup(html, attr={'class': 'ma-title'}).text

        price_temp = self.soup(html, attr={'class': 'priceVal'})
        if not price_temp:
            price_temp = self.soup(html, attr={'class': 'ma-spec-price'})
            if not price_temp:
                self.info['产品价格'] = self.soup(html,
                                              attr={
                                                  'class': 'ma-ref-price'
                                              }).text
            else:
                self.info['产品价格'] = price_temp.get('title')
        else:
            self.info['产品价格'] = price_temp.get('title')

        self.info['产品价格'] = self.info['产品价格'].split(' - ')[-1]

        auid = href.split('_')[-1].split('.')[0]

        # self.info['及时交付率'] = self.soup(html,
        #                                attr={
        #                                    'data-role': 'onTimeShippmentVal'
        #                                }).text

        resp = self.req(
            path=
            f'https://www.alibaba.com/event/app/companyCardIntegrated/getSupplierData.htm?detailId={auid}',
            header=header)
        data = json.loads(resp)
        self.info['及时交付率'] = data.get('result').get(
            'supplierOnTimeDeliveryRate')

        self.info['产品网页链接'] = href

        href_temp = self.soup(html, attr={'class': 'transaction-info-lite'})
        if not href_temp:
            self.info['供应商评论量'] = None
            return
        else:
            href = href_temp.a.get('href')

        self.header['Referer'] = href
        self.shop_detail(href)

    @magic_time()
    def shop_detail(self, path):
        # self.header['Host'] = path.replace('https://', '').split('/')[0]
        chrome.driver.get(path)
        chrome.waiting('star-review-count')
        review = chrome.driver.find_element_by_class_name('star-review-count')
        self.info['供应商评论量'] = review.text.split(' ')[0]

    def main(self):
        category = ['disposable_mask']
        with open('./data/already.txt', 'r', encoding='utf-8') as fn:
            already = fn.read().split('\n')

        error_count = 0
        for keyword in category:
            count, page = (0, 1) if keyword != '车载充电器' else (56, 3)
            # keyword = quote(str(keyword).encode('gbk'))
            while count < 4000:
                # self.header['Host'] = 's.1688.com'

                if page == 1:
                    # self.header['Referer'] = 'https://auto.1688.com/'
                    path = f'https://www.alibaba.com/trade/search?keyword={keyword}&indexArea=company_en&f1=y&viewType=L&n=50'
                    resp = self.req(path, header=self.header)
                else:
                    path = f'https://www.alibaba.com/trade/search?page={page}&indexArea=company_en&keyword={keyword}&viewType=L&n=50&f1=y'
                    resp = self.req(path, header=self.header, data=True)

                time.sleep(1)
                goods = self.soup(resp,
                                  attr={'class': 'f-icon m-item'},
                                  all_tag=True)

                for good in goods:
                    title = self.soup(good, attr={
                        'class': 'title ellipsis'
                    }).text
                    if title in already:
                        logger.info('alrady have')
                        continue
                    else:
                        already.append(title)

                    self.info = {}
                    self.header['Referer'] = path
                    # self.header['Host'] = 'detail.1688.com'
                    self.good_detail(self.soup(good, attr={'class':
                                                           'product'}))
                    # try:
                    #     self.good_detail(
                    #         self.soup(good, attr={'class': 'product'}))
                    # except Exception as exc:
                    #     logger.error('Error: {}\n path is {}'.format(
                    #         exc, path))
                    #     error_count += 1
                    #     if error_count > 15:
                    #         print(time.time(), keyword, count)
                    #         return
                    #     else:
                    #         continue

                    write(self.info)
                    count += 1
                page += 1


def remove_charater(content: str):
    if not isinstance(content, str):
        return content

    return content.replace('\n',
                           '').replace('\t',
                                       '').replace('\r',
                                                   '').replace('\xa0',
                                                               '').strip(' ')


def write(content=None):
    title_list = [
        '供应商名称', '金牌会员年数', '交易等级', '交易量', '回复率', '供应商评论等级', '产品名称', '产品价格',
        '及时交付率', '产品网页链接', '供应商评论量'
    ]
    if content is None:
        need = title_list
    elif len(content) == 0:
        return
    else:
        need = [content[key] for key in title_list]

    need = [remove_charater(value) for value in need]

    with open('./data/data.csv', 'a', encoding='utf-8') as fn:
        writer = csv.writer(fn)
        # csv.DictWriter()
        writer.writerow(need)

    with open('./data/already.txt', 'a', encoding='utf-8') as fn:
        fn.write(need[0])
        fn.write('\n')


chrome = OperaChrome()
if __name__ == "__main__":
    # write()
    Deal(Cookie).main()

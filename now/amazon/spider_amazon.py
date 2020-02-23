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
import tkinter as tk
from tkinter import ttk
from tkinter.scrolledtext import ScrolledText
import threading
from icon import img
import io

IP = ''
PROXY = ''


def remove_charater(content: str):
    return content.replace('\n', '').replace('\t',
                                             '').replace('\r',
                                                         '').replace(' ', '')


def check_ip():
    if not IP:
        return

    try:
        requests.adapters.DEFAULT_RETRIES = 3
        if 'http' not in IP:
            proxy = "http://" + IP

        ip = "".join(IP.split(":")[0:1])
        resp = requests.get(url="http://icanhazip.com/",
                            timeout=8,
                            proxies={"http": proxy})
        real_ip = resp.text
        if (ip == real_ip):
            output('Info: 代理有效')
            return True
        else:
            output('Info: 代理无效')
    except:
        output('Info: 代理无效')


def get_proxy():
    global IP

    if not PROXY:
        return
    if check_ip():
        return IP
    retry = 5
    while retry:
        resp = requests.get(PROXY)
        ip = remove_charater(resp.text)

        if 'code' not in ip:
            output('Info: 代理地址 - {}'.format(ip))
            if check_ip:
                IP = ip
                return ip
            else:
                retry -= 1
        else:
            output('Error: 获取代理失败 - {}'.format(ip))

    sys.exit()


class OperaChrome(object):
    def __init__(self, path=None, proxy=False):
        self.init_chrome(path, proxy)

    def init_chrome(self, path, proxy):
        options = webdriver.ChromeOptions()
        options.add_argument("disable-infobars")
        options.add_argument("disable-web-security")
        options.add_argument("--headless")
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
        service = webdriver.chrome.service
        webdriver.Chrome.service.command_line_args
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
        self.header = {
            'Accept': 'text/html,*/*',
            'User-Agent':
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.100 Safari/537.36',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'zh-CN,zh;q=0.9',
        }
        super().__init__()

    def good_info(self):
        info = {}
        self.excel.init_sheet(sheet='商品信息')

        # info['品牌'] = self.chrome.find_by_css('#bylineInfo').text
        # info['星级'] = self.chrome.find_by_css('#acrPopover').get_attribute(
        #     'title')
        # info['评价'] = self.chrome.find_by_css('#acrCustomerReviewText').text
        # info['价格'] = self.chrome.find_by_css('#priceblock_ourprice').text
        info['品牌'] = self.soup(self.html, attr={'id': 'bylineInfo'}).text
        info['星级'] = self.soup(self.html, attr={
            'id': 'acrPopover'
        }).get('title')
        info['评价'] = self.soup(self.html, attr={
            'id': 'acrCustomerReviewText'
        }).text
        info['价格'] = self.soup(self.html, attr={
            'id': 'priceblock_ourprice'
        }).text
        if info:
            for key in info:
                self.excel.write([key, info.get(key)])
                output('Info: {} - {}'.format(key, info.get(key)))

        # result = re.search(r'"dimensionValuesDisplayData" : (\{.*\})',
        #                    self.chrome.driver.page_source)
        result = re.search(r'"dimensionValuesDisplayData" : (\{.*\})',
                           self.html)
        if result:
            data = json.loads(result.group(1))
            self.excel.write(['变体数量', len(data)])
            for key in data:
                need = [key]
                for value in data.get(key):
                    need.append(value)
                self.excel.write(need)
                output('Info: {}'.format(need))

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
        # buys = self.chrome.find_by_css('#view_to_purchase-sims-feature')
        buys = self.soup(self.html,
                         attr={'id': 'view_to_purchase-sims-feature'})
        if not buys:
            return

        buys = self.soup(buys,
                         attr={'class': 'a-fixed-left-grid p13n-asin'},
                         all_tag=True)

        # asin_list = [
        #     buy.get_attribute('data-p13n-asin-metadata').split(
        #         '&quot;asin&quot;:&quot;')[-1].replace('&quot;}')
        #     for buy in buys
        # ]
        asin_list = [buy.get('data-p13n-asin-metadata') for buy in buys]

        return asin_list

    def similar_parser(self):
        similars = self.soup(self.html, attr={'id': 'HLCXComparisonTable'})
        if not similars:
            return

        similars = self.soup(similars,
                             attr={'class': 'comparison_image_title_cell'},
                             all_tag=True)

        asin_list = [similar.get('data-asin') for similar in similars]

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
                                cookies=self.cookie)
            else:
                resp = self.req(path, header=header, cookies=self.cookie)

            if isinstance(resp, int):
                if 400 <= resp <= 403:
                    output('Waring: Cookie 失效')
                return data

            for item in json.loads(resp)['data']:
                data.append(item['oid'])

            time.sleep(self.sleep_time)
        return data

    def parser_by_re(self):
        if self.proxy == 1:
            proxy = get_proxy()
            resp = self.req(self.link,
                            header=self.header,
                            proxies={
                                'http': proxy,
                                'https': proxy
                            },
                            cookies=self.cookie)
        else:
            resp = self.req(self.link, header=self.header, cookies=self.cookie)
        if isinstance(resp, int):
            if 400 <= resp <= 403:
                output('Waring: Cookie 失效')
                return
            elif 500 <= resp <= 505:
                output('Error: 服务器错误, 请重新获取 cookie 或使用代理')
                return
        self.html = resp

        self.good_info()

        for sheet_name in ['buy', 'similar']:
            # buy similar
            asin = eval(f'self.{sheet_name}_parser()')
            if asin:
                self.excel.init_sheet(sheet=sheet_name)
                for value in asin:
                    value = value.replace('::', '')
                    self.excel.write(f'https://www.amazon.com/dp/{value}')
                    output(f'Info: 已抓取 - https://www.amazon.com/dp/{value}')

        # html = self.chrome.driver.page_source

        option_list = []

        for id_tag in ['sp_detail_thematic', 'sp_detail', 'sp_detail2']:
            div_obj = self.soup(self.html, attr={'id': id_tag})
            if div_obj:
                option_list.append(
                    div_obj.attrs.get('data-a-carousel-options'))

        view_obj = self.soup(
            self.html,
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
                output(f'Info: 已抓取 - https://www.amazon.com/dp/{value}')

    def change_code(self):
        timeout = 15
        output('Info: 切换地区 90005')
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

    def check_links(self):
        with open('./links.txt', 'r', encoding='utf-8') as fn:
            links = fn.readlines()
        self.real_link = []
        for link in links:
            link = link.replace('\n', '').replace('\t', '')
            if 'http' not in link or not link:
                Text1.insert('insert', 'Error: 网址错误, 请检查 {}'.format(link))
                Text1.see(tk.END)
            else:
                self.real_link.append(link)

    def get_cookie(self):
        link = self.real_link[0]
        output('Info: 获取 cookie 中...')
        if self.mode == 1:
            if self.proxy == 1:
                self.chrome = OperaChrome(proxy=1)
            else:
                self.chrome = OperaChrome()

            self.chrome.driver.get(link)

            self.change_code()
            self.code_status = 1

            cookies = self.chrome.driver.get_cookies()
            self.cookie = {x['name']: x['value'] for x in cookies}
            self.chrome.driver.quit()

        elif self.mode == 2:
            with open('./cookie.txt', 'r', encoding='utf-8') as fn:
                text = fn.read()
            cookie1 = re.search('cookie1=(\[[\s\S]*\])', text)
            cookie2 = re.search('cookie2="(.*)"', text)
            if cookie1 and cookie2:
                output('Warning: 仅支持保留一个 cookie 请检查')
                raise ReferenceError
            elif cookie1:
                try:
                    cookies = json.loads(cookie1.group(1))
                except AttributeError:
                    output('Waring: 请检查 cookies 文件')
                    raise ReferenceError
                self.cookie = {x['name']: x['value'] for x in cookies}
            elif cookie2:
                cookies = cookie2.group(1).replace(' ', '')
                self.cookie = {
                    x.split('=')[0]: x.split('=')[1]
                    for x in cookies.split(';')
                }
            else:
                output('Error: cookie 文件错误, 请检查')
                raise ReferenceError

                # os._exit(0)

            # print(self.cookie)

        output('Info: Cookie 获取成功')

    def run(self, mode):
        global PROXY
        self.mode = mode
        self.check_links()
        if self.proxy == 1:
            with open('./proxy.txt', 'r', encoding='utf-8') as fn:
                PROXY = remove_charater(fn.readline())
        self.get_cookie()
        output('Info: 采集开始')
        for link in self.real_link:
            self.link = link
            self.parser_by_re()
            try:
                self.parser_by_re()
            except Exception as exc:
                output('Error: {}'.format(exc))
                output('Info: Excel 已保存')
            else:
                self.excel.save()
                output('Info: 采集成功, Excel 已保存')

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

            with open('./links.txt', 'r', encoding='utf-8') as fn:
                links = fn.readlines()
            for link in links:
                link = link.replace('\n', '').replace('\t', '')
                if 'http' not in link or not link:
                    Text1.insert('insert', 'Error: 网址错误')
                    Text1.see(tk.END)
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

        self.excel.save()


def make_it():
    mode = var1.get()
    proxy = var2.get()
    interval = var3.get()

    spider.proxy = proxy
    spider.sleep_time = interval

    if mode == 0:
        Text1.insert('insert', 'Error: 请选择 Cookie 获取方式\n')
        Text1.see(tk.END)
    elif mode in [1, 2]:
        spider.run(mode)


def output(message):
    print(message)
    Text1.insert('insert', f'{message}\n')
    Text1.see(tk.END)


def fun():
    th = threading.Thread(target=make_it, args=())
    if 'spider' in [x.name for x in threading.enumerate()]:
        Text1.insert('insert', 'Warning: 已在运行, 请勿重复点击\n')
        Text1.see(tk.END)
        return

    th.setDaemon(True)
    th.setName('spider')
    th.start()


if __name__ == "__main__":
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    spider = Amazon()

    windows = tk.Tk()
    windows.geometry('600x325')
    windows.resizable(0, 0)

    windows.title('Amazon 采集')

    tmp = open("tmp.ico", "wb+")
    tmp.write(img)
    tmp.close()
    windows.iconbitmap("tmp.ico")
    os.remove("tmp.ico")

    var1 = tk.IntVar()
    var1.set(0)
    var2 = tk.IntVar()
    var2.set(0)

    r1 = tk.Radiobutton(windows, text='自动获取 Cookies', variable=var1, value=1)

    r1.place(height=20, width=120, x=15, y=15)
    # r1.grid(row=0, column=0, padx=5, pady=5)
    r2 = tk.Radiobutton(windows, text='手动导入 Cookie', variable=var1, value=2)
    r2.place(height=20, width=120, x=150, y=15)
    # r2.grid(row=0, column=1, padx=5, pady=5)

    r3 = tk.Radiobutton(windows, text='使用代理', variable=var2, value=1)
    r3.place(height=20, width=120, x=285, y=15)
    # r3.grid(row=0, column=2, padx=5, pady=5)

    Label1 = tk.Label(windows, text='请求间隔(秒): ')
    # Label1.grid(row=1, column=0, padx=30, pady=5, sticky='W')
    Label1.place(height=20, width=120, x=15, y=50)

    var3 = tk.IntVar()
    c1 = ttk.Combobox(textvariable=var3)
    c1['values'] = (1, 2, 3, 4, 5, 6, 7, 8, 9)
    # numberChosen.grid(column=1, row=1)
    c1.current(0)
    c1.place(height=20, width=120, x=150, y=50)
    # c1.grid(row=1, column=1, padx=0, pady=0, sticky='W')

    Button1 = tk.Button(windows, text='采集', command=fun)
    Button1.place(height=40, width=90, x=420, y=25)
    # Button1.grid(row=1, column=2, padx=10, pady=10)  # , rowspan=2, columnspan=2

    # Text1 = tk.Text(windows)
    Text1 = ScrolledText(windows)
    Text1.insert('insert', '初始化程序...\n')
    Text1.see(tk.END)
    Text1.place(height=120, width=570, x=15, y=90)
    # Text1.grid(row=3, column=1)

    Label1 = tk.Label(
        windows,
        justify='left',
        text=
        '采集程序使用说明: \n采集链接放在程序目录下 links.txt 中, 每行放一个链接; 使用熊猫代理, 链接放在程序目录下 proxy.txt 中\n'
    )
    Label1.place(height=60, width=570, x=15, y=225)

    Label2 = tk.Label(
        windows,
        justify='left',
        text=
        '选项一: 后台静默打开网页切换地区获取 Cookie, 影响因素较多, 可能会出错\n选项二: 手动导入 Cookie, Cookie 会失效(导入方法参考 cookie_example.txt 中注释)'
    )
    Label2.place(height=60, width=470, x=20, y=260)

    windows.mainloop()

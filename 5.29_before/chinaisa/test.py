import xlwt
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

options = webdriver.ChromeOptions()
options.add_argument('--ignore-certificate-errors')
browser = webdriver.Chrome(chrome_options=options)
link_path = '//*[@id="0000000000010086"]/table[1]/tbody/tr/td/div/a[@href]'
url = 'http://www.chinaisa.org.cn/gxportal/DispatchAction.do?efFormEname=ECTM40&key=VjVbZAxnAGEFZA45AmVQMVA0UDMDZ1BnUmEJPFg6BDMEF1oVARoCMFFAUBcFElY2###'
browser.get(url)
titlename = './{}.xls'  #文件名称

for y in range(3):
    WebDriverWait(browser, 15, 0.5).until(
        EC.presence_of_element_located((By.XPATH, link_path)))
    element = browser.find_elements_by_xpath(link_path)
    browser.find_element_by_id
    length = len(element)
    for i in range(0, length):
        try:
            link = element[i]
            url = link.get_attribute('href')
            option = "window.open('{}')".format(url)
            browser.execute_script(option)
            windows = browser.window_handles
            browser.switch_to_window(windows[1])
            WebDriverWait(browser, 15, 0.5).until(
                EC.frame_to_be_available_and_switch_to_it("mframe"))
            WebDriverWait(browser, 15, 0.5).until(
                EC.frame_to_be_available_and_switch_to_it("frSheet"))
            html = browser.page_source

            wbk = xlwt.Workbook()
            sheet = wbk.add_sheet('test01')

            soup = BeautifulSoup(html, 'lxml')
            soup = soup.findAll('tr')
            for x, tr in enumerate(soup):
                soup_td = tr.findAll('td')
                for j, td in enumerate(soup_td):
                    if x == 0:
                        filename = titlename.format(td.text)
                    sheet.write(x, j, td.text)
            wbk.save(filename)

            browser.close()
            browser.switch_to_window(windows[0])
        except Exception as exc:
            print(exc)
            continue

    browser.find_element_by_link_text('下页').click()

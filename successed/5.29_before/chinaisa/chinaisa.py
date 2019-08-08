import xlwt
from selenium import webdriver
from bs4 import BeautifulSoup


class GetInfo(object):
    def __init__(self):
        self.list_url = "http://www.chinaisa.org.cn/gxportal/DispatchAction.do?efFormEname=ECTM40&key=VjVbZAxnAGEFZA45AmVQMVA0UDMDZ1BnUmEJPFg6BDMEF1oVARoCMFFAUBcFElY2"
        self.filename = "./data/{}.xls"

    def excel_opera(self, i, j, value):
        wbk = xlwt.Workbook()
        sheet = wbk.add_sheet('sheet 1')
        sheet.write(i, j, value)
        wbk.save(self.filename)

    def one_page(self, url):
        browser = webdriver.Chrome()
        browser.get(url)
        browser.implicitly_wait(15)
        browser.switch_to_frame('mframe')
        browser.switch_to_frame('frSheet')
        html = browser.page_source
        browser.close()

        soup = BeautifulSoup(html, 'lxml')
        soup = soup.findAll('tr')

        wbk = xlwt.Workbook()
        sheet = wbk.add_sheet('sheet 1')

        for i, tr in enumerate(soup):
            soup_td = tr.findAll('td')
            for j, td in enumerate(soup_td):
                if i == 0:
                    filename = self.filename.format(td.text)
                sheet.write(i, j, td.text)

        wbk.save(filename)

    def page_list(self):
        browser = webdriver.Chrome()
        browser.get(self.list_url)
        browser.implicitly_wait(15)
        html = browser.page_source

        soup = BeautifulSoup(html, 'lxml')
        soup = soup.findAll('table')
        table_list = soup[10]
        table_page = soup[12]
        self.one_page(
            "http://www.chinaisa.org.cn/gxportal/DispatchAction.do?efFormEname=ECTM40&key=VDdeYQhjWDkDYg45UzQBYFE1AWEAZAEyUmMJMAJiATFXRAxDW0ADMwQVAEcEE1U3"
        )
        pass

    def run(self):
        self.page_list()


def main():
    import os
    os.chdir(os.path.dirname(os.path.abspath(__file__)))

    run = GetInfo()
    run.run()


if __name__ == "__main__":
    main()
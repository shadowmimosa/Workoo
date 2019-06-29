import os
import xlwt
from bs4 import BeautifulSoup, Tag


class HtmlToExcel(object):
    def __init__(self):
        self.wkb = xlwt.Workbook()
        self.sheet = self.wkb.add_sheet("sheet1")
        self.row = 0

    def deal_excel(self, content):
        if isinstance(content, list):
            for i, j in enumerate(content):
                self.sheet.write(self.row, i, j)
        elif isinstance(content, str):
            self.sheet.write(self.row, 0, content)

        self.row += 1

    def deal_chapter(self):
        for div in self.content.find_all("div"):
            self.deal_excel(div.text)
            pass

    def deal_block(self):
        self.deal_excel(self.content.find("div").text.replace("\n", "").replace(" ", ""))
        pass

    def deal_h4(self):
        info_ = []
        info_.append(self.content.find("a").text)
        info_.append(self.content.find("span").text)
        self.deal_excel(info_)

    def deal_con(self):
        sign = self.content.get("style")
        if sign == None:
            info_ = []
            info_.append(self.content.find("a").text)
            info_.append(self.content.find("span").text)
            self.deal_excel(info_)
        elif sign == "display: none":
            return

    def main(self):
        for index in range(0,23):
            soup = BeautifulSoup(open("./nhsa_raw_html/index_{}.html.htm".format(index), encoding="utf-8"), "lxml")
            for child in soup.find("div", attrs={"id": "classicont"}).children:
                a = type(child)
                if isinstance(child, Tag):
                    classname = child.get("class")[0]
                    self.content = child
                    if classname == "Chapter":
                        self.deal_chapter()
                    elif classname == "Block":
                        self.deal_block()
                    elif classname == "els-doc-h4":
                        self.deal_h4()
                    elif classname == "els-doc-con":
                        self.deal_con()

        self.wkb.save("./data.xlsx")

    # for child in soup.find("div", attrs={"id": "classicont"}).descendants:


if __name__ == "__main__":
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    HtmlToExcel().main()
"""
    作者：上海信访
    创建时间2020/1/27上午8:54
    开发IDE：PyCharm
    描述：http://xfb.sh.gov.cn/xfb/n62/n69/index.html
    数据爬取保存csv
"""
from bs4 import BeautifulSoup
# from xlutils.copy import copy
import requests
import re
import time
import csv
import codecs
headers = {
    "User-Agent":
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.117 Safari/537.36"
}


def main(url_page):
    response = requests.get(url_page, headers=headers)
    html = response.text
    soup = BeautifulSoup(html, 'lxml')
    data = soup.select('#main > div > div > ul > li > span > a')

    for url in data:
        # result = re.match(r'^window.open\(".*"\)$', url)
        # print(result.group())

        result = re.match('^window.open\("(.*)"\)$', url["onclick"])
        print(result.group(1))
        result_letterID = re.search('LetterID=(\w+)', result.group(1), re.S)
        letterID = result_letterID.group(1)
        print(letterID)
        response_html(letterID)

    # time.sleep(10)


def response_html(letterID):
    html = "http://wsxf.sh.gov.cn/xf_swldxx/areaSearch/hfxd_info.aspx?State=C4AD4221A364E620&LetterID={}".format(
        letterID)
    print(html)
    response = requests.get(html, headers=headers)
    # print(response.text)
    soup = BeautifulSoup(response.text, 'lxml')
    data_1 = soup.select("#LaTitle")[0].text  # 信件标题
    data_2 = soup.select("#LaDate")[0].text  # 来信日期
    data_3 = soup.select("#LaContent")[0].text  # 信件内容
    data_4 = soup.select("#LaHFDate")[0].text  # 回复日期
    data_5 = soup.select("#LaDeptment")[0].text  # 回复单位
    data_6 = soup.select("#LaDisposition")[0].text  # 处理情况

    rows = [
        [html, data_1, data_2, data_3, data_4, data_5, data_6],
    ]
    print(html, data_1, data_2, data_3, data_4, data_5, data_6)

    with codecs.open('data.csv', 'a', encoding='utf-8-sig') as f:
        f_csv = csv.writer(f, lineterminator='\n')
        # f_csv.writerow(header)
        f_csv.writerows(rows)


if __name__ == '__main__':
    header = ['URL', '信件标题', '来信日期', '信件内容', '回复日期', '回复单位', '处理情况']

    with codecs.open('data.csv', 'a', encoding='utf-8-sig') as f:
        f_csv = csv.writer(f, lineterminator='\n')
        f_csv.writerow(header)
    # url_page = "http://wsxf.sh.gov.cn/xf_sw2ldxx/areaSearch/hfxdAll.aspx?nav=&pageindex=1&pagesize=20"
    url_pages = []
    for i in range(1, 91):
        url_pages.append(
            "http://wsxf.sh.gov.cn/xf_swldxx/areaSearch/hfxdAll.aspx?nav=&pageindex={}&pagesize=20"
            .format(i))
    for url_page in url_pages:
        # print(url_page)
        main(url_page)
    # response_html("4386595EA9C14D65")

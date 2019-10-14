from multiprocessing import Lock
import requests as req
from lxml import etree
import threading
import pymysql
import time
import bs4
import re
import os

spider_delay = 60*5

#数据库
# if(os.path.exists('gzggzyjy.db')):
#     os.remove('gzggzyjy.db')
# db = sqlite3.connect('gzggzyjy.db')
# cursor = db.cursor()
# cursor.execute('''CREATE TABLE gdggzyjyxx(
#     id INTEGER PRIMARY KEY AUTOINCREMENT  NOT NULL,
#     entry_name TEXT NOT NULL,
#     entry_number INT NOT NULL,
#     entry_type TEXT NOT NULL,
#     entry_budget INT NOT NULL,
#     quotation_time_start TEXT,
#     quotation_time_end TEXT,
#     purchaser TEXT,
#     url TEXT NOT NULL
# );''')
# db.commit()

def plog(*args):
    ctime = time.strftime('[ %m-%d %H:%M:%S ] ')
    file = open('gdgg.log','a')
    file.write(ctime)
    print(ctime,end='')
    for i in args:
        file.write(str(i))
        print(i,end='')
    print('')
    file.write('\n')
    file.close()

def FuckSQL(s):
    r = s.replace('\\','\\\\').replace("'","\\'").replace('"','\\"')
    r = r.replace('\b','\\b').replace('\r','\\r').replace('\n','\\n')
    r = r.replace('\t','\\t').replace('%','\\%').replace('_','\\_')
    return r
#爬虫本体
def spyon(db):
    host_url = 'http://mall.gzggzy.cn/bid/noticeList?type=01&pageNo=' #主页面地址（缺陷）
    r = req.get(host_url) #获取主页面地址
    page_count = int(re.search(r'(?<=共)\d+(?=页)',r.text).group()) #获取页数
    for i in range(page_count): #在每一页循环
        r = req.get(host_url + str(i)) #主页面地址（完整）
        soup = bs4.BeautifulSoup(r.text,'html5lib') #调用美味汤来以html形式打开主页面
        try:
            tbody = soup.select('tbody')[0] #找到tbody
        except Exception as ex:
            file = open('error.html','wb')
            file.write(r.content)
            file.close()
            raise ex
        data_collection = tbody.select('tr') #在tbody中收集tr数据
        for data_item in data_collection: #在tr中一条一条循环
            bid_inv_number =data_item.select('.col-xs-1')[0].text #获取项目编号
            title_link = data_item.select('td > a')[0] #获取项目详情页链接
            bid_tittle = title_link.get('title') #获取项目名称
            bid_url = title_link.get('href') #项目详情页链接地址
            r_in = req.get('http://mall.gzggzy.cn' + bid_url) #获取项目详情页链接地址
            soup_in = bs4.BeautifulSoup(r_in.text,'html5lib') #调用美味汤来以html形式打开详情页
            content_all = soup_in.select('tr > td') #找到tr中td

            entry_name = '' #项目名称
            entry_number = '' #项目编号
            entry_type = '' #项目类别
            entry_budget = '' #项目报价
            entry_content = '' #项目采购内容
            quotation_time_start = '' #报价开始时间
            quotation_time_end = '' #报价结束时间
            purchaser = '' #采购人名称
            url = 'http://mall.gzggzy.cn' + bid_url

            for content in content_all: #在td中一条一条循环
                text = content.text #以text形式循环
                m = re.findall(r'\d{4}年\d{2}月\d{2}日\s*\d{2}:\d{2}:\d{2}',text) #找到报价时间
                if(text.startswith('（一）项目名称：')): #找到项目名称
                    entry_name = text[8:]
                elif(text.startswith('（二）项目编号：')):
                    entry_number = text[8:]
                elif(text.startswith('（三）项目类别：')):
                    entry_type = text[8:]
                elif(text.startswith('（四）采购预算（最高限价）：')):
                    entry_budget_all = text[14:]
                    entry_budget = re.search(r'([\d|,|.]+)+',entry_budget_all).group()
                elif(text.startswith('（五）采购内容：')):
                    entry_content = text[8:]
                elif(m): #找到报价时间
                    quotation_time_start = m[0].replace('年','-').replace('月','-').replace('日','').replace('  ',' ')
                    quotation_time_end = m[1].replace('年','-').replace('月','-').replace('日','').replace('  ',' ')
                elif(text.startswith('名称：')):
                    purchaser = text[3:]
                    break #跳出当前循环        

            entry_name = FuckSQL(entry_name)
            entry_number = FuckSQL(entry_number)
            entry_type = FuckSQL(entry_type)
            entry_budget = FuckSQL(entry_budget)
            entry_content = FuckSQL(entry_content)
            quotation_time_start = FuckSQL(quotation_time_start)
            quotation_time_end = FuckSQL(quotation_time_end)
            purchaser = FuckSQL(purchaser)
            url = FuckSQL(url)
            html_data = FuckSQL(r_in.text)

            cursor = db.cursor()
            cmd = '''select count(*) from tb_bid where inviter_number ='{}';'''.format(entry_number)
            r = cursor.execute(cmd)
            r = cursor.fetchone()[0]
            if  r != 0:
                plog(entry_name,'已存在，跳过')
                return
            cursor.close()
            cmd = ''' INSERT INTO tb_bid(platform_id,title,inviter_number,type,budget_money,announce_time,end_time,company,url,html,sysdata) 
            VALUES(2,'{}','{}','{}','{}','{}','{}','{}','{}','{}',0);'''.format(entry_name,entry_number,entry_type,entry_budget,quotation_time_start,quotation_time_end,purchaser,url,html_data)
            cursor = db.cursor()
            cursor.execute(cmd)
            cursor.close()
            db.commit()


if __name__ == "__main__":
    plog('监控系统启动完成')
    while True:
        # main loop
        try:
            db = pymysql.connect('212.64.5.21','dev','dev','bidpython',charset='utf8')
            spyon(db)
            plog('爬取进程成功完成')
        except Exception as ex:
            plog('抓取数据时出现异常:',ex)
            db.rollback()
        finally:
            db.commit()
            db.close()
            time.sleep(spider_delay)


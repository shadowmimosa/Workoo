from multiprocessing import Lock
import requests as req
from lxml import etree
import threading
import pymysql
import json
import time
import bs4
import re
import os

def plog(*args):
    ctime = time.strftime('[ %m-%d %H:%M:%S ] ')
    file = open('gdls.log','a')
    file.write(ctime)
    print(ctime,end='')
    for i in args:
        file.write(str(i))
        print(i,end='')
    print('')
    file.write('\n')
    file.close()

bid_list = 'http://www.gdedulscg.cn/home/bill/billlist?page='
spider_delay = 60 * 5
def Trim(s):
    r = re.sub(r'^\s+','',s)
    r = re.sub(r'\s+$','',r)
    return r
def FuckSQL(s):
    r = s.replace('\\','\\\\').replace("'","\\'").replace('"','\\"')
    r = r.replace('\b','\\b').replace('\r','\\r').replace('\n','\\n')
    r = r.replace('\t','\\t')
    return r

def GetNumber(s: str) -> int:
    m = re.search(r'\d+', s)
    if(m):
        res = m.group()
        return int(res)
    else:
        return -1

def spyonbid(db):
    global bid_list
    global spider_delay
    r = req.get(bid_list)
    page_count = int(re.search(r'(?<=pages: )\d+', r.text).group())
    for i in range(page_count):
        response = req.get(bid_list + str(i))
        page_soup = bs4.BeautifulSoup(response.text, 'html5lib')
        list_data = page_soup.select('.list_data')
        for data in list_data:
            list_tittle_num_data = data.select('.list_title_num_data')[0]
            bid_id = GetNumber(list_tittle_num_data.get('onclick')) #id 
            bid_inviter_number = list_tittle_num_data.text #编号
            bid_url = 'http://www.gdedulscg.cn/home/bill/billdetail/billGuid/' + \
                str(bid_id) + '.html' #url
            # (1)
            bid_tittle = ''                 #标题
            bid_type = '网上竞价需求公告'     #类别
            bid_industry = '所有分类'        #分类
            bid_announce_time = ''          #宣传时间
            bid_end_time = ''               #结束时间
            bid_budget_money = ''           #报价时间
            bid_company = ''                #公司

            detail_response = req.get(bid_url)
            detail_soup = bs4.BeautifulSoup(
                detail_response.text, 'html5lib')
            data_collection1 = detail_soup.select('.bill_info_l2')#1
            for data_item1 in data_collection1:
                data_text: str = data_item1.text
                if(data_text.startswith('采购单位：')):
                    bid_company = data_text[5:]
                elif data_text.startswith('项目名称：'):
                    bid_tittle = data_text[5:]
                elif data_text.startswith('开始时间：'):
                    bid_announce_time = data_text[5:]
                elif data_text.startswith('结束时间：'):
                    bid_end_time = data_text[5:]
                elif data_text.startswith('最高限价(元)：'):
                    bid_budget_money = data_text[8:]
            item_colloction = []
            data_rbody = detail_soup.select('#product_info_tbody')[0]#2
            data_tr_collection = data_rbody.select('tr')
            for data_tr in data_tr_collection:
                data_td_collection = data_tr.select('td')
                if(len(data_td_collection) > 1):
                    # bid_prodact_name = data_td_collection[1].text #产品名称
                    # bid_brand = data_td_collection[2].text #品牌
                    # bid_product_type = data_td_collection[3].text #产品类别
                    # bid_model = data_td_collection[4].text #型号
                    # bid_purchase_quantity = data_td_collection[5].text #采购数量
                    
                    bid_item = {}
                    bid_item['参数'] = ''
                    bid_item['单位'] = Trim(data_td_collection[6].text)
                    bid_item['招标编号'] = bid_inviter_number
                    bid_item['序号']= Trim(data_td_collection[0].text) #产品序号
                    bid_item['产品名称'] = Trim(data_td_collection[1].text) #产品名称
                    bid_item['产品类别'] = Trim(data_td_collection[3].text) #产品类别
                    bid_item['品牌'] = Trim(data_td_collection[2].text) #品牌
                    bid_item['数量'] = Trim(data_td_collection[5].text) #采购数量
                    bid_item['标配'] = Trim(data_td_collection[7].text)
                    bid_item['型号'] = Trim(data_td_collection[4].text) #型号
                    bid_item['url'] = bid_url
                    bid_item['招标平台'] = '广东省教育部门零散采购竞价系统'



                    item_colloction.append(bid_item)
                else:
                    item_colloction[-1]['参数'] += Trim(data_td_collection[0].text)
            bid_tittle = FuckSQL(bid_tittle)
            bid_company = FuckSQL(bid_company)
            bid_announce_time = FuckSQL(bid_announce_time)
            bid_end_time = FuckSQL(bid_end_time)
            bid_budget_money = FuckSQL(bid_budget_money)
            bid_url = FuckSQL(bid_url)
            bid_content = FuckSQL(detail_response.text)

            cursor = db.cursor()
            cmd = '''select count(*) from tb_bid where inviter_number ='{}';'''.format(bid_inviter_number)
            r = cursor.execute(cmd)
            r = cursor.fetchone()[0]
            if  r != 0:
                plog('检测到数据库中',bid_tittle,'已有记录，检测bid_json...')
            else:            
                cmd = '''INSERT INTO tb_bid(title,company,type,industry,announce_time,end_time,budget_money,url,html,inviter_number,platform_id,sysdata)
                    VALUES('{}','{}','{}','{}','{}','{}','{}','{}','{}','{}',7,0);'''.format(bid_tittle, bid_company, bid_type, bid_industry,
                                                                                  bid_announce_time, bid_end_time,
                                                                                  bid_budget_money, bid_url,bid_content,bid_inviter_number)
                cursor = db.cursor()
                r = cursor.execute(cmd)

            cursor = db.cursor()
            cmd = '''select count(*) from tb_bid_json where url ='{}';'''.format(bid_url)
            r = cursor.execute(cmd)
            r = cursor.fetchone()[0]
            if  r != 0:
                plog("json存在，更新完成")
                return

            bid_json = json.dumps(item_colloction,ensure_ascii=False)
            bid_json = FuckSQL(bid_json)

            cmd = '''INSERT INTO tb_bid_json(platform_name,inviter_number,url,json_kv)
            VALUES('广东省教育部门零散采购竞价系统','{}','{}','{}')'''.format(bid_inviter_number,bid_url,bid_json)
            cursor = db.cursor()
            r = cursor.execute(cmd)

            db.commit()
            plog('项目:',bid_tittle,' 已插入，编号：',bid_inviter_number)

bid_result_list = 'http://www.gdedulscg.cn/home/bill/billResult?page='


def spyonbidResult(db):
    global bid_result_list
    global spider_delay
    r = req.get(bid_result_list)
    page_count = int(re.search(r'(?<=pages: )\d+', r.text).group())
    for i in range(page_count):
        response = req.get(bid_result_list + str(i))
        page_soup = bs4.BeautifulSoup(response.text, 'html5lib')
        list_data = page_soup.select('.list_data')
        for data in list_data:
            bid_tittle = ''                 #标题
            bid_announce_time = ''          #宣传时间
            bid_end_time = ''               #结束时间
            bid_budget_money = ''           #报价
            bid_company = ''                #公司
            bid_state = ''
            bid_announce_company = ''
            list_tittle_num_data = data.select('.list_title_num_data')[0]
            bid_id = GetNumber(list_tittle_num_data.get('onclick')) #id 
            bid_inviter_number = list_tittle_num_data.text #编号
            bid_state = Trim(data.select('.list_title_remain_data2')[0].text)

            bid_url = 'http://www.gdedulscg.cn/home/bill/billdetails/billGuid/' + \
                str(bid_id) + '.html' #url
            # (1)


            detail_response = req.get(bid_url)
            detail_soup = bs4.BeautifulSoup(
                detail_response.text, 'html5lib')
            data_collection1 = detail_soup.select('.bill_info_l2')#1
            for data_item1 in data_collection1:
                data_text: str = data_item1.text
                if(data_text.startswith('采购单位：')):
                    bid_company = data_text[5:]
                elif data_text.startswith('项目名称：'):
                    bid_tittle = data_text[5:]
                elif data_text.startswith('成交金额：'):
                    bid_budget_money = data_text[8:]
                elif data_text.startswith('成交单位：'):
                    bid_announce_company = data_text[5:]
                # elif data_text.startswith('开始时间：'):
                #     bid_announce_time = data_text[5:]
                # elif data_text.startswith('结束时间：'):
                #     bid_end_time = data_text[5:]
            time_div = detail_soup.select(".bill_title_time > div")[0].text
            bid_announce_time = re.findall(r'\d{4}-\d{2}-\d{2}\s*\d{2}:\d{2}:\d{2}',time_div)[0]
            bid_end_time = re.findall(r'\d{4}-\d{2}-\d{2}\s*\d{2}:\d{2}:\d{2}',time_div)[1]
            item_colloction = []
            data_rbody = detail_soup.select('#product_info_tbody')[0]#2
            data_tr_collection = data_rbody.select('tr')
            for data_tr in data_tr_collection:
                data_td_collection = data_tr.select('td')
                if(len(data_td_collection) > 1):
                    # bid_prodact_name = data_td_collection[1].text #产品名称
                    # bid_brand = data_td_collection[2].text #品牌
                    # bid_product_type = data_td_collection[3].text #产品类别
                    # bid_model = data_td_collection[4].text #型号
                    # bid_purchase_quantity = data_td_collection[5].text #采购数量
                    
                    bid_item = {}
                    bid_item['参数'] = ''
                    bid_item['单位'] = Trim(data_td_collection[6].text)
                    bid_item['招标编号'] = bid_inviter_number
                    bid_item['序号']= Trim(data_td_collection[0].text) #产品序号
                    bid_item['产品名称'] = Trim(data_td_collection[1].text) #产品名称
                    bid_item['产品类别'] = Trim(data_td_collection[3].text) #产品类别
                    bid_item['品牌'] = Trim(data_td_collection[2].text) #品牌
                    bid_item['数量'] = Trim(data_td_collection[5].text) #采购数量
                    bid_item['标配'] = Trim(data_td_collection[7].text)
                    bid_item['型号'] = Trim(data_td_collection[4].text) #型号
                    bid_item['url'] = bid_url
                    bid_item['招标平台'] = '广东省教育部门零散采购竞价系统'
                    


                    item_colloction.append(bid_item)
                else:
                    item_colloction[-1]['参数'] += Trim(data_td_collection[0].text)
            bid_tittle = FuckSQL(bid_tittle)
            bid_company = FuckSQL(bid_company)
            bid_announce_time = FuckSQL(bid_announce_time)
            bid_end_time = FuckSQL(bid_end_time)
            bid_budget_money = FuckSQL(bid_budget_money)
            bid_url = FuckSQL(bid_url)
            bid_content = FuckSQL(detail_response.text)
            bid_announce_company = FuckSQL(bid_announce_company)
            if(bid_state == '交易成功'):
                bid_state = 1
            else:
                bid_state = 0

            cursor = db.cursor()
            cmd = '''select count(*) from tb_bid_result where inviter_number ='{}';'''.format(bid_inviter_number)
            r = cursor.execute(cmd)
            r = cursor.fetchone()[0]
            if  r != 0:
                plog('检测到数据库中',bid_tittle,'已有记录，检测trjson...')
            else:            
                cmd = '''INSERT INTO tb_bid_result(title,inviter_number,announce_time,end_time,budget_money,state,win_state,company,announce_company,url,html,platform_id,sysdata)
                    VALUES('{}','{}','{}','{}','{}',1,{},'{}','{}','{}','{}',7,0);'''.format(bid_tittle, bid_inviter_number, 
                                                                                            bid_announce_time, bid_end_time,bid_budget_money,
                                                                                            bid_state,bid_company,bid_announce_company,
                                                                                            bid_url,bid_content)
                cursor = db.cursor()
                r = cursor.execute(cmd)

            cursor = db.cursor()
            cmd = '''select count(*) from tb_tr_json where url ='{}';'''.format(bid_url)
            r = cursor.execute(cmd)
            r = cursor.fetchone()[0]
            if  r != 0:
                plog("json存在，更新完成")
                return

            bid_json = json.dumps(item_colloction,ensure_ascii=False)
            bid_json = FuckSQL(bid_json)

            cmd = '''INSERT INTO tb_tr_json(platform_id,platform_name,url,tr_json)
            VALUES(7,'广东省教育部门零散采购竞价系统','{}','{}')'''.format(bid_url,bid_json)
            cursor = db.cursor()
            r = cursor.execute(cmd)

            db.commit()
            plog('项目:',bid_tittle,' 已插入，编号：',bid_inviter_number)
if __name__ == "__main__":
    plog('监控系统启动完成')
    while True:
        # main loop
        try:
            db = pymysql.connect('212.64.5.21','dev','dev','bidpython',charset='utf8')
            spyonbidResult(db)
            spyonbid(db)
            plog("数据库扫描完成")
        except Exception as ex:
            plog('抓取数据时出现异常:',ex)
            db.rollback()
        finally:
            db.commit()
            db.close()
            time.sleep(spider_delay)

    cursor = db.cursor()
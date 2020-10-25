import os
import re
import time
import json
import pymysql

from utils.run import run_func
from utils.request import Query
from utils.soup import DealSoup
from config import DEBUG


def remove_character(content: str):
    if not isinstance(content, str):
        return content
    return content.replace("\n", "").replace("\r",
                                             "").replace("\t", "").replace(
                                                 '\xa0', '').replace('￥', '')


def clean_date(content: str):
    return content.replace('年', '-').replace('月', '-').replace('日', '')


class SpiderMan(object):
    def __init__(self):
        self.bid_path = "http://www.nbzfcg.cn/project/dzjj_Notice1.aspx"
        self.bid_detail = "https://www.gec123.com/xcjenquiry/notice!enquiryNotice.action?notic_seq={}"
        self.result_path = "http://www.nbzfcg.cn/project/dzjj_Notice2.aspx"
        self.result_detail = "https://www.gec123.com/xcj-gateway/api/v1/notices/stable/{}"
        self.header = {
            'Content-Type': 'application/x-www-form-urlencoded',
            'User-Agent':
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.100 Safari/537.36',
            'Accept':
            'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'Referer': 'http://www.nbzfcg.cn/project/dzjj_Notice1.aspx',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,zh;q=0.9'
        }

        self.insert_tb_bid = "INSERT INTO `bidpython`.`tb_bid` ( `title`, `inviter_number`, `announce_time`, `end_time`, `budget_money`, `platform_id`, `url`, `company` ) VALUES ( '{网上竞价名称}', '{网上竞价编号}', '{竞价开始时间}', '{竞价截止时间}', '{金额上限}', 24, '{path}', '{采购人}' );"
        self.insert_bid_result = "INSERT INTO `bidpython`.`tb_bid_result` ( `title`, `inviter_number`, `announce_time`, `end_time`, `announce_date`, `platform_id`, `url`, `company`, `budget_money`, `announce_company` ) VALUES ( '{网上竞价名称}', '{网上竞价编号}', '{竞价开始时间}', '{竞价截至时间}', '{成交公告时间}', 24, '{path}', '{采购人}', '{中标总额}', '{中标公司}' );"
        self.insert_bid_json = "INSERT INTO `bidpython`.`tb_bid_json` ( `shot`, `platform_name`, `inviter_number`, `url`, `json_kv`, `create_time` ) VALUES ( '', '宁波政府采购网', '{}', '{}', '{}', '{}');"
        self.insert_tr_json = "INSERT INTO `bidpython`.`tb_tr_json` ( `platform_id`, `platform_name`, `tr_json`, `url` ) VALUES ( 24, '宁波政府采购网', '{}', '{}');"
        self.request = Query().run
        self.soup = DealSoup().judge
        self.init_sql()
        self.pattern = re.compile(r"\(询价编号：.*\)")

        self.bid_data = '__EVENTTARGET=ctl00%24ContentPlaceHolder3%24gdvProjects%24ctl18%24AspNetPager1&__EVENTARGUMENT={}&__VIEWSTATE=%2FwEPDwULLTEyMDA5MTg4MzQPFgQeBXBhaXh1BQ5CaWRFbmRUaW1lIEFzYx4PU2VhcmNoQ29uZGl0aW9uBTFCaWRTdGF0dXM9NSBBbmQgQmlkRW5kVGltZSA%2BJzIwMjAvMTAvMjQgMjA6MTc6NDcnFgJmD2QWAgIDD2QWAgIFD2QWBAIFDxBkEBUVAAblpK7lsZ4G55yB5bGeBuW4guWxngbmtbfmm5kG5rGf5LicBuaxn%2BWMlwbplYfmtbcG5YyX5LuRBumEnuW3ngbmhYjmuqoG5L2Z5aeaBuWlieWMlgbosaHlsbEG5a6B5rW3CeS%2FneeojuWMugnkuJzpkrHmuZYJ6auY5paw5Yy6BuWkp%2BamrQblhbbku5YG56m65rivFRUABjEwMDAwMAYzMzAwMDAGMzMwMjAwBjMzMDIwMwYzMzAyMDQGMzMwMjA1BjMzMDIxMQYzMzAyMDYGMzMwMjEyBjMzMDI4MgYzMzAyODEGMzMwMjgzBjMzMDIyNQYzMzAyMjYGMzMwMjkxBjMzMDI5MgYzMzAyOTMGMzMwMjk0Bjk5MDAwMAYzMzAyOTYUKwMVZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZGQCDQ88KwANAQAPFgQeC18hRGF0YUJvdW5kZx4LXyFJdGVtQ291bnQCE2QWAmYPZBYkZg8PFgIeB1Zpc2libGVoZGQCAQ9kFgJmD2QWAmYPFQYBMQUyNTUxNgbmtbfmm5lU5a6B5rOi5biC5rW35puZ5Yy66byT5qW86KGX6YGT56S%2B5Yy65Y2r55Sf5pyN5Yqh5Lit5b%2BD55S15Yqo5aSa5Yqf6IO95LqU5q6155CG55aX5bqKCjIwMjAtMTAtMjEEMeWkqWQCAg9kFgJmD2QWAmYPFQYBMgUyNTUxNwbmtbfmm5lU5a6B5rOi5biC5rW35puZ5Yy66byT5qW86KGX6YGT56S%2B5Yy65Y2r55Sf5pyN5Yqh5Lit5b%2BD55S15Yqo5aSa5Yqf6IO95LiJ5q6155CG55aX5bqKCjIwMjAtMTAtMjEEMeWkqWQCAw9kFgJmD2QWAmYPFQYBMwUyNTUxOAbmtbfmm5lF5a6B5rOi5biC5rW35puZ5Yy66byT5qW86KGX6YGT56S%2B5Yy65Y2r55Sf5pyN5Yqh5Lit5b%2BD5r%2BA5YWJ5rK755aX5LuqCjIwMjAtMTAtMjEEMeWkqWQCBA9kFgJmD2QWAmYPFQYBNAUyNTUxOQbmtbfmm5lF5a6B5rOi5biC5rW35puZ5Yy66byT5qW86KGX6YGT56S%2B5Yy65Y2r55Sf5pyN5Yqh5Lit5b%2BD55%2Bt5rOi5rK755aX5LuqCjIwMjAtMTAtMjEEMeWkqWQCBQ9kFgJmD2QWAmYPFQYBNQUyNTUyMAbmtbfmm5lI5a6B5rOi5biC5rW35puZ5Yy66byT5qW86KGX6YGT56S%2B5Yy65Y2r55Sf5pyN5Yqh5Lit5b%2BD5bmy5omw55S15rK755aX5LuqCjIwMjAtMTAtMjEEMeWkqWQCBg9kFgJmD2QWAmYPFQYBNgUyNTUyNAbmtbfmm5k55a6B5rOi5biC5rW35puZ5Yy65qiq6KGX6ZWH5Y2r55Sf6Zmi5Lit6aKR5rK755aX5Luq6aG555uuCjIwMjAtMTAtMjIEMeWkqWQCBw9kFgJmD2QWAmYPFQYBNwUyNTUwMAbmtbfmm5mSAeWugeazouW4gua1t%2BabmeWMuueWvueXhemihOmYsuaOp%2BWItuS4reW%2FgzIwMjDlubTluqblroHms6LluILmtbfmm5nljLog6ICB5bm05Lq65rWB5oSf55ar6IuX5byC5bi45Y%2BN5bqU6KGl5YG%2F6LSj5Lu75L%2Bd6Zmp55S15a2Q56ue5Lu35pyN5Yqh6aG555uuCjIwMjAtMTAtMjEEMeWkqWQCCA9kFgJmD2QWAmYPFQYBOAUyNTUxMQbmtbfmm5lO5a6B5rOi5biC5rW35puZ5Yy65rC06LWE5rqQ566h55CG5Lit5b%2BD5rW35puZ5Yy65Y%2BW5rC055uR5o6n6K6%2B5aSH6YeH6LSt6aG555uuCjIwMjAtMTAtMTkEMeWkqWQCCQ9kFgJmD2QWAmYPFQYBOQUyNTUyOQbmtbfmm5ke5a6B5rOi5biC5a6e6aqM5bCP5a2m5py65Zmo5Lq6CjIwMjAtMTAtMjIEMeWkqWQCCg9kFgJmD2QWAmYPFQYCMTAFMjU1MjIG5rW35puZVOWugeazouW4gua1t%2BabmeWMuuilv%2BmXqOacm%2BaYpeekvuWMuuWNq%2BeUn%2BacjeWKoeS4reW%2Fg%2BmHh%2Bi0reenu%2BWKqOW8j%2BepuuawlOa2iOavkuWZqAoyMDIwLTEwLTIyBDLlpKlkAgsPZBYCZg9kFgJmDxUGAjExBTI1NTIzBua1t%2BabmTblroHms6LluILmtbfmm5nljLrmqKrooZfplYfljavnlJ%2FpmaLpq5jpopHnlLXliIDpobnnm64KMjAyMC0xMC0yMQQy5aSpZAIMD2QWAmYPZBYCZg8VBgIxMgUyNTUxNAbmtbfmm5kw5a6B5rOi5biC5Lic5oGp5Lit5a2m5pWw5a2X5YyW5qCh5Zut566h55CG57O757ufCjIwMjAtMTAtMjIEM%2BWkqWQCDQ9kFgJmD2QWAmYPFQYCMTMFMjU1MzEG5rW35puZPOWugeazouW4gua1t%2BabmeWMuuWPo%2BiFlOWMu%2BmZouWPo%2BiFlOagueeuoeayu%2BeWl%2Bi%2BheWKqeiuvuWkhwoyMDIwLTEwLTIyBDPlpKlkAg4PZBYCZg9kFgJmDxUGAjE0BTI1NTM1Bua1t%2BabmTnlroHms6LluILniLHoj4roibrmnK%2FlrabmoKHmmbrmhaflubPlronmoKHlm63pl6jnpoHns7vnu58KMjAyMC0xMC0yMwQz5aSpZAIPD2QWAmYPZBYCZg8VBgIxNQUyNTUzNgbmtbfmm5lC5a6B5rOi5biC5rW35puZ5Yy66ZuG5aOr5riv6ZWH5Lit5b%2BD5Yid57qn5Lit5a2m5a6k5YaFTEVE5pi%2B56S65bGPCjIwMjAtMTAtMjMEM%2BWkqWQCEA8PFgIfBGhkZAIRD2QWAmYPZBYCAgEPDxYEHgtSZWNvcmRjb3VudAITHghQYWdlU2l6ZQIPZGQYAQUlY3RsMDAkQ29udGVudFBsYWNlSG9sZGVyMyRnZHZQcm9qZWN0cw88KwAKAQgCAmSBUlfkCVyjBeP%2B5vCj%2Bz044nhBmQ%3D%3D&ctl00%24ContentPlaceHolder3%24txtProjectName=&ctl00%24ContentPlaceHolder3%24txtSerialNumber=&ctl00%24ContentPlaceHolder3%24ddlProjectRegion=&ctl00%24ContentPlaceHolder3%24gdvProjects%24ctl18%24AspNetPager1_input=1'
        self.result_data = '__EVENTTARGET=ctl00%24ContentPlaceHolder3%24gdvProjects%24ctl18%24AspNetPager1&__EVENTARGUMENT={}&__VIEWSTATE=%2FwEPDwUJLTk1MTY2Mzg1DxYCHgVwYWl4dQUWWkJOb3RpY2VCZWdpblRpbWUgRGVzYxYCZg9kFgICAw9kFgICBQ9kFgQCBQ8QZBAVFQAG5aSu5bGeBuecgeWxngbluILlsZ4G5rW35puZBuaxn%2BS4nAbmsZ%2FljJcG6ZWH5rW3BuWMl%2BS7kQbphJ7lt54G5oWI5rqqBuS9meWnmgblpYnljJYG6LGh5bGxBuWugea1twnkv53nqI7ljLoJ5Lic6ZKx5rmWCemrmOaWsOWMugblpKfmpq0G5YW25LuWBuepuua4rxUVAAYxMDAwMDAGMzMwMDAwBjMzMDIwMAYzMzAyMDMGMzMwMjA0BjMzMDIwNQYzMzAyMTEGMzMwMjA2BjMzMDIxMgYzMzAyODIGMzMwMjgxBjMzMDI4MwYzMzAyMjUGMzMwMjI2BjMzMDI5MQYzMzAyOTIGMzMwMjkzBjMzMDI5NAY5OTAwMDAGMzMwMjk2FCsDFWdnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2RkAgsPPCsADQEADxYEHgtfIURhdGFCb3VuZGceC18hSXRlbUNvdW50AqqjAWQWAmYPZBYkZg8PFgIeB1Zpc2libGVoZGQCAQ9kFgJmD2QWAmYPFQUBMQUyNTQzNAbmtbfmm5k%2B5a6B5rOi5biC5rW35puZ5Yy656ys5LiJ5Yy76Zmi5Y%2BM5p2%2FRFLvvIjmlbTmnLrvvInkv53kv67mnI3liqEKMjAyMC0xMC0yMmQCAg9kFgJmD2QWAmYPFQUBMgUyNTQ0MAbmtbfmm5lL5a6B5rOi5biC5rW35puZ5Yy65pyI5rmW6KGX6YGT56S%2B5Yy65Y2r55Sf5pyN5Yqh5Lit5b%2BD54mZ56eR57u85ZCI5rK755aX5py6CjIwMjAtMTAtMjJkAgMPZBYCZg9kFgJmDxUFATMFMjU0OTUG5rW35puZM%2BWugeazouW4guauteWhmOWtpuagoeS4i%2BayieW5v%2BWcuuetieijheS%2FruOAgeijhemlsAoyMDIwLTEwLTIyZAIED2QWAmYPZBYCZg8VBQE0BTI1NTAyBua1t%2BabmT%2FlroHms6LluILmtbfmm5nljLrmqKrooZfplYfkuK3lv4PliJ3nuqfkuK3lrabmiqXlkYrljoVMRUTlsY%2FluZUKMjAyMC0xMC0yMmQCBQ9kFgJmD2QWAmYPFQUBNQUyNTQ5Mwbmtbfmm5k35a6B5rOi5biC5rW35puZ5Yy65qiq6KGX6ZWH5Lit5b%2BD5bCP5a2m4oCc56u5LueUn%2Ba0u%2BKAnQoyMDIwLTEwLTIyZAIGD2QWAmYPZBYCZg8VBQE2BTI1NDk0Bua1t%2BabmSrlroHms6LluILmrrXloZjlrabmoKHlvq7moLzmlZnlrqTmoYzmpIXmn5wKMjAyMC0xMC0yMmQCBw9kFgJmD2QWAmYPFQUBNwUyNTQ5OAbmtbfmm5k85a6B5rOi5biC5a2Z5paH6Iux5bCP5a2m5bCP5a2m6LWE5rqQ5pWZ5a6k6K6%2B5aSH6YeH6LSt6aG555uuCjIwMjAtMTAtMjJkAggPZBYCZg9kFgJmDxUFATgFMjU0OTAG5rW35puZG%2BaVmeWupOmfs%2BWTjeOAgeeBr%2BWFieaUuemAoAoyMDIwLTEwLTIyZAIJD2QWAmYPZBYCZg8VBQE5BTI1NDkyBua1t%2BabmVflroHms6LluILmtbfmm5nljLrljavnlJ%2FlgaXlurflsYDljLrln5%2FljavnlJ%2Fkv6Hmga%2FlubPlj7DlronlhajnrYnnuqfkv53miqTmtYvor4Tpobnnm64KMjAyMC0xMC0yMmQCCg9kFgJmD2QWAmYPFQUCMTAFMjU1MDEG5rW35puZJOWugeazouW4guWunumqjOWtpuagoeiZmuaLn%2BeUteinhuWPsAoyMDIwLTEwLTIyZAILD2QWAmYPZBYCZg8VBQIxMQUyNTQzNQbmtbfmm5lD5a6B5rOi5biC5rW35puZ5Yy656ys5LiJ5Yy76ZmiMTbmjpJDVO%2B8iOS4jeWQq%2BeQg%2Beuoe%2B8ieS%2FneS%2FruacjeWKoQoyMDIwLTEwLTIyZAIMD2QWAmYPZBYCZg8VBQIxMgUyNTQ4MQbmtbfmm5k25a6B5rOi5biC5bC55rGf5bK45bCP5a2m5a2m5qCh6LWw5buK5oKs5rWu5ou86KOF5Zyw5p2%2FCjIwMjAtMTAtMjJkAg0PZBYCZg9kFgJmDxUFAjEzBTI1NDkxBuW4guWxnk7lroHms6LluILljavnlJ%2Fkv6Hmga%2FkuK3lv4PlroHms6LluILlhajmsJHlgaXlurfkv6Hmga%2FlubPlj7DlubTluqbov5Dnu7TmnI3liqEKMjAyMC0xMC0xOWQCDg9kFgJmD2QWAmYPFQUCMTQFMjU0ODUG5biC5bGeWuWugeazouW4guWNq%2BeUn%2BS%2FoeaBr%2BS4reW%2Fg%2BWugeazouW4guS8oOafk%2BeXheOAgeaFoueXheWNj%2BWQjOeuoeeQhuezu%2Be7n%2BW5tOW6pue7tOaKpOacjeWKoQoyMDIwLTEwLTE5ZAIPD2QWAmYPZBYCZg8VBQIxNQUyNTQ4NgbluILlsZ5O5a6B5rOi5biC5Y2r55Sf5L%2Bh5oGv5Lit5b%2BD5a6B5rOi5biC6K6h5YiS5YWN55ar5pS56YCg6aG555uu5bm05bqm57u05oqk5pyN5YqhCjIwMjAtMTAtMTlkAhAPDxYCHwNoZGQCEQ9kFgJmD2QWAgIBDw8WBB4LUmVjb3JkY291bnQCqqMBHghQYWdlU2l6ZQIPZGQYAQUlY3RsMDAkQ29udGVudFBsYWNlSG9sZGVyMyRnZHZQcm9qZWN0cw88KwAKAQgC8gpk%2B%2F6jJ0fhmLIXH3u0OuN95fuwoRU%3D&ctl00%24ContentPlaceHolder3%24txtProjectName=&ctl00%24ContentPlaceHolder3%24txtSerialNumber=&ctl00%24ContentPlaceHolder3%24ddlProjectRegion=&ctl00%24ContentPlaceHolder3%24gdvProjects%24ctl18%24AspNetPager1_input=1'

    def init_sql(self):
        from config import DATABASES

        try:
            if DEBUG:
                config = DATABASES["debug"]
            else:
                config = DATABASES["product"]

            ecnu_mysql = pymysql.connect(**config)

        except pymysql.err.OperationalError as exc:
            print('登录失败！TimeoutError!')
            os._exit(0)
        else:
            self.ecnu_cursor = ecnu_mysql.cursor()

    def judge_already(self, item_code):
        if self.bid_type == "bid":
            sql = "SELECT `id` FROM `bidpython`.`tb_bid` WHERE `inviter_number` = '{}' and `platform_id` = 24 LIMIT 1;"
        elif self.bid_type == "bidResult":
            sql = "SELECT `id` FROM `bidpython`.`tb_bid_result` WHERE `inviter_number` = '{}' and `platform_id` = 24 LIMIT 1;"

        if run_func(self.ecnu_cursor.execute, sql.format(item_code)) == 0:
            return True
        else:
            return

    def get_time(self):
        return time.strftime('%Y-%m-%d %H:%M:%S',
                             time.localtime(int(time.time())))

    def deal_detail(self, page):
        resp = run_func(self.request,
                        self.bid_path,
                        header=self.header,
                        data=self.bid_data.format(page))

        tables = self.soup(
            self.soup(resp, {'id': 'ctl00_ContentPlaceHolder3_gdvProjects'}),
            'table', True)

        for table in tables[:-1]:
            href = self.soup(table, 'td', True)[1].a.get('href')
            uri = f'http://www.nbzfcg.cn/project/{href}'

            resp = run_func(self.request, uri, header=self.header)
            # resp = resp.replace('\n', '').replace('\t', '').replace('\xa0', '').replace('\r', '')
            # resp = ''.join(resp.split())
            info = {}
            bgs = self.soup(resp, {'bgcolor': 'B3CDE6'}, True)
            info["网上竞价编号"] = remove_character(
                bgs[0].contents[5].contents[3].text)

            if not self.judge_already(info["网上竞价编号"]):
                continue

            info["网上竞价名称"] = bgs[0].contents[3].contents[3].text

            info["采购人"] = bgs[1].contents[1].contents[7].text
            info["竞价开始时间"] = bgs[1].contents[1].contents[3].text
            info["竞价截止时间"] = bgs[1].contents[3].contents[3].text
            info['金额上限'] = ''
            info["path"] = uri

            tr_json = {
                "参数": "",
                "单位": bgs[2].contents[3].contents[3].text,
                "招标编号": info["网上竞价编号"],
                "序号": 1,
                "产品名称": bgs[2].contents[3].contents[0].text,
                "产品类别": "",
                "产品单价": '',
                "合计": '',
                "品牌": bgs[2].contents[3].contents[1].text,
                "数量": bgs[2].contents[3].contents[4].text,
                "标配": "",
                "型号": '',
                "url": uri,
                "招标平台": "宁波政府采购网",
                "售后服务": "",
            }

            info = {x: remove_character(info[x]) for x in info}
            tr_json = [{x: remove_character(tr_json[x]) for x in tr_json}]
            run_func(self.ecnu_cursor.execute,
                     self.insert_tb_bid.format(**info))

            run_func(
                self.ecnu_cursor.execute,
                self.insert_bid_json.format(
                    info["网上竞价编号"], info["path"],
                    json.dumps(tr_json, ensure_ascii=False), self.get_time()))

    def deal_result(self, page):
        resp = run_func(self.request,
                        self.result_path,
                        header=self.header,
                        data=self.result_data.format(page))

        tables = self.soup(
            self.soup(resp, {'id': 'ctl00_ContentPlaceHolder3_gdvProjects'}),
            'table', True)

        for table in tables[:-1]:
            href = self.soup(table, 'td', True)[1].a.get('href')
            uri = f'http://www.nbzfcg.cn/project/{href}'

            resp = run_func(self.request, uri, header=self.header)
            info = {}
            tables = self.soup(resp, 'table', True)

            info["网上竞价编号"] = remove_character(
                tables[5].contents[7].contents[3].text)

            if not self.judge_already(info["网上竞价编号"]):
                continue

            info["网上竞价名称"] = tables[5].contents[5].contents[3].text

            info["采购人"] = tables[9].contents[5].contents[3].text
            info["path"] = uri
            info["成交公告时间"] = tables[5].contents[3].contents[3].text
            info["竞价开始时间"] = tables[9].contents[1].contents[3].text
            info["竞价截至时间"] = tables[9].contents[3].contents[3].text

            try:
                info["中标总额"] = tables[12].contents[11].contents[3].text
                info['中标公司'] = tables[5].contents[1].contents[3].text
                tr_json = {
                    "成交时间": info["成交公告时间"],
                    "招标编号": info["网上竞价编号"],
                    "规格配置": '',
                    "详情url": uri,
                    "平台名称": "宁波政府采购网",
                    "总价": info["中标总额"],
                    "中标供应商": info['中标公司'],
                    "设备名称": tables[15].contents[1].contents[1].text,
                    "创建时间": self.get_time(),
                    "品牌": tables[15].contents[1].contents[3].text,
                    "型号": tables[15].contents[1].contents[5].text,
                    "数量": tables[15].contents[1].contents[7].text
                }
            except:
                info["中标总额"] = ''
                info['中标公司'] = ''

                tr_json = {
                    "成交时间": info["成交公告时间"],
                    "招标编号": info["网上竞价编号"],
                    "规格配置": '',
                    "详情url": uri,
                    "平台名称": "宁波政府采购网",
                    "总价": info["中标总额"],
                    "中标供应商": info['中标公司'],
                    "设备名称": '',
                    "创建时间": self.get_time(),
                    "品牌": '',
                    "型号": '',
                    "数量": ''
                }

            info = {x: remove_character(info[x]) for x in info}
            tr_json = [{x: remove_character(tr_json[x]) for x in tr_json}]

            run_func(self.ecnu_cursor.execute,
                     self.insert_bid_result.format(**info))

            run_func(
                self.ecnu_cursor.execute,
                self.insert_tr_json.format(
                    json.dumps(tr_json, ensure_ascii=False), uri))

    def run(self):
        for page in range(1, 10):
            self.bid_type = "bid"
            run_func(self.deal_detail, page)
            self.bid_type = "bidResult"
            run_func(self.deal_result, page)


if __name__ == "__main__":
    os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    SpiderMan().run()

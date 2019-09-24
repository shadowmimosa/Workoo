import os
import time
import random
import pymysql
import platform
import pandas as pd
from bs4 import BeautifulSoup

from request import Query




a = platform.system()

if platform.system() == "Linux":
    DEBUG = False
elif system_version == "Windows":
    DEBUG = True


class DealCicpa(object):
    def __init__(self):
        self.office_list = "http://cmispub.cicpa.org.cn/cicpa2_web/OfficeIndexAction.do"
        self.office_path_before = "http://cmispub.cicpa.org.cn/cicpa2_web/002/{},{}/7.shtml"
        self.office_path = "http://cmispub.cicpa.org.cn/cicpa2_web/09/{}.shtml"

        # self.staff_list = "http://cmispub.cicpa.org.cn/cicpa2_web/public/query/swszs/%20/{}.html"
        self.staff_list = "http://cmispub.cicpa.org.cn/cicpa2_web/OfficeIndexAction.do"
        self.staff_path = "http://cmispub.cicpa.org.cn/cicpa2_web/07/{}.shtml"

        self.header = {
            "Accept":
            "text/html, application/xhtml+xml, image/jxr, */*",
            "Referer":
            "http://cmispub.cicpa.org.cn/cicpa2_web/public/query2/1/00.shtml",
            "Accept-Language":
            "zh-Hans-CN,zh-Hans;q=0.8,en-IE;q=0.5,en;q=0.3",
            "User-Agent":
            "Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko",
            "Content-Type":
            "application/x-www-form-urlencoded",
            "Accept-Encoding":
            "gzip, deflate",
            "Host":
            "cmispub.cicpa.org.cn",
            "Pragma":
            "no-cache",
            "Cookie":
            "JSESSIONID=AEE4B3114FBA5176021022B050D84B0B; cookiee=20111116"
        }
        self.data = "pageSize=15&pageNum={}&method=indexQuery&queryType=1&isStock=00&ascGuid=0000010F84968569DDB2CD9ADD2CAA43&offName=&offAllcode=&personNum="
        self.staff_data = "method=getPersons&offGuid={}&pageNum={}&pageSize=10&title=&age=&stuexpCode="

        self.request = Query()

        self.insert_office = "INSERT INTO `workoo`.`cicpa_offices`(`会计师事务所名称`, `证书编号`, `联系人`, `联系电话`, `办公地址`, `传真`, `通讯地址`, `邮政编码`, `电子邮箱`, `网址`, `批准设立机关`, `批准设立文件号`, `批准设立时间`, `法定代表人(或执行合伙人)`, `出资额或注册资本(万元)`, `组织形式(有限/合伙)`, `分所数量`, `合伙人或股东人数`, `注册会计师人数`, `从业人员人数`, `注册会计师人数(含分所)`, `从业人员人数(含分所)`, `大于70岁人数`, `小于等于70岁且大于60岁人数`, `小于等于60岁且大于40岁人数`, `小于等于40岁人数`, `博士研究生人数`, `硕士研究生人数`, `本科人数`, `大专及以下人数`, `加入国际网络`, `境外分支机构`, `是否具有内部培训资格`, `继续教育完成率(上一年度)`, `处罚/惩戒信息(披露时限:自2016年至今)`, `被检查信息`, `参与公益活动`, `其它`) VALUES ('{会计师事务所名称}', '{证书编号}', '{联系人}', '{联系电话}', '{办公地址}', '{传真}', '{通讯地址}', '{邮政编码}', '{电子邮箱}', '{网址}', '{批准设立机关}', '{批准设立文件号}', '{批准设立时间}', '{法定代表人(或执行合伙人)}', '{出资额或注册资本(万元)}', '{组织形式(有限/合伙)}', '{分所数量}', '{合伙人或股东人数}', '{注册会计师人数}', '{从业人员人数}', '{注册会计师人数(含分所)}', '{从业人员人数(含分所)}', '{大于70岁人数}', '{小于等于70岁且大于60岁人数}', '{小于等于60岁且大于40岁人数}', '{小于等于40岁人数}', '{博士研究生人数}', '{硕士研究生人数}', '{本科人数}', '{大专及以下人数}', '{加入国际网络}', '{境外分支机构}', '{是否具有内部培训资格}', '{继续教育完成率(上一年度)}', '{处罚/惩戒信息}', '{被检查信息}', '{参与公益活动}', '{其它}');"
        self.insert_staff = "INSERT INTO `workoo`.`cicpa_staffs`(`office_id`, `姓名`, `性别`, `出生日期`, `所内职务`, `是否党员`, `学历`, `学位`, `所学专业`, `毕业学校`, `资格取得方式(考试/考核)`, `全科合格证书号`, `全科合格年份`, `考核批准文号`, `批准时间`, `注册会计师证书编号`, `是否合伙人(股东)`, `批准注册文件号`, `批准注册时间`, `所在事务所`, `本年度应完成学时`, `本年度已完成学时`, `处罚/惩戒信息`, `参加公益活动`) VALUES ('{office_id}', '{姓名}', '{性别}', '{出生日期}', '{所内职务}', '{是否党员}', '{学历}', '{学位}', '{所学专业}', '{毕业学校}', '{资格取得方式(考试/考核)}', '{全科合格证书号}', '{全科合格年份}', '{考核批准文号}', '{批准时间}', '{注册会计师证书编号}', '{是否合伙人(股东)}', '{批准注册文件号}', '{批准注册时间}', '{所在事务所}', '{本年度应完成学时}', '{本年度已完成学时}', '{处罚/惩戒信息}', '{参加公益活动}');"
        self.select_staff_count = "SELECT count(id) FROM `workoo`.`cicpa_staffs` WHERE `office_id` = {};"
        self.select_count_from_office = "SELECT `注册会计师人数` FROM `workoo`.`cicpa_offices` WHERE `id` = {};"
        self.init_sql()
        self.office_num = 0
        self.key = None
        self.value = None

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

    def remove_character(self, item_list: list):
        for item in item_list:
            if item == "\n":
                item_list.remove("\n")

        return item_list

    def deal_text(self, content):
        return content.replace("\t",
                               "").replace("\r", "").replace("\n", "").replace(
                                   " ", "").replace("\xa0", "").replace(
                                       "（", "(").replace("）", ")")

    def get_text(self):

        if self.key is None:
            return
        elif self.value is None:
            return
        else:
            key = self.key.replace("\t", "").replace("\n", "").replace(
                " ", "").replace("\xa0", "").replace("（", "(").replace(
                    "）", ")")
            value = self.value.replace("\t", "").replace("\n", "").replace(
                " ", "")
            self.key = None
            self.value = None

            if len(key) == 0:
                return
            else:
                try:
                    self.info[key] = value.replace("（请点击）", "").replace(
                        "请点击", "")
                except AttributeError as exc:
                    pass

    def deal_resp(self, path, header, data=None):
        while True:
            resp = self.request.run(path, header=header, data=data)

            if isinstance(resp, str):
                if "错误异常页面" in resp:
                    time.sleep(30)
                    continue
                # elif "中国注册会计师协会行业管理信息系统" not in resp:
                #     time.sleep(30)
                #     continue
                else:
                    # time.sleep(random.uniform(0, 3))
                    return resp
            elif isinstance(resp, int):
                if resp == 502:
                    print("Sleep Now")
                    time.sleep(3600)
                    continue
                elif resp == 400:
                    time.sleep(5)
                    print("Continue Now")
                    return

    def judge_already(self, sign, code):
        if sign == 0:
            sql = "SELECT `id` FROM `workoo`.`cicpa_offices` WHERE `证书编号` = '{}' LIMIT 1;"
        else:
            sql = "SELECT `id` FROM `workoo`.`cicpa_staffs` WHERE `注册会计师证书编号` = '{}' LIMIT 1;"

        if self.ecnu_cursor.execute(sql.format(code)) == 0:
            return True
        else:
            return self.ecnu_cursor.fetchone()[0]

    def judge_count(self, office_id):
        self.ecnu_cursor.execute(self.select_staff_count.format(office_id))
        already_has = self.ecnu_cursor.fetchone()[0]

        self.ecnu_cursor.execute(
            self.select_count_from_office.format(office_id))
        should_has = int(self.ecnu_cursor.fetchone()[0])

        if already_has < should_has:
            return office_id
        else:
            return True

    def get_office_info(self):
        resp = self.deal_resp(
            self.office_path_before.format(self.office_href, self.office_id),
            self.header)
        resp = self.deal_resp(
            self.office_path.format(self.office_href), self.header)
        table_obj = BeautifulSoup(resp,
                                  "lxml").find(attrs={"class": "detail_table"})

        tr_list = self.remove_character(table_obj.contents)
        self.info = {}
        other_content = ""
        for item in tr_list:
            if not isinstance(item, str):
                if item.name == "tr":
                    td_list = self.remove_character(item.contents)
                    for td in td_list:
                        if td.attrs.get("class") == None:
                            pass
                        elif "table_header" in td.attrs.get("class"):
                            pass
                        elif "tdl" in td.attrs.get("class"):
                            self.key = td.text
                        elif "data_tb_content" in td.attrs.get("class"):
                            self.value = td.text
                        self.get_text()

                elif item.name == "tbody":
                    c = item.attrs.get("style")
                    if item.attrs.get("style") == "display:none":
                        pass
                    elif item.attrs.get("style") == "display:":
                        other_tr_list = item.find(attrs={
                            "class": "detail_table"
                        }).contents
                        for other_td in other_tr_list[3].children:
                            if other_td != "\n":
                                if len(other_content) == 0:
                                    other_content = self.deal_text(
                                        other_td.text)
                                else:
                                    other_content = " ".join([
                                        other_content,
                                        self.deal_text(other_td.text)
                                    ])

        self.info["其它"] = other_content
        self.info["处罚/惩戒信息"] = self.info["处罚/惩戒信息(披露时限:自2016年至今)"]

        status = self.judge_already(0, self.info["证书编号"])
        if status is True:
            self.ecnu_cursor.execute(self.insert_office.format(**self.info))
            self.office_key_id = self.ecnu_cursor.lastrowid

            if DEBUG:
                self.get_staff_list()
            else:
                try:
                    self.get_staff_list()
                except Exception as exc:
                    print(
                        "--->Error: the staff list is wrong, the error is {}".
                        format(exc))

        else:
            print("--->Info: office is already exist")

            if self.judge_count(status) is not True:
                self.office_key_id = status
                print("--->Info: person count is lack, try again now")

                if DEBUG:
                    self.get_staff_list()
                else:
                    try:
                        self.get_staff_list()
                    except Exception as exc:
                        print(
                            "--->Error: the staff list is wrong, the error is {}"
                            .format(exc))
            else:
                print("--->Info: person count is ok")

    def get_staff_info(self):
        resp = self.deal_resp(
            self.staff_path.format(self.staff_href), header=self.header)
        soup = BeautifulSoup(resp, "lxml")

        tr_list = self.remove_character(
            soup.find(attrs={
                "class": "detail_table"
            }).contents)

        other_content = ""
        for item in tr_list:
            if not isinstance(item, str):
                if item.name == "tr":
                    td_list = self.remove_character(item.contents)
                    for td in td_list:
                        if not isinstance(td, str):
                            if td.attrs.get("class") == None:
                                pass
                            elif "table_header" in td.attrs.get("class"):
                                pass
                            elif "tdl" in td.attrs.get("class"):
                                self.key = td.text
                            elif "data_tb_content" in td.attrs.get("class"):
                                self.value = td.text
                            self.get_text()

        self.info["office_id"] = self.office_key_id
        for key in [
                "姓名", "性别", "出生日期", "所内职务", "是否党员", "学历", "学位", "所学专业", "毕业学校",
                "资格取得方式(考试/考核)", "全科合格证书号", "全科合格年份", "考核批准文号", "批准时间",
                "注册会计师证书编号", "是否合伙人(股东)", "批准注册文件号", "批准注册时间", "所在事务所",
                "本年度应完成学时", "本年度已完成学时", "处罚/惩戒信息", "参加公益活动"
        ]:
            if key not in self.info.keys():
                self.info[key] = ""
        if self.judge_already(1, self.info["注册会计师证书编号"]) is True:
            self.ecnu_cursor.execute(self.insert_staff.format(**self.info))
        else:
            print("--->Info: staff is already exist")

    def get_staff_list(self):

        for page in range(1, 1000):
            print("--->Info: Staff page is {}".format(page))
            resp = self.deal_resp(
                self.staff_list,
                header=self.header,
                data=self.staff_data.format(self.office_href, page))

            soup = BeautifulSoup(resp, "lxml")

            table_obj = soup.find(attrs={"id": "pertable"})

            tr_list = self.remove_character(table_obj.contents)

            for tr in tr_list:
                self.info = {}
                if tr.attrs.get("class") is None:
                    # if "table_header" not in tr.attrs.get("class"):
                    td_list = self.remove_character(tr.contents)
                    for index, td in enumerate(td_list):
                        if index == 1:
                            self.staff_href = td.find("a").attrs.get(
                                "onclick").replace("getPerDetails('",
                                                   "").split(",")[0].replace(
                                                       "'", "")
                        elif index == 4:
                            self.info["出生日期"] = self.deal_text(td.text)

                    if DEBUG:
                        self.get_staff_info()
                    else:
                        try:
                            self.get_staff_info()
                        except Exception as exc:
                            print(
                                "--->Error: the staff info is wrong, the error is {}"
                                .format(exc))

            if "disabled>下一页</" in resp:
                break
            elif "下一页" not in resp:
                break

    def get_office_list(self, page):
        resp = self.deal_resp(
            self.office_list, header=self.header, data=self.data.format(page))
        soup = BeautifulSoup(resp, "lxml")
        tr_list = soup.find_all(attrs={"class": "rsTr"})

        for index, item in enumerate(tr_list):
            # if index < 13:
            #     continue
            self.office_num += 1
            print("--->Info: Office number is {}".format(self.office_num))
            self.office_id = item.find(attrs={"style": "width: 10%;"}).text
            self.office_href = item.find(attrs={
                "align": "left"
            }).find("a")["href"].replace("javascript:viewDetail(", "").replace(
                "'", "").split(",")[0]

            if DEBUG:
                self.get_office_info()
            else:
                try:
                    self.get_office_info()
                except Exception as exc:
                    print(
                        "--->Error: the office info is wrong, the error is {}".
                        format(exc))

    def main(self):
        for page in range(1, 300):
            print("--->Info: Office page is {}".format(page))

            if DEBUG:
                self.get_office_list(page)
            else:
                try:
                    self.get_office_list(page)
                except Exception as exc:
                    print("--->Error: the error is {}, the page is {}".format(
                        exc, page))
                    continue


if __name__ == "__main__":
    DealCicpa().main()
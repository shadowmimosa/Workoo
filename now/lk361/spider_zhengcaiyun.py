import os
import re
import time
import json
import random
import pymysql
import xlsxwriter
from PIL import Image
from io import BytesIO
from urllib.parse import quote
from urllib.request import urlopen
from bs4 import BeautifulSoup

from config import DEBUG, logger
from utils.run import run_func
from utils.request import Query
from utils.soup import DealSoup


class DealLk(object):
    def __init__(self):
        self.path = "https://smallshop50462.lk361.com.cn/mall.api?___method={method}&tok={token}&s={s}&pagetype={type}"
        self.header = {
            "Host":
            "smallshop50462.lk361.com.cn",
            "Accept":
            "application/json, text/plain, */*",
            "Origin":
            "https://smallshop50462.lk361.com.cn",
            "pagename":
            "index",
            "User-Agent":
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36 MicroMessenger/7.0.4.501 NetType/WIFI MiniProgramEnv/Windows WindowsWechat",
            "Content-Type":
            "application/x-www-form-urlencoded",
            "Referer":
            "https://smallshop50462.lk361.com.cn/index.html?v=8245",
            "Accept-Encoding":
            "gzip, deflate",
            "Accept-Language":
            "en-us,en",
            "Cookie":
            "acw_tc=707c9f9815739036991931982e48b4a60707f314baa4d27a2323d9011faed9; nickname=ShadowMimosa; _cookieId=APP_d30f5ec8-506b-49d5-ae96-2ba07ed0cce5; grwng_uid=3bce06fe-5dda-4a73-b873-05604edb4e06; issmall=True; sid=0; drid=0; wx_openid=olEHWvp-txdbrvXVaAcKJ9YqEbM4; gr_user_id=e3f712a9-4dcc-4e30-a0b1-f30982a18923; ba1b0cd2008605e4_gr_session_id_546cc1b9-153d-4e29-b57f-87c26bdd2dae=true; ba1b0cd2008605e4_gr_session_id=546cc1b9-153d-4e29-b57f-87c26bdd2dae; ba1b0cd2008605e4_gr_last_sent_sid_with_cs1=546cc1b9-153d-4e29-b57f-87c26bdd2dae; ba1b0cd2008605e4_gr_last_sent_cs1=11030117; ba1b0cd2008605e4_gr_cs1=11030117; tok=f60906cb2eb94d6b92007935ece5d3a6; s=36350ca3a30015ea"
        }

        self.insert_tr_json = insert_sql = "INSERT INTO `bidpython`.`tb_tr_json` ( `platform_id`, `platform_name`, `tr_json`, `url` ) VALUES ( 17, '政府采购云', '{}', '{}');"

        self.request = Query().run
        self.soup = DealSoup().judge
        # self.init_sql()
        self.init_xlsx()
        self.count = 1

    def init_xlsx(self):
        self.workbook = xlsxwriter.Workbook("./info.xlsx")
        self.worksheet = self.workbook.add_worksheet("sheet 1")

        self.worksheet.write_row(
            "A1", ["一级分类", "二级分类", "三级分类", "名称", "规格", "价格", "图片"])

        self.worksheet.set_column("G:G", 50)
        # self.worksheet.set_column(6, 6, 50)

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

    def get_info(self):
        pass

    def get_goods(self, gid, name, page=1):
        param = {
            "method": "CC.ERP.Mall.BLL.Goods.GoodManager.SearchGoods",
            # "token": "f60906cb2eb94d6b92007935ece5d3a6",
            # "s": "36350ca3a30015ea",
            "token": "",
            "s": "",
            "type": "mall"
        }
        path = self.path.format(**param)
        data = '{{"key":"","tag":0,"brandid":0,"goodsdir":{},"page":{},"pagesize":20,"orderby":4,"categoryName":"{}"}}'.format(
            gid, page, name)

        resp = run_func(
            self.request,
            path,
            header=self.header,
            data="__postdata={}".format(quote(data)))

        good_list = json.loads(resp)["data"]

        for good in good_list["datasource"]:
            fullname = good["fullname"]
            spec = good["spec"]
            price = good["price"]
            img = good['imgurl']

            if ".jpg" in img:
                img = img.replace(".jpg", "/150x150.jpg")

            img_data = BytesIO(urlopen(img).read())
            pic = Image.open(img_data)

            width, height = pic.size[0], pic.size[0]

            print(width, height)

            self.worksheet.set_row(self.count, height)

            self.count += 1

            self.worksheet.write_row("A{}".format(self.count), [
                self.level_1,
                self.level_2,
                self.level_3 if self.level_3 else "",
                fullname,
                spec,
                price,
            ])

            self.worksheet.insert_image(
                "G{}".format(self.count), "img", {
                    "image_data": img_data,
                    "x_offset": 1,
                    "y_offset": 1,
                    "x_scale": 1,
                    "y_scale": 1,
                    "positioning": 1
                })

        if good_list["pageinfo"]["curpage"] != good_list["pageinfo"][
                "totalpages"]:
            page += 1
            self.get_goods(gid, name, page)

    def main(self):
        param = {
            "method": "CC.ERP.Mall.BLL.Goods.MallManager.Category",
            # "token": "f60906cb2eb94d6b92007935ece5d3a6",
            # "s": "36350ca3a30015ea",
            "token": "",
            "s": "",
            "type": "mall"
        }
        path = self.path.format(**param)

        resp = run_func(
            self.request, path, header=self.header, data="__postdata={}")

        categorys = json.loads(resp)

        for category_1 in categorys["data"]["cat"]:
            if category_1["title"] != "全部商品":
                self.level_1 = category_1["title"]

                for category_2 in category_1["children"]:
                    self.level_2 = category_2["gfullname"]

                    if category_2["isparent"] is True:
                        for category_3 in category_2["children"]:
                            self.level_3 = category_3["gfullname"]
                            self.get_goods(category_3["gid"], self.level_3)
                    else:
                        self.level_3 = None
                        self.get_goods(category_3["gid"],
                                       category_3["gfullname"])
            else:
                continue
            
        self.workbook.close()


if __name__ == "__main__":
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    DealLk().main()

import requests
import time
import urllib3
import pymysql
import logging
from logging.handlers import RotatingFileHandler
import os
import json


def get_proxy():
    return requests.get("http://127.0.0.1:5010/get/").content


def delete_proxy(proxy):
    # requests.get("http://127.0.0.1:5010/delete/?proxy={}".format(proxy))
    pass


class Deal(object):
    def __init__(self, index=""):
        self.index = index
        self.init_log()
        # self.proxies = False
        # self.proxies = True
        self.init_pool()
        self.url_index = "http://exam.sac.net.cn/pages/registration/train-line-register!orderSearch.action"
        self.headers = {
            "Host":
            "exam.sac.net.cn",
            "Accept":
            "application/json, text/javascript, */*; q=0.01",
            "Origin":
            "http://exam.sac.net.cn",
            "X-Requested-With":
            "XMLHttpRequest",
            "User-Agent":
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.90 Safari/537.36",
            "Content-Type":
            "application/x-www-form-urlencoded",
            "Referer":
            "http://exam.sac.net.cn/pages/registration/sac-publicity-report.html",
            "Accept-Encoding":
            "gzip, deflate",
            "Accept-Language":
            "zh-CN,zh;q=0.9",
            "Cookie":
            "BIGipServergrade=2924587200.20480.0000; JSESSIONID=ZSOIsUcClH6E8hNv8AWYWy5wqJ0HLDg4PSIA8rTQTOH1wS3bTsow!-9023950"
        }
        self.insert_index = """INSERT INTO `sac`.`registration`(`AOI_ID`, `AOI_NAME`, `PR_COUNT_PERSON`, `type`, `PTI0PERSON`, `PTI1PERSON`, `PTI2PERSON`, `PTI3PERSON`, `PTI4PERSON`, `PTI5PERSON`, `PTI6PERSON`, `PTI7PERSON`) VALUES ({},"{}",{},{},{},{},{},{},{},{},{},{});"""
        self.init_mysql()
        self.run()
        self.ecnu_cursor.close()

    def init_mysql(self):
        try:
            ecnu_mysql = pymysql.connect(
                host='127.0.0.1',
                port=3306,
                user='root',
                passwd='shadow',
                database="sac",
                use_unicode=True,
                charset="utf8mb4",
                autocommit=True)
        except pymysql.err.OperationalError as exc:
            print('登录失败！TimeoutError!')
            os._exit(0)
        else:
            self.ecnu_cursor = ecnu_mysql.cursor()

    def init_log(self):

        logger = logging.getLogger(__name__)
        logger.propagate = False
        logger.setLevel(level=logging.INFO)
        if not logger.handlers:
            try:

                handler = RotatingFileHandler(
                    "./log/run_info.log",
                    maxBytes=10 * 1024 * 1024,
                    backupCount=100)
                # handler = loggingFileHandler("./log/run_info.log")
            except FileNotFoundError as exc:
                os.makedirs("./log/")
                self.init_log()
                return
            handler.setLevel(logging.WARNING)
            formatter = logging.Formatter(
                '%(asctime)s - %(funcName)s - %(levelname)s - %(message)s')
            handler.setFormatter(formatter)

            console = logging.StreamHandler()
            console.setLevel(logging.WARNING)

            logger.addHandler(handler)
            logger.addHandler(console)

        self.logger = logger

    def init_pool(self):
        proxyHost = "http-dyn.abuyun.com"
        proxyPort = "9020"
        # 代理隧道验证信息
        proxyUser = "H23W005A02J5V10D"
        proxyPass = "5FDF530C49CD925F"

        proxyMeta = "http://%(user)s:%(pass)s@%(host)s:%(port)s" % {
            "host": proxyHost,
            "port": proxyPort,
            "user": proxyUser,
            "pass": proxyPass,
        }

        self.proxies = {
            "http": proxyMeta,
            "https": proxyMeta,
        }

    def get_session(self):
        """创建 session 示例，以应对多线程"""

        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

        # 设置重连次数
        requests.adapters.DEFAULT_RETRIES = 120
        # 设置连接活跃状态为False
        session = requests.session()
        session.keep_alive = False
        session.verify = False

        adapter = requests.adapters.HTTPAdapter(max_retries=30)
        # 将重试规则挂载到http和https请求
        session.mount('http://', adapter)
        session.mount('https://', adapter)

        return session

    def deal_re(self, byte=False, need_header=False, **kwargs):
        """requests of get"""

        url = kwargs.get("url")
        header = kwargs.get("header")
        try:
            data = kwargs.get("data")
        except:
            data = None

        sesscion_a = self.get_session()

        # print("---> 开始请求网址：{}".format(url))
        self.logger.info("---> 开始请求网址：{}".format(url))
        start_time = time.time()
        retry_count = 5
        while retry_count > 0:
            if self.proxies:
                try:
                    try:
                        if not data:
                            resp = sesscion_a.get(
                                url,
                                headers=header,
                                timeout=(2, 8),
                                allow_redirects=False,
                                proxies=self.proxies)
                        else:
                            # proxy = get_proxy()
                            # if type(proxy) != str:
                            #     proxy = str(get_proxy(), encoding='utf-8')
                            # if proxy == "no proxy!":
                            #     raise ValueError("no proxy")
                            # else:
                            #     # print("the proxy is {}".format(proxy))
                            #     pass
                            resp = sesscion_a.post(
                                url,
                                headers=header,
                                data=data,
                                timeout=(2, 8),
                                # proxies={"http": "http://{}".format(proxy)})
                                proxies=self.proxies)
                        if resp.status_code != 200:
                            print("It's {} now".format(resp.status_code))
                            time.sleep(0.5)
                            retry_count -= 1
                            # if retry_count == 0:
                            #     delete_proxy(proxy)
                            #     print("---> 0: 删除代理")
                        # elif "过于频繁" in resp.text or "稍后再试" in resp.text:
                        #     delete_proxy(proxy)
                        #     retry_count -= 1
                        #     print("---> 1: 删除代理")
                        else:
                            retry_count = 0
                    except Exception as exc:
                        self.logger.error(
                            "---> The error is {}, and the website is {}. Now try again just one time."
                            .format(exc, url))
                        # delete_proxy(proxy)
                        # print("---> 3: 删除代理")
                        retry_count -= 1

                except ValueError as exc:
                    retry_count -= 1
                    try:
                        if not data:
                            resp = sesscion_a.get(
                                url, headers=header, timeout=(2, 8))
                        else:
                            resp = sesscion_a.post(
                                url, headers=header, data=data, timeout=(2, 8))
                    except Exception as exc:
                        self.logger.error(
                            "---> The error is {}, and the website is {}. Now try again just one time."
                            .format(exc, url))
                        self.deal_re(url=url, header=header, data=data)
            else:
                try:
                    if not data:
                        resp = sesscion_a.get(
                            url,
                            headers=header,
                            allow_redirects=False,
                            timeout=(2, 8))
                    else:
                        resp = sesscion_a.post(
                            url, headers=header, data=data, timeout=(2, 8))
                    retry_count = 0
                except Exception as exc:
                    retry_count -= 1
                    self.logger.error(
                        "---> The error is {}, and the website is {}. Now try again just one time."
                        .format(exc, url))
                    self.deal_re(url=url, header=header, data=data)

        end_time = time.time()

        try:
            if resp.status_code == 200:
                magic_time = end_time - start_time
                self.logger.info(
                    "--->Info: Request successful. It takes {:.3} seconds".
                    format(magic_time))
                return resp
            elif resp.status_code == 302:
                return resp.headers
            else:
                self.logger.error("--->Info {} 请求失败！状态码为{}，共耗时{:.3}秒".format(
                    url, resp.status_code, end_time - start_time))
        except UnboundLocalError as exc:
            self.logger.error(
                "--->Error: deal re is error, the error is {}".format(exc))
            return None

    def get_registration(self):
        data = {
            "filter_EQS_OTC_ID": "10",
            "ORDERNAME": "AOI#AOI_NAME",
            "ORDER": "ASC",
            "sqlkey": "registration",
            "sqlval": "SELECT_LINE_PERSON"
        }
        for index in range(10, 15):
            data["filter_EQS_OTC_ID"] = str(index)
            resp = self.deal_re(
                url=self.url_index, header=self.headers, data=data)
            info_ = json.loads(resp.text)
            for value in info_:
                a = self.insert_index.format(
                    value["AOI_ID"], value["AOI_NAME"],
                    value["PR_COUNT_PERSON"], index, value["PTI0PERSON"],
                    value["PTI1PERSON"], value["PTI2PERSON"],
                    value["PTI3PERSON"], value["PTI4PERSON"],
                    value["PTI5PERSON"], value["PTI6PERSON"],
                    value["PTI7PERSON"])
                self.ecnu_cursor.execute(
                    self.insert_index.format(
                        value["AOI_ID"], value["AOI_NAME"],
                        value["PR_COUNT_PERSON"], index, value["PTI0PERSON"],
                        value["PTI1PERSON"], value["PTI2PERSON"],
                        value["PTI3PERSON"], value["PTI4PERSON"],
                        value["PTI5PERSON"], value["PTI6PERSON"],
                        value["PTI7PERSON"]))

    def get_person_info(self):
        self.ecnu_cursor.execute("SELECT  AOI_ID FROM sac.registration;")
        sql_data = self.ecnu_cursor.fetchall()
        for _ in sql_data:
            for index in _:
                # index = 1999088
                self.headers[
                    "Referer"] = "http://exam.sac.net.cn/pages/registration/sac-publicity-finish.html?aoiId={}".format(
                        index)
                data = {
                    "filter_EQS_AOI_ID": "".format(index),
                    "filter_EQS_PTI_ID": "",
                    "page.searchFileName": "homepage",
                    "page.sqlKey": "PAGE_FINISH_PUBLICITY",
                    "page.sqlCKey": "SIZE_FINISH_PUBLICITY",
                    "_search": "false",
                    "nd": "".format(int(time.time())),
                    "page.pageSize": "270000",
                    "page.pageNo": "1",
                    "page.orderBy": "id",
                    "page.order": "desc"
                }
                resp = self.deal_re(
                    url=
                    "http://exam.sac.net.cn/pages/registration/train-line-register!list.action",
                    header=self.headers,
                    data=data)
                count = 0
                with open("./data/info.json", "w", encoding="utf-8") as fn:
                    fn.write(
                        json.dumps(
                            json.loads(resp.text),
                            ensure_ascii=False,
                            indent=4))
                for value in json.loads(resp.text)["result"]:
                    self.ecnu_cursor.execute(
                        "INSERT INTO `sac`.`person_info`(`AOI_NAME`, `CER_NUM`, `COUNTCER`, `COUNTCX`, `CTI_NAME`, `ECO_NAME`, `PPP_END_DATE`, `PPP_GET_DATE`, `PPP_ID`, `PTI_NAME`, `RNUM`, `RPI_NAME`, `SCO_NAME`) VALUES (\"{}\", \"{}\", {}, \"{}\", \"{}\", \"{}\", \"{}\", \"{}\", \"{}\", \"{}\", {}, \"{}\", \"{}\");"
                        .format(value["AOI_NAME"], value["CER_NUM"],
                                value["COUNTCER"], value["COUNTCX"],
                                value["CTI_NAME"], value["ECO_NAME"],
                                value["PPP_END_DATE"], value["PPP_GET_DATE"],
                                value["PPP_ID"], value["PTI_NAME"],
                                value["RNUM"], value["RPI_NAME"],
                                value["SCO_NAME"]))
                    count += 1
                print(count)
                break
            break

    def get_rpi_id(self):
        self.ecnu_cursor.execute(
            "SELECT `PPP_ID` FROM `sac`.`person_info` WHERE `id` = {} LIMIT 1;"
            .format(self.index))
        self.ppp_id = self.ecnu_cursor.fetchone()[0]
        self.headers[
            "Referer"] = "http://exam.sac.net.cn/pages/registration/sac-finish-person.html?r2SS_IFjjk={}".format(
                self.ppp_id)
        data = {
            "filter_EQS_PPP_ID": "",  # self.ppp_id,  # 传空可取全部
            "sqlkey": "registration",
            "sqlval": "SD_A02Leiirkmuexe_b9ID"
        }
        resp = self.deal_re(
            url=
            "http://exam.sac.net.cn/pages/registration/train-line-register!gsUDDIsearch.action",
            header=self.headers,
            data=data)
        with open("./data/id.json", "w", encoding="utf-8") as fn:
            fn.write(
                json.dumps(
                    json.loads(resp.text), ensure_ascii=False, indent=4))
        # info_ = json.loads(resp.text)[0]["RPI_ID"]
        # return json.loads(resp.text)[0]["RPI_ID"]
        self.rpi_id = json.loads(resp.text)[0]["RPI_ID"]

    def get_certificate(self):
        data = {
            "filter_EQS_RH#RPI_ID": self.rpi_id,
            "sqlkey": "registration",
            "sqlval": "SEARCH_LIST_BY_PERSONWWCX"
        }
        # 'INSERT INTO `sac`.`person_detail`(`filter_EQS_RPI_ID`, `PPP_ID`, `ADI_ID`, `ADI_NAME`, `AOI_ID`, `AOI_NAME`, `ARRIVE_DATE`, `CER_NUM`, `CERTC_ID`, `CERTC_NAME`, `ECO_NAME`, `OBTAIN_DATE`, `PTI_NAME`, `RPI_NAME`, `RPI_PHOTO_PATH`, `SCO_NAME`, `certificate`) VALUES (034597, "8C02E3883DF8180EE053D651A8C079EE", 42239, "宁波彩虹南路证券营业部", 1999082, "爱建证券有限责任公司", "2019-12-31", "S0820100010020", "00", "None", "本科", "2004-04-09", "一般证券业务", "杨博文", "20080102/registrationRpInfo/136386182285344993.jpg", "男", [{"AOI_NAME":"爱建证券有限责任公司","PTI_NAME":"一般证券业务","CER_NUM":"S0820100010020","OBTAIN_DATE":"2004-04-09","CERTC_NAME":"正常","OPER_DATE":null}]);'
        resp = self.deal_re(
            url=
            "http://exam.sac.net.cn/pages/registration/train-line-register!gsUDDIsearch.action",
            header=self.headers,
            data=data)
        return resp.text

    def get_person_detail(self):
        # self.get_rpi_id()

        data = {
            "filter_EQS_RPI_ID": self.rpi_id,
            "sqlkey": "registration",
            "sqlval": "SELECT_PERSON_INFO"
        }
        resp = self.deal_re(
            url=
            "http://exam.sac.net.cn/pages/registration/train-line-register!gsUDDIsearch.action",
            header=self.headers,
            data=data)
        # a = json.loads(resp.text)
        info_ = json.loads(resp.text)[0]
        self.ppp_id = "None"
        self.ecnu_cursor.execute(
            "INSERT INTO `sac`.`person_detail`(`filter_EQS_RPI_ID`, `PPP_ID`, `ADI_ID`, `ADI_NAME`, `AOI_ID`, `AOI_NAME`, `ARRIVE_DATE`, `CER_NUM`, `CERTC_ID`, `CERTC_NAME`, `ECO_NAME`, `OBTAIN_DATE`, `PTI_NAME`, `RPI_NAME`, `RPI_PHOTO_PATH`, `SCO_NAME`, `certificate`) VALUES (\"{}\", \"{}\", \"{}\", \"{}\", \"{}\", \"{}\", \"{}\", \"{}\", \"{}\", \"{}\", \"{}\", \"{}\", \"{}\", \"{}\", \"{}\", \"{}\", '{}');"
            .format(self.rpi_id, self.ppp_id, info_["ADI_ID"],
                    info_["ADI_NAME"], info_["AOI_ID"], info_["AOI_NAME"],
                    info_["ARRIVE_DATE"], info_["CER_NUM"], info_["CERTC_ID"],
                    info_["CERTC_NAME"], info_["ECO_NAME"],
                    info_["OBTAIN_DATE"], info_["PTI_NAME"], info_["RPI_NAME"],
                    info_["RPI_PHOTO_PATH"], info_["SCO_NAME"],
                    self.get_certificate()))

    def run(self):
        # self.get_registration()
        # self.get_person_info()
        # self.get_rpi_id()
        self.rpi_id = self.index
        # self.get_person_detail()
        try:
            self.get_person_detail()
        except Exception as exc:
            print(exc)


        # for index in range(2, 260732):
        #     self.index = index
        #     self.get_person_detail()
def get_id():
    will_get = []
    with open("./data/id.json", "r", encoding="utf-8") as fn:
        ids = json.loads(fn.read())

    for value in ids:
        will_get.append(value['RPI_ID'])

    for index in will_get:
        yield index


def multi_query(processes=10):
    from multiprocessing import Process, Queue, Pool, freeze_support

    pool = Pool(processes)

    # for index in range(238, 260732):
    #     try:
    #         pool.apply_async(Deal, (index, ))
    #     except Exception as exc:
    #         print(exc)
    yield_id = get_id()

    while True:
        try:
            pool.apply_async(Deal, (next(yield_id), ))
        except StopIteration:
            yield_id.close()
            break
        except Exception as exc:
            print(exc)

    pool.close()
    pool.join()


def main():
    # a = get_id()
    # while True:
    #     print(next(a))
    # yield_id = get_id()
    # Deal(next(yield_id))
    multi_query(5)


if __name__ == "__main__":
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    main()
import time
import pymysql

from bs4 import BeautifulSoup

from request import Query

DEBUG = True


def timer(func):
    '''
    @summary: cal the time of the fucntion
    @param : None
    @return: return the res of the func
    '''

    def wrapper(*args, **kw):
        start_time = time.time()
        # start_time = datetime.datetime.now()
        res = func(*args, **kw)
        over_time = time.time()
        # over_time = datetime.datetime.now()
        print('current Function {0} run time is {1}'.format(
            func.__name__, over_time - start_time))
        # print ('current Function {0} run time is {1}'.format(func.__name__ , (over_time - start_time).total_seconds()))
        return res

    return wrapper


@timer
class DealCicpa(object):
    @timer
    def __init__(self):
        self.path = "http://www.whalebj.com/xzjc/"

        self.header = {
            "Host": "www.whalebj.com",
            "Cache-Control": "max-age=0",
            "Upgrade-Insecure-Requests": "1",
            "User-Agent":
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.90 Safari/537.36",
            "Accept":
            "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3",
            "Accept-Encoding": "gzip, deflate",
            "Accept-Language": "zh-CN,zh;q=0.9",
        }
        self.insert_sql = "INSERT INTO `workoo`.`whalebj`(`time`, `num`, `in`, `leave`) VALUES ('{}', '{}', '{}', '{}');"
        self.request = Query()
        self.init_sql()

    @timer
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

    @timer
    def remove_character(self, content):
        if isinstance(content, str):
            return content.replace("；", "")
            # .replace("辆","").replace("；","")
    @timer
    def main(self):
        resp = self.request.run(self.path, header=self.header)

        start_time = time.time()
        soup = BeautifulSoup(resp, "lxml")
        obj_list = soup.find(attrs={"id": "Label_Msg"}).contents
        over_time = time.time()
        print(' {0} run time is {1}'.format("soup", over_time - start_time))

        start_time = time.time()
        for item in obj_list:
            if isinstance(item, str):
                if "：" in item:
                    key, value = item.split("：")[0], item.split("：")[-1]
                    if "场内待运车辆数" in key:
                        num = self.remove_character(value)
                    elif "前半小时进场车辆数" in key:
                        in_ = self.remove_character(value)
                    elif "前半小时离场车辆数" in key:
                        leave = self.remove_character(value)
                elif "截止目前为止" in item:
                    time_ = item.split("（")[-1].replace("）", "")

        over_time = time.time()
        print(' {0} run time is {1}'.format("for", over_time - start_time))

        start_time = time.time()
        self.ecnu_cursor.execute(
            self.insert_sql.format(time_, num, in_, leave))
        over_time = time.time()
        print(' {0} run time is {1}'.format("sql", over_time - start_time))

    @timer
    def run(self):
        # while True:
            # try:
        start_time = time.time()
        self.main()
        over_time = time.time()
        print(' {0} run time is {1}'.format("main", over_time - start_time))
            # except Exception as exc:
            #     print("--->Info: the error is {}".format(exc))
        time.sleep(58)


if __name__ == "__main__":
    DealCicpa().run()
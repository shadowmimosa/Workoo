import logging
import requests
import urllib3
import time
from logging.handlers import RotatingFileHandler


class Query(object):
    def __init__(self):
        self.init_log()
        self.proxies = False
        self.page = 1
        self.url = "http://api.bilibili.com/x/reply?type=1&oid={}&pn={}&nohot=1&sort=0"
        self.headers = {
            "Host": "checkcoverage.apple.com",
            "Upgrade-Insecure-Requests": "1",
            "User-Agent":
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36",
            "Accept":
            "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "zh-CN,zh;q=0.9"
        }

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
            handler.setLevel(logging.ERROR)
            formatter = logging.Formatter(
                '%(asctime)s - %(funcName)s - %(levelname)s - %(message)s')
            handler.setFormatter(formatter)

            console = logging.StreamHandler()
            console.setLevel(logging.WARNING)

            logger.addHandler(handler)
            logger.addHandler(console)

        self.logger = logger

    def get_session(self):
        """创建 session 示例，以应对多线程"""

        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

        # 设置重连次数
        requests.adapters.DEFAULT_RETRIES = 60
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
                                timeout=(2, 6),
                                allow_redirects=False,
                                proxies=self.proxies)
                        else:
                            resp = sesscion_a.post(
                                url,
                                headers=header,
                                data=data,
                                timeout=(2, 6),
                                proxies=self.proxies)
                        retry_count = 0
                    except Exception as exc:
                        self.logger.error(
                            "---> The error is {}, and the website is {}. Now try again just one time."
                            .format(exc, url))
                        retry_count -= 1

                except ValueError as exc:
                    retry_count -= 1
                    try:
                        if not data:
                            resp = sesscion_a.get(
                                url, headers=header, timeout=(2, 6))
                        else:
                            resp = sesscion_a.post(
                                url, headers=header, data=data, timeout=(2, 6))
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
                            timeout=(2, 6))
                    else:
                        resp = sesscion_a.post(
                            url, headers=header, data=data, timeout=(2, 6))
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

    def spider_main(self, avid):
        resp = self.deal_re(
            url=self.url.format(avid, self.page),
            headers={
                "User-Agent":
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.140 Safari/537.36 Edge/17.17134",
                "Accept-Language":
                "zh-Hans-CN,zh-Hans;q=0.8,en-IE;q=0.5,en;q=0.3",
                "Accept":
                "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
                "Upgrade-Insecure-Requests": "1",
                "Accept-Encoding": "gzip, deflate",
                "Host": "api.bilibili.com",
            })
        print(resp)

def main():
    q = Query()
    for index in range(23828478,23828479):
        q.spider_main(index)

if __name__ == "__main__":
    main()
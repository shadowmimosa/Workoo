import requests
import urllib3
import time
import sys
import random
import os
import json
import hashlib
import logging
from logging.handlers import RotatingFileHandler


def get_bookid():
    bookid_list = [
        "57593", "6693", "14892", "15023", "6780", "13305", "52047", "52052",
        "58843", "58842", "58844", "58847", "58845", "52075", "52048", "52054",
        "52072", "52073", "52050", "52076", "52057", "52074", "57214", "27529",
        "24031", "57265", "57269", "61885", "61737", "52647", "59632", "6511",
        "15027", "5814", "15022", "63881", "15019", "60757", "54717", "15026",
        "60865", "53042", "64229", "6444", "15025", "6473", "59849", "6264",
        "62177", "60895", "59414", "15021", "17832", "51572", "59850", "15024",
        "64027", "6503", "60061", "5813", "6438", "60785", "15028", "51485",
        "10063", "60127", "53470", "59906", "55518", "6500", "51576", "50313",
        "51143", "15020", "61829", "6793", "36185", "53698", "15140", "37594",
        "59772", "52624", "10068", "59392", "11595", "52622", "11441", "10069",
        "25819", "11116", "15133", "52611", "6514", "52618", "6591", "6616",
        "37596", "52143", "18014", "41658", "10065", "25793", "7642", "10067",
        "25805", "6588", "17902", "39639", "63925", "64259", "63889", "64247",
        "63947", "63887", "64391", "64553", "64429", "64249", "63923", "58997",
        "64659", "64045", "64787", "64251", "64243", "64263", "64669", "63951",
        "63891", "64805", "64261", "64777", "64557", "62487", "64237", "64325",
        "64265", "63943", "64699", "64389", "64051", "64059", "64373", "64231",
        "64571", "64647", "64661", "64583", "64609", "64387", "64241", "64371",
        "64683", "63939", "63885", "63917", "64245", "64385", "63105", "62951",
        "62905", "63027", "62895", "63599", "63137", "63117", "63107", "63119",
        "63995", "63141", "63121", "63609", "63115", "63999", "63113", "63145",
        "63971", "63607", "62893", "62987", "63011", "62971", "63099", "62923",
        "63043", "63989", "62959", "63603", "64007", "62943", "63109", "64003",
        "62999", "63053", "64009", "63021", "62995", "62891", "63993", "63111",
        "62899", "62889", "63073", "63097", "62933", "63047", "63005", "63991",
        "10059", "42324", "25639", "6280", "60815", "18488", "6269", "13851",
        "25635", "6281", "13722", "25641", "5591", "18012", "18020", "42254",
        "6332", "6282", "6456", "6257", "5624", "59366", "18074", "60565",
        "13852", "11507", "8377", "60120", "18026", "6474", "18700", "45588",
        "58562", "6289", "8533", "6268", "13027", "58567", "18048", "59763",
        "18040", "59591", "47386", "18062", "49435", "60106", "60765", "49864",
        "60845", "59136", "59048", "49433", "5659", "59463", "49460", "44932",
        "31175", "59349", "57919", "39001", "59062", "49189", "63893", "63799",
        "59110", "63785", "49188", "59708", "59753", "60767", "60645", "58110",
        "49191", "7430", "59688", "59852", "60439", "54042", "60777", "57656",
        "54055", "49440", "59131", "49478", "56609", "51512", "49192", "59692",
        "49445", "49438", "60683", "49443", "60577", "43963", "36785", "59683",
        "5310", "53876", "59401", "13651", "54112", "42036", "57614", "59430",
        "59301", "18042", "54049", "44381", "6288", "6774", "59354", "59636",
        "47518", "51216", "58222", "56081", "59690", "59379", "59469", "55297",
        "25301", "45532", "14104", "49479", "37419", "14417", "47384", "47338",
        "14179", "59840", "14112", "46767", "14198", "14159", "14234", "57548",
        "40066", "48692", "47118", "48687", "41315", "48911", "14253", "14164",
        "14297", "14447", "57014", "49455", "14534", "14345", "14377", "43403",
        "56053", "37231", "55223", "54088", "56068", "43663", "63621", "44563",
        "12994", "46903", "59657", "46584", "43897", "56071", "11396", "51715",
        "43627", "43899", "59860", "62317", "24919", "54867", "37234", "43161",
        "54852", "54949", "34717", "25117", "35597", "35023", "54913", "38491",
        "25091", "37108", "34747", "58077", "58011", "25151", "24843", "43155",
        "36693", "24891", "25119", "25087", "38776", "24695", "24699", "56206",
        "36690", "24685", "54849", "24839", "34775", "56192", "24965", "37340",
        "56213", "37352", "36718", "34999", "24931", "34711", "36687", "53742",
        "36692", "25357", "47549", "54254", "35467", "41040", "41480", "28085",
        "15199", "5532", "14071", "53438", "39243", "14829", "18662", "18670",
        "13858", "13765", "13763", "18822", "25935", "17736", "18852", "17738",
        "14825", "18638", "13767", "25937", "18728", "18642", "18644", "13764",
        "18836", "18630", "13846", "17734", "48678", "13847", "18834", "18636",
        "13862", "57279", "18666", "13739", "54257", "18628", "13741", "13768",
        "18656", "14748", "25939", "10407", "13861", "13837", "18826", "13845",
        "18080", "25967", "14070", "13838", "14757", "18632", "13738", "18322",
        "15184", "39211", "46763", "14113", "47620", "24655", "38730", "57025",
        "36334", "5469", "49956", "6502", "40176", "44997", "57311", "35389",
        "39210", "15185", "36281", "61293", "38198", "18334", "41500", "14384",
        "59776", "18336", "14373", "13695", "47453", "9158", "13696", "13697",
        "13855", "13691", "47472", "14196", "18686", "39847", "18694", "18710",
        "18730", "18716", "16943", "36027", "18690", "38737", "41600", "12754",
        "13693", "17868", "34451", "22256", "24657", "18708", "18714", "22260",
        "47796", "33439", "52358", "13685", "18724", "18706", "13687", "39102",
        "59360", "16959", "14062", "17872", "22486", "29459", "18702", "42293",
        "18688", "38756", "42323", "18000", "22444", "14432", "50349", "36162",
        "14189", "18024", "22396", "52218", "50426", "42318", "22440", "47536",
        "18308", "57260", "25667", "14148", "50355", "39269", "8399", "22448",
        "57266", "36421", "40103", "57309", "22446", "11407", "54080", "22438",
        "50427", "55049", "18018", "42051", "42315", "57280", "50574", "42319",
        "15491", "39175", "50351", "7161", "36164", "24319", "40494", "18892",
        "24725", "18570", "33797", "10054", "9117", "49754", "59316", "33801",
        "5528", "48305", "18572", "24667", "18664", "24713", "18574", "54351",
        "18840", "8577", "17332", "6283", "40476", "40672", "22428", "41437",
        "33791", "5603", "6272", "18668", "14188", "48296", "8576", "52983",
        "59319", "33795", "5584", "48318", "49117", "41592", "18634", "45750",
        "7133", "24687", "26295", "48309", "59320", "41595", "48312", "11628",
        "9103", "12205", "47485", "22474", "39979", "14532", "39880", "36022",
        "14266", "14530", "12670", "17878", "12203", "14321", "41421", "11406",
        "14524", "20008", "14226", "39982", "58429", "6498", "17688", "45600",
        "36021", "12493", "6318", "14527", "58425", "26643", "24049", "14528",
        "5260", "22476", "27817", "11415", "10064", "18986", "11629", "48143",
        "38727", "28073", "47213", "36130", "28967", "42053", "30299", "55206",
        "47208", "18044", "36139", "25897", "39446", "47878", "13857", "49823",
        "30275", "15032", "42276", "54708", "47218", "39306", "33689", "47216",
        "18674", "39296", "36134", "36135", "25905", "47207", "43455", "44437",
        "47561", "18576", "7768", "39449", "25921", "30297", "54299", "39448",
        "35487", "54704", "43659", "47211", "36138", "25893", "33681", "14411",
        "39445", "15031", "36136", "50354", "12681", "50405", "14257", "15224",
        "35865", "25697", "48239", "25677", "35873", "39455", "36416", "11999",
        "6590", "19322", "59329", "12686", "25675", "6656", "8049", "25679",
        "12687", "35864", "12680", "18310", "36420", "59323", "12553", "59336",
        "39104", "35874", "7091", "36092", "35871", "10035", "11961", "35997",
        "16995", "36417", "35863", "39457", "48682", "39458", "14348", "12683",
        "36422", "11994", "36094", "49077"
    ]
    for value in bookid_list:
        yield value


class Query(object):
    def __init__(self, x=10000, y=11000):
        self.init_log()
        self.getdata_url = "https://www.getepic.com/webapi/index.php?class=WebBook&method=getFullDataForWeb&bookId={}&dev=web"
        self.getdata_header = {
            "Host":
            "www.getepic.com",
            "Accept":
            "application/json, text/plain, */*",
            "User-Agent":
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36",
            "Referer":
            "https://www.getepic.com/app/",
            "Accept-Encoding":
            "gzip, deflate, br",
            "Accept-Language":
            "zh-CN,zh;q=0.9",
            "Cookie":
            "__cfduid=dfed48779989ef58e6599bbc3eda03ab81559109882; PHPSESSID=0adtbeobbjbpbn9ulrnq7v09h3; __stripe_mid=b5724726-5f81-4d1d-8b40-dbf184dceb2f; _ga=GA1.2.505693845.1559112691; PHPSESSID=0adtbeobbjbpbn9ulrnq7v09h3; epic_session=36e81a94-e5f9-4f19-94c7-3f3ab189c329%3Ab225f31a01f2c15816cb5ef60b1afd55; _gid=GA1.2.2114200151.1559222467; _fbp=fb.1.1559222480190.1343861901; __stripe_sid=f4a470c5-6361-47b5-97ff-dc7de5574f73"
        }
        self.media_url = "https://cdn.getepic.com//{}?ttl={}&token={}"
        self.pic_cover_url = "https://cdn.getepic.com/drm/2/8822/cover.jpg"
        self.media_header = {
            "Host":
            "cdn.getepic.com",
            "User-Agent":
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36",
            "Accept":
            "image/webp,image/apng,image/*,*/*;q=0.8",
            "Referer":
            "https://www.getepic.com/app/read/{}",
            "Accept-Encoding":
            "gzip, deflate, br",
            "Accept-Language":
            "zh-CN,zh;q=0.9",
            "Cookie":
            "__cfduid=dfed48779989ef58e6599bbc3eda03ab81559109882; _ga=GA1.2.505693845.1559112691; PHPSESSID=0adtbeobbjbpbn9ulrnq7v09h3; epic_session=36e81a94-e5f9-4f19-94c7-3f3ab189c329%3Ab225f31a01f2c15816cb5ef60b1afd55; _gid=GA1.2.2114200151.1559222467; _fbp=fb.1.1559222480190.1343861901; _gat=1"
        }

        if sys.platform == "win32":
            self.proxies = False
            # self.init_pool()
        else:
            self.init_pool()
        self.detail_path = "./data/index/{}.json"
        self.info_path = "./data/books/{}/info.json"
        self.media_path = "./data/books/{}/{}/{}.{}"
        self.x = x
        self.y = y
        self.timestamp = self.format_timestamp()
        self.run()

    def init_log(self):

        logger = logging.getLogger(__name__)
        logger.setLevel(level=logging.INFO)
        # try:

        #     handler = RotatingFileHandler(
        #         "./log/run_info.log", maxBytes=1024 * 1024, backupCount=3)
        #     # handler = loggingFileHandler("./log/run_info.log")
        # except FileNotFoundError as exc:
        #     os.makedirs("./log/")
        #     self.init_log()
        #     return
        # handler.setLevel(logging.INFO)
        # formatter = logging.Formatter(
        #     '%(asctime)s - %(funcName)s - %(levelname)s - %(message)s')
        # handler.setFormatter(formatter)

        console = logging.StreamHandler()
        console.setLevel(logging.ERROR)

        # logger.addHandler(handler)
        logger.addHandler(console)

        self.logger = logger

    def init_pool(self):
        proxyHost = "http-dyn.abuyun.com"
        proxyPort = "9020"
        # 代理隧道验证信息
        proxyUser = "H23W005A02J5V10D"
        proxyPass = "CB31E09182BA20C4"

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

    def deal_re(self, byte=False, **kwargs):
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
                                timeout=(3.2, 10),
                                proxies=self.proxies)
                        else:
                            resp = sesscion_a.post(
                                url,
                                headers=header,
                                data=data,
                                timeout=(3.2, 10),
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
                                url, headers=header, timeout=(3.2, 30))
                        else:
                            resp = sesscion_a.post(
                                url,
                                headers=header,
                                data=data,
                                timeout=(3.2, 30))
                    except Exception as exc:
                        self.logger.error(
                            "---> The error is {}, and the website is {}. Now try again just one time."
                            .format(exc, url))
                        self.deal_re(url=url, header=header, data=data)
            else:
                try:
                    if not data:
                        resp = sesscion_a.get(
                            url, headers=header, timeout=(3.2, 30))
                    else:
                        resp = sesscion_a.post(
                            url, headers=header, data=data, timeout=(3.2, 30))
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
                if byte:
                    return resp.content
                else:
                    return resp.text
            elif resp.status_code == 401:
                self.logger.warning(
                    "--->Warning: Retrying because error code 401")
                resp = self.deal_re(
                    byte=byte, url=url, header=header, data=data)
            elif resp.status_code == 503:
                print(resp.text)
            else:
                self.logger.error("--->Info {} 请求失败！状态码为{}，共耗时{:.3}秒".format(
                    url, resp.status_code, end_time - start_time))
        except UnboundLocalError as exc:
            self.logger.error(
                "--->Error: deal re is error, the error is {}".format(exc))
            return None

    def format_timestamp(self):
        return int(time.time())

    def get_timestamp(self):
        if self.format_timestamp() - self.timestamp > 600:
            self.timestamp = self.format_timestamp()
        return self.timestamp

    def make_token(self):
        raw_str = "/{}?ttl={}&auth=4fc6f017797e20e3933800968d99bb73".format(
            self.asset_path, self.expire)
        md5 = hashlib.md5()
        md5.update(raw_str.encode("utf-8"))
        return md5.hexdigest()

    def get_info(self):
        resp = self.deal_re(
            url=self.getdata_url.format(self.bookid),
            header=self.getdata_header)
        try:
            data = json.loads(resp)
        except TypeError as exc:
            self.book_detail = None
            if exc == "the JSON object must be str, bytes or bytearray, not NoneType":
                self.logger.error(
                    "---> Error: The format of the response does not match")
        finally:
            self.book_detail = data["result"]
            if self.book_detail == None:
                self.logger.info("---> Info: Book Id is wrong")
            else:
                self.save_detail()
                # self.save_info() # 改为，有音频的才下载

    def get_media(self):
        self.expire = self.get_timestamp()
        media_url = self.media_url.format(self.asset_path, self.expire,
                                          self.make_token())
        self.media_header["Referer"] = self.media_header["Referer"].format(
            self.bookid)
        resp = self.deal_re(byte=True, url=media_url, header=self.media_header)

        self.save_media(resp)

    def spider_main(self):
        self.get_info()
        time.sleep(random.randint(2, 5))
        return  # 先下载 detail
        if self.book_detail:
            self.has_audio = (True if (
                self.book_detail["userBook"]["book"]["audio"] == 1) else None)
            self.spine = self.book_detail["epub"]["spine"]
            if self.has_audio:
                keywords = ["page", "audio"]
                self.save_info()
            else:
                self.logger.info("--->Info: Not audio, return now")
                return
                keywords = ["page"]

            for value in self.spine:
                for keyword in keywords:
                    try:
                        self.asset_path = value.get(keyword)
                    except Exception as exc:
                        print("Error: {}".format(exc))
                    finally:
                        if self.asset_path:
                            self.get_media()
                        else:
                            self.logger.info(
                                "--->Info: The {} not found".format(keyword))

    def run(self):
        if self.x == self.y:
            if os.path.exists("./data/index/{}".format(self.x)):
                return
            else:
                self.bookid = self.x
                self.pic_count = -1
                while True:
                    try:
                        self.spider_main()
                        break
                    except:
                        continue
        else:
            for index in range(self.x, self.y):
                if os.path.exists("./data/books/{}".format(index)):
                    continue
                else:
                    self.bookid = index
                    self.pic_count = -1
                    self.spider_main()

    def save_detail(self):
        if os.path.exists(self.detail_path.format(self.bookid)):
            self.logger.error("exists already, pass")
        else:
            try:
                with open(
                        self.detail_path.format(self.bookid),
                        "w",
                        encoding="utf-8") as fn:
                    fn.write(json.dumps(self.book_detail, indent=4))
                self.logger.error("save detail now")
            except FileNotFoundError as exc:
                self.logger.warning(
                    "---> Warning: The file path can't found, building it now")
                os.makedirs(self.detail_path.replace("{}.json", ""))
                self.save_detail()

    def extract_info(self):
        self.book_info = {
            "title": self.book_detail['book']['title'],
            "author": self.book_detail['book']['author'],
            "bookDescription": self.book_detail['book']['bookDescription'],
            "avgTime": self.book_detail['book']['avgTime'],
            "lexile": self.book_detail['book']['lexile'],
            "ar": self.book_detail['book']['ar']
        }

    def save_info(self):
        try:
            with open(
                    self.info_path.format(self.bookid), "w",
                    encoding="utf-8") as fn:
                self.extract_info()
                fn.write(json.dumps(self.book_info, indent=4))
        except FileNotFoundError as exc:
            self.logger.warning(
                "---> Warning: The file path can't found, building it now")
            os.makedirs(
                self.info_path.format(self.bookid).replace("info.json", ""))
            self.save_info()

    def save_media(self, content):
        sign = self.asset_path.split(".")[-1]

        if sign != "jpg":
            if sign != "mp3":
                self.logger.error("---> Error: File format does not conform")
                with open("./data/error.txt", "w", encoding="utf-8") as fn:
                    fn.write(sign, self.bookid)
                return
        else:
            self.pic_count += 1

        try:
            with open(
                    self.media_path.format(self.bookid, sign, self.pic_count,
                                           sign), "wb") as fn:
                fn.write(content)
        except FileNotFoundError as exc:
            self.logger.warning(
                "---> Warning: The file path can't found, building it now")
            os.makedirs(
                self.media_path.replace("{}.{}", "").format(self.bookid, sign))
            self.save_media(content)

    def read_info(self):
        try:
            with open(
                    self.detail_path.format(self.bookid), "r",
                    encoding="utf-8") as fn:
                self.book_detail = json.loads(fn.read())
        except FileNotFoundError as exc:
            self.logger.warning(
                "---> Warning: The file path can't found, building it now")
            os.makedirs(self.detail_path.replace("{}.json", ""))
            self.read_info()


def single_process():
    """单进程、单线程"""

    yield_id = get_bookid()

    while True:
        try:
            bookid = next(yield_id)
            Query(bookid, bookid)
            time.sleep(random.randint(3, 10))
        except StopIteration:
            yield_id.close()
            break


def get_bookids():
    for index in range(33600, 70000):
        yield index


def multi_processes(processes=10):
    """多进程，默认最多 10 个进程"""

    from multiprocessing import Process, Queue, Pool, freeze_support

    pool = Pool(processes)

    # yield_id = get_bookid()
    yield_id = get_bookids()

    while True:
        try:
            bookid = next(yield_id)
            pool.apply_async(Query, (
                bookid,
                bookid,
            ))
        except StopIteration:
            yield_id.close()
            break

    pool.close()
    pool.join()


def main():
    # Query(10000, 10002)
    # Query(67)
    # single_process()
    multi_processes(30)


def build_sql():
    final = ""
    sql = "UNION ALL SELECT avid, content, time FROM comment_{} "
    for index in range(2, 129):
        final += sql.format(index)

    print(final)


if __name__ == "__main__":
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    build_sql()
    main()

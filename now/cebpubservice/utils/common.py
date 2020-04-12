import os
import sys
import time
import json
import socket
import ftplib
import pymysql
import platform
from urllib.parse import urlparse
from configparser import ConfigParser
from pdf2image import convert_from_path

from utils.baidu_ocr import BaiduOCR


class Myparser(ConfigParser):
    def to_dict(self):
        d = dict(self._sections)
        for k in d:
            d[k] = dict(d[k])
        return d


def get_strftime(timestamps=None):
    if timestamps:
        result = time.strftime('%Y-%m-%d %X', time.localtime(timestamps))
    else:
        result = time.strftime('%Y-%m-%d %X', time.localtime(time.time()))

    return result.split(' ')[0]


def clean_date(content: str):
    return content.replace('T', ' ').replace('.000+0000', '').split(' ')[0]


def filter_host(url):
    if not url:
        return
    res = urlparse(url)
    host = res.netloc

    if host in [
            'e.sinochemitc.com', 'eps.qdgxjt.com', 'eb.chinalco.com.cn',
            'ebid.aecc-mall.com', 'eps.sdic.com.cn', 'ec.ceec.net.cn',
            'www.xaprtc.com', 'bid.aited.cn', 'lygccgpt.gdlygc.cn',
            'ebid.aecc-mall.com', 'www.cqzbcg.com'
    ]:
        return True


def clean_region(content: str):
    for sign in ['省', '市', '自治区', '维吾尔', '回族', '壮族', '特别行政区']:
        content = content.replace(sign, '')
    return content


def parser_trade(title: str, trade: str):
    if not isinstance(trade, str) or trade == '其他':
        trade = '地方公告'

    if not isinstance(title, str):
        title = ''

    replace_list = {
        '内蒙古电力集团': '蒙电',
        '呼和浩特供电局': '蒙电',
        '包头供电局': '蒙电',
        '鄂尔多斯电业局': '蒙电',
        '乌兰察布电业局': '蒙电',
        '巴彦淖尔电业局': '蒙电',
        '乌海电业局': '蒙电',
        '锡林郭勒电业局': '蒙电',
        '阿拉善电业局': '蒙电',
        '薛家湾供电局': '蒙电',
        '内蒙古电力': '蒙电',
        '华能': '华能',
        '大唐': '大唐',
        '国网': '国网',
        '国家电网': '国网',
        '平高集团': '国网',
        '中核 ': '中核',
        '中广核 ': '中广核',
    }

    for key in replace_list:
        if key in title:
            return replace_list.get(key)

    return trade


def pdf2pic(file_path, output_path):
    if DEBUG:
        poppler_path = r'C:\Users\ShadowMimosa\Desktop\poppler-0.68.0\bin'
    else:
        poppler_path = CONFIG.get('PopPath', 'path')
        # poppler_path = None
    convert_from_path(file_path,
                      200,
                      output_path,
                      fmt="jpg",
                      output_file='pic',
                      thread_count=4,
                      poppler_path=poppler_path)

    return output_path
    # images = convert_from_path(file_path)
    # for index, img in enumerate(images):
    #     img.save('%s/page_%s.png' % (output_path, index))


def pic2text(path):
    pic_list = []
    if os.path.isdir(path):
        files = os.listdir(path)
        files.sort(key=lambda x: int(x.split('-')[-1][:-4]))
        for filename in files:
            with open(os.path.join(path, filename), 'rb') as fn:
                pic_list.append(fn.read())
    elif os.path.isfile(path):
        with open(path, 'rb') as fn:
            pic_list.append(fn.read())

    result = []
    for pic in pic_list:
        text = ocr.pic2word(pic)["words_result"]
        texts = '\n'.join([x['words'] for x in text])
        result.append(texts)

    return '\n\n'.join(result)


def img_tag(dirpath):
    result = ''
    tag = '<img src="/image/{}{}"/>'
    files = os.listdir(dirpath)
    files.sort(key=lambda x: int(x.split('-')[-1][:-4]))
    for img in files:
        path = dirpath.split('/pic/')[-1]
        result += tag.format(path, img)

    return result


def create_path(folder, filepath=None):
    """
    根据时间生成新文件目录
    """
    date = time.strftime("%Y-%m-%d")
    if filepath:
        filename = filepath.split('/')[-1].split('.')[0]
        path = f'./static/{folder}/{date}/{filename}/'
    else:
        path = f'./static/{folder}/{date}/'

    os.makedirs(path) if not os.path.exists(path) else True

    return path


from functools import wraps


def ping(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        args[0].ecnu_mysql.ping(reconnect=True)

        return func(*args, **kwargs)

    return wrapper


class MysqlOpea(object):
    def __init__(self, upload=False):
        self.upload = upload
        self.init_sql()
        super().__init__()

    def init_sql(self):
        if self.upload:
            sign = 'DataBaseDev'
        else:
            sign = 'DataBaseLocal'
        mysql = {}
        for key in ['host', 'port', 'user', 'passwd', 'database']:
            mysql[key] = CONFIG.get(sign, key)

        mysql['port'] = int(mysql['port'])
        mysql['use_unicode'] = True
        mysql['autocommit'] = True
        mysql['charset'] = 'utf8mb4'

        self.database = mysql.get('database')

        try:
            self.ecnu_mysql = pymysql.connect(**mysql)
        except pymysql.err.OperationalError as exc:
            print('登录失败！TimeoutError!')
            sys.exit(0)
        else:
            if self.upload:
                self.ecnu_cursor = self.ecnu_mysql.cursor(
                    cursor=pymysql.cursors.DictCursor)
            else:
                self.ecnu_cursor = self.ecnu_mysql.cursor(
                    cursor=pymysql.cursors.DictCursor)

    def escape_param(self, param):
        for key in param:
            value = param[key]
            if isinstance(value, str):
                param[key] = pymysql.escape_string(value)

        return param

    @ping
    def repeat(self, bulletin_id=None):
        sql = 'SELECT id FROM `dd1`.`wy` WHERE `platform` = 1 AND `special` = "{}" LIMIT 1;'.format(
            bulletin_id)
        if self.ecnu_cursor.execute(sql) == 0:
            return True

    @ping
    def select(self):
        if self.upload:
            sql = ''
        else:
            sql = 'SELECT * FROM `dd1`.`wy` WHERE `sync` = 0 LIMIT 10;'
        if self.ecnu_cursor.execute(sql) != 0:
            return self.ecnu_cursor.fetchall()

    @ping
    def update(self, ID):
        sql = f'UPDATE `dd1`.`wy` SET `sync` = 1 WHERE `ID` = {ID};'
        self.ecnu_cursor.execute(sql)
        return True

    @ping
    def insert(self, param: dict):
        # param = {x: pymysql.escape_string(param[x]) for x in param}
        param = self.escape_param(param)
        if self.upload:
            sql = 'INSERT INTO `database`.`wy` ( `fid`, `uid`, `bt`, `url`, `nr`, `w1`, `w2`, `w5`, `g`, `r1`, `r2`) VALUES ( {fid}, 20, "{bt}", "{url}", "{nr}", "{w1}", "{w2}", "{w5}", "{g}", "{r1}", "{r2}" );'
        else:
            sql = 'INSERT INTO `database`.`wy` ( `fid`, `uid`, `bt`, `url`, `nr`, `w1`, `w2`, `w5`, `g`, `r1`, `r2`, `local`, `special`, `platform`) VALUES ( {fid}, 20, "{title}", "{path}", "{img}", "{region}", "{trade}", "{text}", "{source}", "{add_time}", "{notice_time}", "{local}", "{bulletin_id}", 1 );'
        self.ecnu_cursor.execute(
            sql.format(**param).replace('database', self.database))

        return True


class FtpOpea(object):
    def __init__(self):
        super().__init__()

    def connect(self):
        try:
            ftp = ftplib.FTP(CONFIG.get('Ftp', 'host'))
            ftp.login(CONFIG.get('Ftp', 'user'), CONFIG.get('Ftp', 'pwd'))
            self.ftp = ftp
        except (socket.error, socket.gaierror):
            print(
                "FTP is unavailable,please check the host,username and password!"
            )
            sys.exit(0)

    def disconnect(self):
        self.ftp.quit()

    def upload(self, filepath):
        with open(filepath, "rb") as fn:
            file_name = os.path.split(filepath)[-1]
            try:
                self.ftp.storbinary('STOR %s' % file_name, fn,
                                    CONST_BUFFER_SIZE)
            except ftplib.error_perm:
                return False
            return True

    def download(self, filename):
        with open(filename, "wb") as fn:
            try:
                self.ftp.retrbinary("RETR %s" % filename, fn.write,
                                    CONST_BUFFER_SIZE)
            except ftplib.error_perm:
                return False
            return True

    def list_dir(self):
        return self.ftp.dir()

    def find(self, filename):
        ftp_f_list = self.ftp.nlst()
        if filename in ftp_f_list:
            return True
        else:
            return False

    def into_path(self, path, setup=True):
        if setup:
            path_list = path.split('/')[:-1]
            for path in path_list:
                if not self.find(path) and path:
                    self.ftp.mkd(path)
                self.ftp.cwd(path)
            return True
        else:
            try:
                self.ftp.cwd(path)
            except Exception:
                return False
            else:
                return True


CONST_BUFFER_SIZE = 1024

NOTICE_INFO = 'http://bulletin.cebpubservice.com/cutominfoapi/bulletin/{}/uid/0'
NOTICE_LIST = 'http://bulletin.cebpubservice.com/cutominfoapi/recommand/type/{}/pagesize/20/currentpage/{}/uid/0'
PDF_REFERER = 'http://bulletin.cebpubservice.com/cebinfomobile/static/pdfjs-dist/web/viewer.html?file={}'
HOST = 'http://bulletin.cebpubservice.com'
UA = 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.116 Safari/537.36 QBCore/4.0.1295.400 QQBrowser/9.0.2524.400 Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2875.116 Safari/537.36 NetType/WIFI MicroMessenger/7.0.5 WindowsWechat'
HEADER = {
    'Accept':
    'application/json, text/plain, */*',
    'User-Agent':
    UA,
    'Referer':
    'http://bulletin.cebpubservice.com/cebinfomobile/',
    'Accept-Encoding':
    'gzip, deflate',
    'Accept-Language':
    'zh-CN,zh;q=0.8,en-US;q=0.6,en;q=0.5;q=0.4',
    'Cookie':
    'acw_tc=2760777615817744196615043e16ad5b7ca269d0bfeaec67357c0747af531b'
}

# config = Myparser()
CONFIG = ConfigParser()
CONFIG.read('config.ini')
# config = config.to_dict()

system = platform.system()
if system == "Linux":
    DEBUG = False
elif system == "Windows":
    DEBUG = False

ocr = BaiduOCR({
    'id': CONFIG.get('BaiduOcr', 'id'),
    'secret': CONFIG.get('BaiduOcr', 'secret')
})

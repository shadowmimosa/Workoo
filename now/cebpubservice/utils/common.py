import os
import time
import pymysql
from pdf2image import convert_from_path

from config import *
from utils.baidu_ocr import BaiduOCR


def get_strftime(timestamps=None):
    if timestamps:
        return time.strftime('%Y-%m-%d %X', time.localtime(timestamps))
    else:
        return time.strftime('%Y-%m-%d %X', time.localtime(time.time()))


def clean_data(content: str):
    return content.replace('T', ' ').replace('.000+0000', '')


def pdf2pic(file_path, output_path):
    if DEBUG:
        poppler_path = r'C:\Users\ShadowMimosa\Desktop\poppler-0.68.0\bin'
    else:
        poppler_path = None
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
        for filename in os.listdir(path):
            with open(os.path.join(path, filename), 'rb') as fn:
                pic_list.append(fn.read())
    elif os.path.isfile(path):
        with open(path, 'rb') as fn:
            pic_list.append(fn.read())

    result = []
    for pic in pic_list:
        text = BaiduOCR().pic2word(pic)["words_result"]
        texts = '\n'.join([x['words'] for x in text])
        result.append(texts)

    return '\n\n'.join(result)


def img_tag(dirpath):
    result = ''
    tag = '<img src=”/image/{}{}”/>'
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


class MysqlOpea(object):
    def __init__(self):
        self.init_sql()
        super().__init__()

    def init_sql(self):
        try:
            if DEBUG:
                config = DATABASES["debug"]
            else:
                config = DATABASES["product"]

            ecnu_mysql = pymysql.connect(**config)

        except pymysql.err.OperationalError as exc:
            print('登录失败！TimeoutError!')
        else:
            self.ecnu_cursor = ecnu_mysql.cursor()

    def insert(self, param: dict):
        sql = 'INSERT INTO `dd1`.`wy` ( `fid`, `uid`, `bt`, `url`, `nr`, `w1`, `w2`, `w5`, `r1`, `r2` ) VALUES ( {fid}, {uid}, "{title}", "{path}", "{img}", "{type}", "{region}", "{text}", "{add_time}", "{notice_time}" );'
        self.ecnu_cursor.execute(sql.format(**param))


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

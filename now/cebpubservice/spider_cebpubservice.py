import os
import json
import time
import urllib
import pymysql
from pdf2image import convert_from_path
from crypto import PyDes3
from config import DEBUG
from config import DATABASES
from utils.request import Query
from less_pic import compress_by_dir
from utils.baidu_ocr import BaiduOCR


def get_strftime(timestamps=None):
    if timestamps:
        return time.strftime('%Y-%m-%d %X', time.localtime(timestamps))
    else:
        return time.strftime('%Y-%m-%d %X', time.localtime(time.time()))


def clean_data(content: str):
    return content.replace('T', ' ').replace('.000+0000', '')


def pdf2pic(file_path, output_path):
    convert_from_path(
        file_path,
        200,
        output_path,
        fmt="PNG",
        output_file='jpeg',
        thread_count=4,
        poppler_path=r'C:\Users\ShadowMimosa\Desktop\poppler-0.68.0\bin')

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
    for img in os.listdir(dirpath):
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
            # os._exit(0)
        else:
            self.ecnu_cursor = ecnu_mysql.cursor()

    def insert(self, param: dict):
        sql = 'INSERT INTO `dd1`.`wy` ( `fid`, `uid`, `bt`, `url`, `nr`, `w1`, `w2`, `w5`, `r1`, `r2` ) VALUES ( {fid}, {uid}, "{title}", "{path}", "{img}", "{type}", "{region}", "{text}", "{add_time}", "{notice_time}" );'
        self.ecnu_cursor.execute(sql.format(sql))

class CebpubService(object):
    """
    notice: 公告
    """
    def __init__(self):
        self.des = PyDes3('ctpstp@custominfo!@#qweASD')
        self.req = Query().run
        self.sql = MysqlOpea()
        self.ua = 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.116 Safari/537.36 QBCore/4.0.1295.400 QQBrowser/9.0.2524.400 Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2875.116 Safari/537.36 NetType/WIFI MicroMessenger/7.0.5 WindowsWechat'
        self.header = {
            'Accept':
            'application/json, text/plain, */*',
            'User-Agent':
            self.ua,
            'Referer':
            'http://bulletin.cebpubservice.com/cebinfomobile/',
            'Accept-Encoding':
            'gzip, deflate',
            'Accept-Language':
            'zh-CN,zh;q=0.8,en-US;q=0.6,en;q=0.5;q=0.4',
            'Cookie':
            'acw_tc=2760777615817744196615043e16ad5b7ca269d0bfeaec67357c0747af531b'
        }
        super().__init__()

    def decrypt_json(self, content):
        data = json.loads(self.des.decrypt(content))
        if data.get('success') is True:
            return data.get('data')
        else:
            print(data.get('errorMessage'))
            return {}

    def real_fid(self, notice_id):
        if notice_id == 0:
            fid = 133
        elif notice_id == 1:
            fid = 0
        elif notice_id == 2:
            fid = 0
        elif notice_id == 3:
            fid = 134
        elif notice_id == 4:
            fid = 135

        return fid

    def get_notice_list(self, _type: int, page):
        """获取公告列表

        0: 招标公告
        1: 资格预审公告
        2: 中标候选人公示
        3: 中标结果公示
        4: 更正公告公示
        """

        path = f'http://bulletin.cebpubservice.com/cutominfoapi/recommand/type/{_type}/pagesize/20/currentpage/{page}/uid/0'
        resp = self.req(path)
        data = self.decrypt_json(resp)
        if not data:
            return []

        return data.get('dataList')

    def down_pdf(self, path, dir_path='./'):
        pdf_path = f'{dir_path}/{path.split("/")[-1]}.pdf'

        opener = urllib.request.build_opener()
        opener.addheaders = [
            ('Accept', '*/*'), ('Accept-Encoding', 'gzip, deflate'),
            ('Origin', 'http://bulletin.cebpubservice.com'),
            ('Accept-Language', 'zh-CN,zh;q=0.8,en-US;q=0.6,en;q=0.5;q=0.4'),
            ('User-Agent', self.ua),
            ('Referer',
             f'http://bulletin.cebpubservice.com/cebinfomobile/static/pdfjs-dist/web/viewer.html?file={path}'
             )
        ]
        urllib.request.install_opener(opener)
        urllib.request.urlretrieve(path, pdf_path)

        return pdf_path

    def get_notice_info(self, bulletin_id):
        path = f'http://bulletin.cebpubservice.com/cutominfoapi/bulletin/{bulletin_id}/uid/0'
        resp = self.req(path)
        data = self.decrypt_json(resp)
        info = {
            'type_id': 0,
            'uid': 0,
            'title': data.get('bulletinName'),
            'path': '',
            'img': '',
            'type': '',
            'region': data.get('regionName').replace('省', '').replace('市', ''),
            'text': '',
            'add_time': get_strftime(),
            'notice_time': clean_data(data.get('noticeSendTime')),
            'pdf_url': data.get('pdfUrl')
        }
        return info

    def detail(self):
        pass

    def main(self):
        for page in range(10):
            for notice_type in range(5):
                data = self.get_notice_list(notice_type, page + 1)

                for item in data:
                    info = self.get_notice_info(item.get('bulletinID'))
                    pdf_path = self.down_pdf(info.get('pdf_url'),
                                             create_path('pdf'))
                    pic_raw_path = pdf2pic(
                        pdf_path, create_path('pic_raw', info.get('pdf_url')))
                    pic_path = compress_by_dir(
                        pic_raw_path, create_path('pic', info.get('pdf_url')))
                    info[''] = item.get('notieIndustriestName')
                    info['fid'] = self.real_fid(notice_type)
                    info['text'] = pic2text(pic_path)
                    info['img'] = img_tag(pic_path)
                    self.sql.insert(info)


if __name__ == "__main__":
    # from ftplib import FTP
    # ftp=FTP()
    # ftp.storbinary()
    spider = CebpubService()
    spider.main()

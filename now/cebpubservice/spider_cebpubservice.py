import os
import json
import time
import urllib
import pymysql
from crypto import PyDes3
from config import DEBUG
from config import DATABASES
from utils.request import Query


def get_strftime(timestamps=None):
    if timestamps:
        return time.strftime('%Y-%m-%d %X', time.localtime(timestamps))
    else:
        return time.strftime('%Y-%m-%d %X', time.localtime(time.time()))


def clean_data(content: str):
    return content.replace('T', ' ').replace('.000+0000', '')


def pdf2pic(file_path, output_path):
    from pdf2image import convert_from_path
    convert_from_path(file_path,
                      500,
                      output_path,
                      fmt="PNG",
                      output_file='pic',
                      thread_count=4,
                      poppler_path=None)

    # images = convert_from_path(file_path)
    # for index, img in enumerate(images):
    #     img.save('%s/page_%s.png' % (output_path, index))


def pic2text(path):
    pass


class MysqlOpea(object):
    def __init__(self):
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
            os._exit(0)
        else:
            self.ecnu_cursor = ecnu_mysql.cursor()

    def insert(self, param: dict):
        sql = "INSERT INTO `dd1`.`wy` ( `fid`, `uid`, `bt`, `url`, `nr`, `w1`, `w2`, `w5`, `r1`, `r2` ) VALUES ( `{type_id}`, `{uid}`, `{title}`, `{path}`, `{text}`, `{type}`, `{region}`, `{keyword}`, `{add_time}`, `{notice_time}` );"
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

    def get_notice_list(self, _type: int):
        """获取公告列表

        0: 招标公告
        1: 资格预审公告
        2: 中标候选人公示        
        3: 中标结果公示        
        4: 更正公告公示        
        """

        path = f'http://bulletin.cebpubservice.com/cutominfoapi/recommand/type/{_type}/pagesize/20/currentpage/1/uid/0'
        resp = self.req(path)
        data = self.decrypt_json(resp)
        if not data:
            return []

        return data.get('dataList')

    def down_pdf(self, path, dir_path='./'):
        os.makedirs(dir_path) if not os.path.exists(dir_path) else True
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

    def get_notice_detail(self, bulletin_id):
        path = f'http://bulletin.cebpubservice.com/cutominfoapi/bulletin/{bulletin_id}/uid/0'
        resp = self.req(path)
        data = self.decrypt_json(resp)
        info = {
            'type_id': 0,
            'uid': 0,
            'title': data.get('bulletinName'),
            'path': '',
            'text': '',
            'type': data.get('type'),
            'region': data.get('region'),
            'keyword': '',
            'add_time': get_strftime(),
            'notice_time': clean_data(data.get('noticeSendTime')),
            'pdf_url': data.get('pdfUrl')
        }
        return info

    def main(self):
        data = self.get_notice_list(0)
        for item in data:
            info = self.get_notice_detail(item.get('bulletinID'))
            pdf_path = self.down_pdf(
                info.get('pdf_url'),
                './static/pdf/{}/'.format(time.strftime("%Y%m%d")))
            pdf2pic(pdf_path,
                    './static/pic/{}/'.format(time.strftime("%Y%m%d")))


if __name__ == "__main__":
    # from ftplib import FTP
    # ftp=FTP()
    # ftp.storbinary()
    spider = CebpubService()
    spider.main()

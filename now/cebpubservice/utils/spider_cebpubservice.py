import os
import json
import urllib

from utils.common import *
from utils.crypto import PyDes3
from utils.request import Query
from utils.less_pic import compress_by_dir

from config import *


class CebpubService(object):
    """
    notice: 公告
    """
    def __init__(self):
        self.des = PyDes3()
        self.req = Query().run
        self.sql = MysqlOpea()
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

        path = NOTICE_LIST.format(_type, page)
        resp = self.req(path, HEADER)
        data = self.decrypt_json(resp)
        if not data:
            return []

        return data.get('dataList')

    def down_pdf(self, path, dir_path='./'):
        pdf_path = f'{dir_path}/{path.split("/")[-1]}.pdf'

        opener = urllib.request.build_opener()
        opener.addheaders = [('Accept', '*/*'),
                             ('Accept-Encoding', 'gzip, deflate'),
                             ('Origin', HOST),
                             ('Accept-Language',
                              'zh-CN,zh;q=0.8,en-US;q=0.6,en;q=0.5;q=0.4'),
                             ('User-Agent', UA),
                             ('Referer', PDF_REFERER.format(path))]
        urllib.request.install_opener(opener)
        urllib.request.urlretrieve(path, pdf_path)

        return pdf_path

    def get_notice_info(self, bulletin_id):
        path = NOTICE_INFO.format(bulletin_id)
        resp = self.req(path, header=HEADER)
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
                        
                    info['w1'] = item.get('notieIndustriestName')
                    info['fid'] = self.real_fid(notice_type)
                    info['text'] = pic2text(pic_path)
                    info['img'] = img_tag(pic_path)

                    self.sql.insert(info)


if __name__ == "__main__":
    spider = CebpubService()
    spider.main()

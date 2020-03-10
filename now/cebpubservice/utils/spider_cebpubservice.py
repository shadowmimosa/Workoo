import os
import json
import urllib

from utils.common import *
from utils.log import logger
from utils.run import run_func
from utils.crypto import PyDes3
from utils.request import Query
from utils.less_pic import compress_by_dir


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
            fid = 133
        elif notice_id == 2:
            fid = 134
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
            'title': data.get('bulletinName'),
            'path': '',
            'img': '',
            'type': '',
            'region': clean_region(data.get('regionName')),
            'text': '',
            'add_time': get_strftime(),
            'notice_time': clean_date(data.get('noticeSendTime')),
            'pdf_url': data.get('pdfUrl')
        }
        return info

    def detail(self, item, fid):
        bulletin_id = item.get('bulletinID')
        if not run_func(self.sql.repeat, bulletin_id):
            return

        info = run_func(self.get_notice_info, bulletin_id)

        pdf_path = run_func(self.down_pdf, info.get('pdf_url'),
                            create_path('pdf'))
        if not pdf_path:
            logger.error('pdf 下载失败失败 - {} '.format(bulletin_id))
            return

        pic_raw_path = run_func(pdf2pic, pdf_path,
                                create_path('pic_raw', info.get('pdf_url')))
        if not pic_raw_path:
            logger.error('转图片失败 - {} '.format(bulletin_id))
            return

        pic_path = run_func(compress_by_dir, pic_raw_path,
                            create_path('pic', info.get('pdf_url')))
        if not pic_path:
            logger.error('图片压缩失败 - {} '.format(bulletin_id))
            return

        info['trade'] = parser_trade(info['title'],
                                     item.get('notieIndustriestName'))
        info['fid'] = fid
        info['text'] = run_func(pic2text, pic_path)
        info['img'] = run_func(img_tag, pic_path)
        info['local'] = pic_path
        info['source'] = item.get('noticeUrl')
        info['bulletin_id'] = bulletin_id
        
        if run_func(self.sql.insert, info):
            logger.info('插入成功 - {} '.format(bulletin_id))
        else:
            logger.error('插入失败 - {} '.format(bulletin_id))

    def main(self):
        for page in range(int(CONFIG.get('PageNum', 'pages'))):
            for notice_type in range(5):
                data = run_func(self.get_notice_list, notice_type, page + 1)
                fid = run_func(self.real_fid, notice_type)
                for item in data:
                    run_func(self.detail, item, fid)


if __name__ == "__main__":
    spider = CebpubService()
    spider.main()

import os
from utils.log import logger
from utils.run import run_func
from utils.common import MysqlOpea, FtpOpea


class UploadSomething(object):
    def __init__(self):
        self.ftp = FtpOpea()
        self.ftp.connect()
        self.local_sql = MysqlOpea()
        self.remote_sql = MysqlOpea(upload=True)
        super().__init__()

    def upload_sql(self):
        pass

    def upload_img(self, dirpath):
        if not dirpath:
            return
        run_func(self.ftp.into_path, dirpath.replace('static/pic/', ''))
        for filename in os.listdir(dirpath):
            filepath = os.path.join(dirpath, filename)
            retry = 5
            while retry:
                status = self.ftp.upload(filepath)
                if status:
                    break
            else:
                return

        retry = 5
        while retry:
            status = run_func(self.ftp.into_path, '/', setup=False)
            if status:
                break
        else:
            return

        return True

    def main(self):
        result = run_func(self.local_sql.select)
        while result:
            for item in result:
                if not run_func(self.upload_img, item['local']):
                    logger.error('图片上传失败 - {}'.format(item.get('ID')))
                    continue
                if not run_func(self.remote_sql.insert, item):
                    logger.error('远程入库失败 - {}'.format(item.get('ID')))
                    continue
                if not run_func(self.local_sql.update, item.get('ID')):
                    logger.error('上传状态修改失败 - {}'.format(item.get('ID')))

                logger.info('上传成功 - {}'.format(item.get('ID')))
                
            result = run_func(self.local_sql.select)


if __name__ == "__main__":
    while 0:
        print(5)
    else:
        print(6)
    upload = UploadSomething()
    upload.main()
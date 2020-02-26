import os
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
        self.ftp.into_path(dirpath.replace('static/pic/', ''))
        for filename in os.listdir(dirpath):
            filepath = os.path.join(dirpath, filename)
            retry = 5
            while retry:
                status = self.ftp.upload(filepath)
                if status:
                    break
        self.ftp.into_path('/', setup=False)

    def main(self):
        result = self.local_sql.select()
        while result:
            for item in result:
                self.remote_sql.insert(item)
                self.upload_img(item['local'])
                self.local_sql.update(item['ID'])
                
            result = self.local_sql.select()


if __name__ == "__main__":
    upload = UploadSomething()
    upload.main()
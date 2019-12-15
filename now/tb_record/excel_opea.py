from xlwt import Workbook
from xlrd import open_workbook
from openpyxl import load_workbook


class InvalidOpeaException(Exception):
    """Error for trying to open a non-ooxml file."""


class ExcelOpea(object):
    def __init__(self, read_or_write='read', use='openpyxl'):
        super().__init__()

        self.use = use

    def read(self, path, use='openpyxl'):
        if use == 'openpyxl':
            workbook = load_workbook(path)
            booksheet = workbook.active

            rows = booksheet.rows
            lines = []

            for row in rows:
                line = [col.value for col in row]
                lines.append(line)

            return lines

        elif use == 'xlrd':
            pass

        else:
            # msg = 'this function only support xlrd and openpyxl to read excel, please check param of use.'
            # raise InvalidOpeaException(msg)
            raise InvalidOpeaException

        self.header = ['skuId', 'extSkuId', 'saleNum']
        self.path = path

        self.init_sheet()

    def init_sheet(self):
        self.wkb = Workbook()
        self.sheet = self.wkb.add_sheet('sheet1', cell_overwrite_ok=True)
        self.row = 0
        self.write(self.header)

    def save(self):
        if self.path is None:
            self.wkb.save('{}.xls'.format(
                time.strftime("%Y-%m-%d %H-%M-%S", time.localtime())))
        else:
            self.wkb.save(self.path)

    def write(self, content: list or dict):
        if isinstance(content, list):
            for index, value in enumerate(content):
                self.sheet.write(self.row, index, value)
        elif isinstance(content, dict):
            for index, value in enumerate(self.header):
                try:
                    need_write = content[value]
                except KeyError:
                    need_write = ''
                self.sheet.write(self.row, index, need_write)

        self.row += 1

    def read_use_xlrd(self):
        pass

    def read_use_openpyxl(self, path):
        pass

    def write_use_xlwt(self):
        self.wkb = Workbook()
        self.sheet = self.wkb.add_sheet('sheet1', cell_overwrite_ok=True)
        self.write(self.header)

    def write_use_openpyxl(self):
        pass


if __name__ == "__main__":
    excel = ExcelOpea()
    excel.read(path='', use='777')

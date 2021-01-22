import csv
from loguru import logger

from utils import excel

excel.init_sheet()


def csv2excel():
    count = 0

    datas = csv.reader(open('D:/detail.csv', 'r', newline='',
                            encoding='utf-8'))
    for line in datas:
        if count > 1000000:
            excel.save()
            count = 0
            excel.init_sheet()

        count += 1
        excel.write(line)
        logger.info(count)

    excel.save()


if __name__ == '__main__':
    csv2excel()

import os

import xlwt

from models.db_schema import Company


def export_data_to_excel(save_name):
    work_book = xlwt.Workbook()
    sheet = work_book.add_sheet('proff.no')
    headers = ['uri', '名称', '电话号码', '种类', '城市', '域名', '邮箱']
    for index, header in enumerate(headers):
        sheet.write(0, index, header)

    company = Company.select()
    for index, _company in enumerate(company):
        sheet.write(index + 1, 0, _company.uri)
        sheet.write(index + 1, 1, _company.name)
        sheet.write(index + 1, 2, _company.phone_number)
        sheet.write(index + 1, 3, _company.category)
        sheet.write(index + 1, 4, _company.city)
        sheet.write(index + 1, 5, _company.domain)
        sheet.write(index + 1, 6, _company.email_address)

    work_book.save(save_name)


def get_project_path():
    return os.path.abspath(
        os.path.join(
            os.path.abspath(os.path.join(os.path.abspath(__file__),
                                         os.pardir)), os.pardir))


if __name__ == '__main__':
    save_path = os.path.join(get_project_path(), 'data/')
    export_data_to_excel(f'{save_path}company.xls')

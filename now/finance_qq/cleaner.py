import csv
import copy
import json


def writer(row: dict):
    product = row['产品']
    manager = row['高管']

    need_rows = []
    for index in range(max(len(product), len(manager))):
        temp_info = {}

        if index == 0:
            temp_info = copy.copy(row)
            temp_info.pop('产品')
            temp_info.pop('高管')

        if len(product) > index:
            temp_info.update({
                '产品': product[index].get('产品'),
                '营业收入': product[index].get('营业收入'),
                '占比': product[index].get('占比')
            })

        if len(manager) > index:
            temp_info.update({
                '职务': manager[index].get('职务'),
                '高管姓名': manager[index].get('高管姓名')
            })

        need_rows.append(temp_info)

    with open('data_with_code.csv', 'a', encoding='utf-8') as fn:
        csv_writer = csv.DictWriter(fn, [
            '股票名称', '股票代码', '公司名称', '主营业务', '所属行业（申万一级）', '所属行业（申万二级）', '产品',
            '营业收入', '占比', '总市值', '流通市值', '高管姓名', '职务'
        ])
        csv_writer.writerows(need_rows)


def reader():
    with open('finace_qq.csv', 'r', encoding='utf-8') as fn:
        csv_reader = csv.DictReader(fn, [
            "产品", "高管", "公司名称", "流通市值", "所属行业（申万二级）", "所属行业（申万一级）", "主营业务",
            "总市值", '股票名称', '股票代码'
        ])
        for row in csv_reader:
            handler = {}
            handler['产品'] = json.loads(row['产品'])
            handler['高管'] = json.loads(row['高管'])
            handler['公司名称'] = row['公司名称']
            handler['流通市值'] = row['流通市值']
            handler['所属行业（申万二级）'] = row['所属行业（申万二级）']
            handler['所属行业（申万一级）'] = row['所属行业（申万一级）']
            handler['主营业务'] = row['主营业务']
            handler['总市值'] = row['总市值']
            handler['股票名称'] = row['股票名称']
            handler['股票代码'] = row['股票代码']

            writer(handler)


if __name__ == "__main__":
    reader()
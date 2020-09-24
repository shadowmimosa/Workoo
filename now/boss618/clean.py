import csv


def writer():
    header = [
        '产品价格', '支付方式', '产品店铺', '24小时销量', '3天销量', '7天销量', '产品类别', '产品名',
        '抢购电话', '公司名', '公司电话', '产品链接'
    ]
    with open('data.csv', 'r', encoding='utf-8') as fn:
        f_csv = csv.DictReader(fn, header)

        for line in f_csv:
            if line['支付方式'] == '0':
                line['支付方式'] = '1'

            with open('result_2_1.csv', 'a', encoding='utf-8') as fn:
                f_csv_w = csv.DictWriter(fn, header)
                f_csv_w.writerow(line)


if __name__ == "__main__":
    writer()
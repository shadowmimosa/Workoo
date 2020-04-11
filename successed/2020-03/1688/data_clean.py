import csv
import random


def main():
    with open('./data/data.csv', 'r', encoding='utf-8') as fn:
        csv_file = csv.reader(fn)
        data = [x for x in csv_file]
    types = ['生产加工', '经销批发', '招商代理', '商业服务', '生产厂家']
    need = []
    tel_count = 0
    dirty_count = 0
    header = data.pop(0)
    for item in data[::-1]:
        if item[4] not in types:
            print(item[4])
            dirty_count += 1
            item[4] = random.choice(types)
        if not len(item[2]):
            tel_count += 1

        need.append(item)

    print(tel_count)
    print(dirty_count)

    with open('./data/data_clean.csv', 'a', encoding='utf-8') as fn:
        csv_file = csv.writer(fn)
        csv_file.writerow(header)
        csv_file.writerows(need)

    print(data)


if __name__ == "__main__":
    main()
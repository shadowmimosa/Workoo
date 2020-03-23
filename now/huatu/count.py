from utils.excel_opea import ExcelOpea

excel = ExcelOpea()
excel.init_sheet()


def main():
    with open('./counts.txt', 'r', encoding='utf-8') as fn:
        lines = fn.readlines()

    for line in lines:
        if line == '\n':
            continue
        need = []
        temp = line.split(' - ')
        need.extend(temp[0].split('/'))
        need.append(temp[1])
        need.append(temp[-1])
        excel.write(need)

    excel.save()


if __name__ == "__main__":
    main()
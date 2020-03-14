import os
import json
from bs4 import BeautifulSoup


def judge(content):
    new = []
    for item in content.contents:
        if not isinstance(item, str):
            new.append(item)

    return new


def extract(content):
    data = {}
    for item in content:
        tag = item.name
        if tag == 'section':
            name = item.find(attrs={'class': 'point-name'}).text
            point = item.find(attrs={
                'class': 'redo interface_toanswer'
            }).get('data-options')
            point = json.loads(point)['pointid']
            child = extract(judge(item))

            data[name] = {'child': child, 'point': point}

    return data


def main():
    data = {}
    dirpath = './data/html/'
    for filename in os.listdir(dirpath):
        with open(f'{dirpath}{filename}', 'r', encoding='utf-8') as fn:
            html = fn.read()

        soup = BeautifulSoup(html, 'lxml')
        title = soup.find(attrs={'class': 'fl title'})
        div = soup.find(attrs={'class': 'tiku-point-panel2 clearfix'})

        obj = judge(div)
        child = extract(obj)
        data[filename.replace('.htm', '')] = child

    with open('./data/points.json', 'w', encoding='utf-8') as fn:
        fn.write(json.dumps(data, ensure_ascii=False))


if __name__ == "__main__":
    main()
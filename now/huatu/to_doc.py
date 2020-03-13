import re
from urllib import parse
from docx import Document
from docx.shared import Inches

from config import MONGO
from utils.log import logger
from utils.run import run_func
from pymongo import MongoClient


class MongoOpea(object):
    def __init__(self):
        self.init_mongo()
        super().__init__()

    def init_mongo(self):

        config = MONGO["debug"]

        config["user"] = parse.quote_plus(config["user"])
        config["passwd"] = parse.quote_plus(config["passwd"])

        client = MongoClient(
            "mongodb://{user}:{passwd}@{host}:{port}/".format(**config),
            connect=False)

        self.mongo = client["huatu"]['raw_data']

    def select(self):
        return list(self.mongo.find({'sync': 0}).limit(1))[0]

    def update(self, sync):
        pass

    def insert(self, data):
        pass


def get_data():
    while True:
        result = mongo.select()
        if result['pointList'][0]['points'][0] in [
                392, 435, 482, 642, 754, 65836, 65877, 65903, 65904, 65905,
                65902, 66089
        ]:
            return result


def down_load_img(url, name):
    r = requests.get(url)
    r.raise_for_status()
    with open(name, 'wb') as fp:
        fp.write(r.content)
        fp.close()


def content_handle(content, index):
    if '<img=' in content and '></img>' in content:
        imgs_url = re.findall('<img=(.*?)></img>', content)
        for url in imgs_url:

            question = question.replace('\\xa0',
                                        '').replace('\\n', '').replace(
                                            '<img=' + url + '></img>', '@@@')

            document.add_paragraph(f'{index}. {question}')

        for url in imgs_url:

            img_name = f'./pic/{url.split("/")[-1]}'
            down_load_img(url, img_name)
            document.add_picture(img_name, width=Inches(2.5))
    else:
        question = question.replace('\\xa0', '').replace('\\n', '')
        document.add_paragraph(f'{index}. {question}')


def material_handle(content):
    if '<img=' in content and '></img>' in content:
        imgs_url = re.findall('<img=(.*?)></img>', content)
        for url in imgs_url:

            question = question.replace('\\xa0',
                                        '').replace('\\n', '').replace(
                                            '<img=' + url + '></img>', '@@@')

            document.add_paragraph(question)

        for url in imgs_url:

            img_name = f'./pic/{url.split("/")[-1]}'
            down_load_img(url, img_name)
            document.add_picture(img_name, width=Inches(2.5))
    else:
        question = question.replace('\\xa0', '').replace('\\n', '')
        document.add_paragraph(question)


def option_handle(content, option):
    if '<img=' in content and '></img>' in content:
        imgs_url = re.findall('<img=(.*?)></img>', content)
        for url in imgs_url:

            analysis = content.replace('\\xa0', '').replace('\\n', '').replace(
                '<img=' + url + '></img>', '@@@')

            document.add_paragraph(f'解析: {analysis}')

        for url in imgs_url:

            img_name = f'./pic/{url.split("/")[-1]}'
            down_load_img(url, img_name)
            document.add_picture(img_name, width=Inches(1))
    else:
        question = question.replace('\\xa0', '').replace('\\n', '')
        document.add_paragraph(f'{option}: {question}')


def answer_handle(answer, percents):
    if answer == 1:
        document.add_paragraph('答案: A')
    elif answer == 2:
        document.add_paragraph('答案: B')
    elif answer == 3:
        document.add_paragraph('答案: C')
    elif answer == 4:
        document.add_paragraph('答案: D')
    else:
        logger.error(f'{answer} is wrong')

    document.add_paragraph(f'全站准确率: {percents[answer-1]}')


def analysis_handle(content):
    if '<img=' in content and '></img>' in content:
        imgs_url = re.findall('<img=(.*?)></img>', content)
        for url in imgs_url:

            analysis = content.replace('\\xa0', '').replace('\\n', '').replace(
                '<img=' + url + '></img>', '@@@')

            document.add_paragraph(f'解析: {analysis}')

        for url in imgs_url:

            img_name = f'./pic/{url.split("/")[-1]}'
            down_load_img(url, img_name)
            document.add_picture(img_name, width=Inches(1))
    else:
        question = question.replace('\\xa0', '').replace('\\n', '')
        document.add_paragraph(f'解析: {analysis}')


def end_handle(points, source):
    document.add_paragraph(f'考点: {" ".join(points)}')
    document.add_paragraph(f'来源: {source}')
    document.add_paragraph('\n\n\n')


def main(ids):
    data = get_data()
    if not data.get('pointName'):
        logger.error(f'{data} is wrong')
        return

    dirname = '/'.join(data.get(data.get('pointName')))
    path = f'./doc/{dirname}/{data.get("id")}.docx'
    os.makedirs(path)
    index = 1
    document.add_heading('heading')
    content_handle(data.get('stem'), index)
    material_handle(data.get('materials'))
    choices = data.get('choices')
    if choices:
        option_handle(choices[0], 'A')
        option_handle(choices[1], 'B')
        option_handle(choices[2], 'C')
        option_handle(choices[3], 'D')
    answer_handle(data.get('answer'), data.get('percents'))
    analysis_handle(data.get('analysis'))
    end_handle(data.get('pointsName'), data.get('from'))

    document.save(path)


if __name__ == "__main__":
    mongo = MongoOpea()
    document = Document()
    main(798)
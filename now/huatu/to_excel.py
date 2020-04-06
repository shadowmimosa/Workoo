import re
import os
import copy
import json
import requests
from bson import ObjectId
from urllib import parse
from docx import Document
from docx.shared import Inches

from config import MONGO
from utils.log import logger
from utils.run import run_func
from pymongo import MongoClient
from utils.excel_opea import ExcelOpea

excel = ExcelOpea()


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

    def select(self, point):
        # return list(
        #     self.mongo.find({'_id': ObjectId('5e694dc6d5e714ac48e3d8a2')}))
        return list(self.mongo.find({"pointList.points": point}))


def get_data(point):
    results = mongo.select(point)

    for data in results:
        yield data


def replace(content: str):
    return content
    if content is None:
        return None
    if isinstance(content, list):
        return content
    if isinstance(content, int):
        return content
    content = re.sub('<img[\s\S]*>', '', content)
    return content.replace('<p>', '').replace('</p>', '').replace(
        '<br>', '\n').replace('<br/>', '\n')


def detail(item: dict, index):
    info = {}
    info['id'] = index
    info['question_type'] = item.get('type')
    info['material'] = replace(item.get('material'))
    info['question'] = replace(item.get('stem'))
    info['answer'] = item.get('answer')
    info['analysis'] = replace(item.get('analysis'))
    info['note_name'] = item.get('pointList')[0]['pointsName'][0]
    info['category_id'] = item.get('pointList')[0]['points'][-1]
    info['category_name'] = item.get('pointList')[0]['pointsName'][-1]
    info['source'] = replace(item.get('from'))

    if item.get('meta'):
        info['summary_accuracy'] = item.get('meta').get('percents')[item.get(
            'meta').get('answers').index(item.get('answer'))]
        info['summary_count'] = item.get('meta').get('count')
        temp = copy.deepcopy(item.get('meta').get('percents'))
        if len(temp) == 1:
            info['summary_fallible'] = 0
        else:
            temp.pop(temp.index(max(temp)))
            fail = max(temp)
            if fail == 0:
                info['summary_fallible'] = 0
            else:
                info['summary_fallible'] = item.get('meta').get('answers')[
                    item.get('meta').get('percents').index(fail)]
    else:
        info['summary_accuracy'] = None
        info['summary_count'] = None
        info['summary_fallible'] = None
    info['options'] = '@@'.join([replace(x) for x in item.get('choices')
                                 ]) if item.get('choices') else None
    info['question_notes'] = ''
    info['source_id'] = item.get('parent')
    info['note_id'] = ''
    excel.write(info)


def main():
    excel.init_sheet(header=[
        'id', 'question_type', 'material', 'question', 'answer', 'analysis',
        'note_name', 'category_id', 'category_name', 'source',
        'summary_accuracy', 'summary_count', 'summary_fallible', 'options',
        'question_notes', 'source_id', 'note_id'
    ])
    index = 1
    # for point in [
    #         "66035", "66081", "66172", "66101", "65912", "65851", "66094",
    #         "65960", "66119", "66095", "66098", "66020", "66155", "65886",
    #         "65853", "65973", "65871", "66039", "65940", "65955", "66159",
    #         "65876", "65966", "65913", "66075", "65954", "67886", "66141",
    #         "66160", "65908", "65885", "65843", "65858", "65952", "65983",
    #         "66139", "65863", "65872", "65969", "65959", "66079", "66030",
    #         "65868", "65845", "65985", "66137", "65964", "66078", "65881",
    #         "66154", "66057", "65857", "66136", "65977", "66007", "71756",
    #         "65897", "66080", "65890", "66085", "65979", "65937", "65893",
    #         "66061", "65909", "66164", "65879", "66135", "65852", "65865",
    #         "65987", "66051", "66099", "66077", "66167", "66156", "66083",
    #         "65911", "66097", "65855", "66076", "65980", "65922", "65861",
    #         "65900", "65842", "65869", "65932", "65944", "66019", "66118",
    #         "65981", "66055", "65862", "66014", "65910", "65918", "65860",
    #         "65839", "66169", "66091", "65888", "65982", "65974", "65884",
    #         "65953", "65970", "65838", "65840", "66093", "65963", "66102",
    #         "65971", "65978", "65880", "65844", "65846", "66142", "65967",
    #         "65975", "66143", "67885", "65898", "65927", "66032", "65883",
    #         "65850", "65854", "65895", "66045", "66110", "67884", "65914",
    #         "65991", "65889", "65948", "65896", "65882", "65864", "65989",
    #         "65916", "65867", "66071", "65984", "65968", "71275", "65995",
    #         "66060", "66073", "65892", "66111", "65899", "65891", "66074",
    #         "66157", "65986", "65849", "66018", "66001", "65873", "66108",
    #         "65972", "65917", "65915", "67887", "66072", "65870", "65848",
    #         "65875"
    # ]:
    for point in [
            "65713", "426", "458", "65814", "1008", "636", "65753", "689",
            "735", "65817", "422", "499", "418", "65715", "456", "686", "402",
            "511", "417", "1017", "706", "702", "504", "65780", "731", "65766",
            "448", "515", "65755", "65770", "65827", "65787", "1026", "1005",
            "65799", "599", "451", "555", "525", "71217", "65806", "65752",
            "667", "741", "782", "433", "489", "744", "1010", "441", "408",
            "396", "427", "484", "65819", "434", "65750", "65834", "65763",
            "449", "727", "65828", "681", "65768", "443", "65716", "1004",
            "644", "413", "421", "410", "65788", "65804", "439", "65777",
            "1027", "495", "430", "445", "440", "65718", "65751", "65722",
            "66184", "572", "65779", "65764", "65805", "455", "693", "395",
            "1001", "65759", "415", "411", "1025", "1009", "617", "65822",
            "457", "602", "407", "405", "450", "674", "680", "595", "437",
            "1000", "612", "583", "447", "1022", "630", "716", "65761", "568",
            "1028", "420", "1013", "65802", "520", "608", "459", "1007", "438",
            "698", "65695", "749", "65825", "431", "65835", "429", "442",
            "454", "1003", "1033", "403", "428", "1012", "65767", "65800",
            "661", "1006", "65719", "406", "423", "65749", "65760", "65758",
            "394", "675", "399", "65771", "65754", "65833", "425", "401",
            "722", "65748", "1011", "409", "738", "1023"
    ]:
        yield_data = get_data(int(point))
        # print(len(list(yield_data)))
        while True:
            try:
                data = next(yield_data)
            except StopIteration:
                break
            else:
                # detail(data, index)
                try:
                    detail(data, index)
                except Exception as exc:
                    logger.error(f'error in detail - {exc}')
                else:
                    index += 1
        logger.info(f'{point} is down')

    excel.save()


if __name__ == "__main__":
    mongo = MongoOpea()
    main()
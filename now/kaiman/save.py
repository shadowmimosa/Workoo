import pandas
from utils import mongo

result = mongo.select('kaiman', {'times': '2'}, limit=3000)

lines = pandas.DataFrame(
    columns=['姓名', '公司', '电话', '城市', '职务', '业务', '规模', '优势', '需求', '微信'])

for item in result:
    info = {x['label']: x['content'] for x in item['list']}

    lines = lines.append(info, ignore_index=True)

lines.to_excel('info.xlsx', index=False)
13000000
14728254
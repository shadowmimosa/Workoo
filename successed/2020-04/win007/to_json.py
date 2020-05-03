import json

with open('./arr.json', 'r', encoding='utf-8') as fn:
    data = json.loads(fn.read())
with open('./arr.json', 'w', encoding='utf-8') as fn:
    fn.write(json.dumps(data, ensure_ascii=False, indent=4))

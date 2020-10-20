import json

with open('rank2.txt', 'r', encoding='utf-8') as fn:
    lines = fn.readlines()

data = []
for line in lines:
    for item in json.loads(line).get('stocks').get('stocks_list'):
        stock_code = item.get('stock_code')
        stock_code = f'{stock_code.split(".")[1]}{stock_code.split(".")[0]}'.lower(
        )
        if stock_code in data:
            continue

        data.append(stock_code)

with open('rank2.json', 'w', encoding='utf-8') as fn:
    fn.write(json.dumps(data))

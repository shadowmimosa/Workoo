import json

need = []


def get_children(content):
    if isinstance(content, list):
        for item in content:
            get_children(item)

    elif isinstance(content, dict):
        children = content.get('children')
        if children is None:
            need.append(content.get('title'))
        else:
            get_children(children)

    else:
        print(content)


if __name__ == "__main__":
    with open('./data/locationTree.json', 'r', encoding='utf-8') as fn:
        data = json.loads(fn.read())

    get_children(data)

    with open('./data/need_title.json', 'w', encoding='utf-8') as fn:
        fn.write(json.dumps(need, ensure_ascii=False, indent=4))

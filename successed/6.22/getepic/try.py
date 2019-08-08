import json


def get_bookid(path):
    bookids = []
    with open("./index.json", "r", encoding="utf-8") as fn:
        data = json.loads(fn.read())
        books = data["result"]["categories"]

    for bookid in books:
        bookids.extend(bookid["bookIds"].split(","))

    return bookids


def clean_index():
    bookids = []
    new_bookids = []
    for root, dirs, files in os.walk("./index/"):
        for value in files:
            bookids.extend(get_bookid(value))
            print("当前路径 {}".format(value))

    print("去重前 {}".format(len(bookids)))
    for value in bookids:
        if value not in new_bookids:
            new_bookids.append(value)
    with open("./data.json", "w+", encoding="utf-8") as fn:
        fn.write(json.dumps(new_bookids))
    print("去重后 {}".format(len(new_bookids)))


def main():
    clean_index()


if __name__ == "__main__":
    import os
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    main()
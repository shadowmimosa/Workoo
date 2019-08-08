from mitmproxy import ctx, flow
import json
import os
import time
import shutil


def request(flow):
    #flow.request.headers['User-Agent'] = 'MitmProxy'
    # print(flow.request.headers)
    # ctx.log.info(str(flow.request.headers))
    # ctx.log.warn(str(flow.request.headers))
    # ctx.log.error(str(flow.request.headers))
    pass


def response(flow):
    url = flow.request.url
    response = flow.response
    if ".jpg" in url or ".png" in url:
        filename = url.replace("/", "_").replace(":", "")
        try:
            sign = filename.split("_group1_M00_00_")[-1]
            sign = sign.split("_")[0]
        except:
            return
        try:
            path = "./data/{}_{}/".format(int(time.time() * 10000), sign)
            os.makedirs(path)
        except:
            return
        print(filename)
        print("save {}".format(url))
        with open("{}/{}".format(path, filename), "wb") as fn:
            fn.write(response.content)
    # print("url is {}".format(flow.request.url))
    # print("content is {}".format(response.content))
    # print("size is {}".format(response.chunk_size))
    # print(response)
    # info = ctx.log.info
    # if flow.request.url.startswith(url):
    #     text = response.text

    #     data = json.loads(text)
    #     save(data)


def save(data):
    pass


def data_clean():
    count = 0
    for root, dirs, files in os.walk("./data/"):
        for value in files:
            path = "{}/{}".format(root, value)
            if os.path.getsize(path) < 1024 * 36:
                # del_folder("{}/".format(root))
                count += 1
                break
                # os.remove(path)
                # os.removedirs("{}/".format(root))
    print(count)


def data_count():
    # http__112.74.44.211_group1_M00_00_5A_eBioJ1ir7OKAJQwFAAvgp1Uff4k478.jpg
    data_list = []
    for root, dirs, files in os.walk("./data/"):
        for value in files:
            data = {}
            temp = value.split("_")
            data["ip"] = temp[2]
            data["group"] = temp[3]
            data["M00"] = temp[4]
            data["00"] = temp[5]
            data["5A"] = temp[6]
            data["name"] = temp[-1].split(".")[0]
            data["jpg"] = temp[-1].split(".")[-1]
            data_list.append(data)
    # print(data_list)
    count = {
        "ip": {},
        "group": {},
        "M00": {},
        "00": {},
        "5A": {},
        "name": {},
        "jpg": {}
    }
    keys = ["ip", "group", "M00", "00", "5A", "name", "jpg"]

    for item in data_list:
        for key in keys:
            if item[key] in count[key]:
                count[key][item[key]] += 1
            elif item[key] not in count[key]:
                count[key][item[key]] = 1
    print(len(count["name"].keys()))
    a = list(count["name"].keys())
    print(count)


def copy_folder_to_folder(folder, target):
    for root, dirs, files in os.walk(folder):
        print(root)
        for value in files:
            shutil.copy("{}/{}".format(root, value), target)


def del_folder(path):
    # for root, dirs, files in os.walk(path):
    #     for file_ in files:
    #         os.remove(file_)
    #     for dir_ in dirs:
    shutil.rmtree(path)


def build_folder():
    before_file = ""
    for root, dirs, files in os.walk("./data/"):
        for value in dirs:
            if value.split("_")[-1] == before_file.split("_")[-1]:
                try:
                    copy_folder_to_folder("{}{}".format(root, value),
                                          "{}{}".format(root, before_file))
                except:
                    continue
                finally:
                    del_folder("{}{}".format(root, value))
            else:
                before_file = value


def file_count():
    folder_list = {}
    count = 0
    count_1 = 0
    count_0 = 0
    for root, dirs, files in os.walk("./data/"):
        folder_list[root] = len(files)

    for value in folder_list.values():
        if value == 1:
            count_1 += 1
        else:
            count_0 += 1
    print("只有 1 张照片的有 {} 个，多于一张照片的有 {} 个；共有 {} 个".format(
        count_1, count_0, len(folder_list)))


def marge_folder():
    single_folder = {}
    for root, dirs, files in os.walk("./data/"):
        if len(files) != 0:
            single_folder[root] = len(files)

    keys = list(single_folder.keys())

    for index, value in enumerate(keys):
        if single_folder[value] == 1:
            for i in range(index + 1, index + 15):
                if keys[i].split("_")[-1] == value.split("_")[-1]:
                    try:
                        copy_folder_to_folder(value, keys[i])
                    except:
                        continue
                    finally:
                        del_folder(value)
                        break


def rename_all():
    num = 0
    for root, dirs, files in os.walk("./data/"):
        count = 0
        for value in files:
            if "jpg" in value:
                name = "{}.jpg"
            elif "png" in value:
                name = "{}.png"
            os.rename("{}/{}".format(root, value), "{}/{}".format(
                root, name.format(count)))
            count += 1
            num += count
    print("共有照片 {} 张".format(num))


if __name__ == "__main__":
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    # data_clean()
    # data_count()
    # build_folder()
    rename_all()
    file_count()
    # marge_folder()
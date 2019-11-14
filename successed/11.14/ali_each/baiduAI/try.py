import os
import json
import time
import pandas
import base64
import traceback

from urllib.parse import quote
from utils.request import Query

requests = Query().run


class BaiduToken(object):
    def __init__(self):
        pass

    def get_current_time(self):
        return int(time.time())

    def save_token(self, token):
        with open("./access_token.json", "w", encoding="utf-8") as fn:
            fn.write(
                json.dumps({
                    "token":
                    token,
                    "unavailable_time":
                    self.get_current_time() + 2592000
                }))

    def judge_token(self):
        try:
            with open("./access_token.json", "r", encoding="utf-8") as fn:
                data = json.loads(fn.read())
                if data["unavailable_time"] > self.get_current_time() + 60:
                    return data["token"]
                else:
                    return False
        except FileNotFoundError:
            return False

    def get_token(self):
        token = self.judge_token()
        if token is False:
            host = 'https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id=9CuIDbDfqVaDVxcLoBvLG7Gq&client_secret=AanUEBu3GQudqc2vTdN5ldLTEBHLRQ9p'
            resp = requests(
                host,
                header={'Content-Type': 'application/json; charset=UTF-8'},
                data={})

            if resp:
                token = json.loads(resp)["access_token"]
                self.save_token(token)
                return token
        else:
            return token


class BaiduOCR(object):
    def __init__(self):
        self.token = BaiduToken().get_token()
        self.info = pandas.DataFrame(columns=[
            "姓名", "年龄", "性别", "省份", "加入天数", "帮助人数", "分摊金额", "赔付金额", "疾病"
        ])

    def pic2base64(self, path):
        with open(path, "rb") as fn:
            base64_data = base64.b64encode(fn.read())
            # return quote(base64_data)
            # base64_data = str(base64.b64encode(fn.read()), encoding='utf-8')

        return base64_data

    def pic2word(self, image_base64):
        host = "https://aip.baidubce.com/rest/2.0/ocr/v1/general_basic?access_token={}".format(
            self.token)

        data = {
            "image": image_base64,
            "url": "",
            "language_type": "CHN_ENG",
            "detect_direction": "false",
            "detect_language": "false",
            "probability": "true",
        }
        resp = requests(
            host,
            headers={"Content-Type": "application/x-www-form-urlencoded"},
            data=data)
        self.data_clean(json.loads(resp))

    def main(self):
        rootname = "./ali_each_orc/part2/"
        count = 0
        try:
            for dirname in os.listdir(rootname):
                if ".png" in dirname or "part" in dirname:
                    continue

                for filename in os.listdir("{}{}/".format(rootname, dirname)):
                    self.path = "{}{}/{}".format(rootname, dirname, filename)
                    count += 1
                    pic = self.pic2base64(self.path)
                    self.pic2word(pic)
                    # print("{} is down".format(filename))
        except:
            print("--->Error: the error is {}".format(traceback.format_exc()))
            self.info.to_excel("./data_error.xlsx", index=False)
        else:
            print(count)
            self.info.to_excel("./data.xlsx", index=False)

    def data_clean(self, data):
        for index, item in enumerate(data["words_result"]):
            
            if item["words"] == ">":
                data["words_result"].pop(index)

            if "k," in item["words"]:
                data["words_result"].pop(index)

            if item["words"] == "症期)":
                data["words_result"].pop(index)
                data["words_result"][0]["words"] = "{}症期)".format(
                    data["words_result"][0]["words"])
                self.data_clean(data)

            if item["words"] == "动脉旁路移植术)":
                data["words_result"].pop(index)
                data["words_result"][0]["words"] = "{}动脉旁路移植术)".format(
                    data["words_result"][0]["words"])

            if item["words"] == '肺癌':
                data["words_result"].pop(index)
                data["words_result"][0]["words"] = "{},肺癌".format(
                    data["words_result"][0]["words"])

            if data["words_result"][0]["words"] == "天" and data[
                    "words_result"][1]["words"] == '乳腺癌':
                data["words_result"][0]["words"] = "吴*漫,乳腺癌"
                data["words_result"].pop(1)

            if item["words"] == '期)':
                data["words_result"].pop(index)
                data["words_result"][0]["words"] = "{}期)".format(
                    data["words_result"][0]["words"])

            # if item["words"] == ">":
            #     data["words_result"].pop(index)
            if ">" in item["words"]:
                item["words"] = item["words"].replace(">", "")
            elif "轻度重症" in item["words"]:
                item["words"] = item["words"].replace("轻度重症", "")
            elif "蚂蚁区块链" in item["words"]:
                data["words_result"].pop(index)
            elif "我有异议" in item["words"]:
                data["words_result"].pop(index)

        info = {}
        if len(data["words_result"]) == 3:

            info["姓名"] = data["words_result"][0]["words"].split(",")[0]
            try:
                info["疾病"] = data["words_result"][0]["words"].split(",")[1]
            except IndexError:
                print("{} is wrong".format(self.path))
                return
            info["年龄"] = data["words_result"][1]["words"].split("岁")[0]
            info[
                "性别"] = "男" if "男" in data["words_result"][1]["words"] else "女"

            if "省" in data["words_result"][1]["words"]:
                info["省份"] = data["words_result"][1]["words"].split(
                    info["性别"])[1].split("省")[0]
            else:
                info["省份"] = "{}区".format(
                    data["words_result"][1]["words"].split(
                        info["性别"])[1].split("区")[0])

            info["赔付金额"] = data["words_result"][1]["words"].split(
                "互助金")[1].replace("万元", "")

            temp = data["words_result"][2]["words"].split(",")
            info["加入天数"] = temp[0].replace("加入相互宝", "").replace("天", "")
            info["帮助人数"] = temp[1].replace("帮助了", "").replace("人", "")
            info["分摊金额"] = temp[2].replace("共分摊", "").replace("元", "")

            self.info = self.info.append(info, ignore_index=True)
        else:
            print("Error: the wrong number of line, try again")
            print(data)
            self.pic2word(self.pic2base64(self.path))


if __name__ == "__main__":
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    B = BaiduOCR()
    B.main()

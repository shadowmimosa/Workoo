import io
import time
import pandas
from sqlalchemy import create_engine
from PIL import ImageGrab
import win32gui, win32api, win32con

from utils.baidu_ocr import BaiduOCR
from config import DATABASES, logger


class WinOperate(object):
    def __init__(self):
        self.handle = win32gui.FindWindow(None, "CS")
        self.get_windows()

    def get_windows(self):
        self.left, self.top, right, bottom = win32gui.GetWindowRect(
            self.handle)

    def mouse_move(self, offset_x, offset_y, click=True):
        win32gui.SetForegroundWindow(self.handle)

        win32api.SetCursorPos([self.left + offset_x, self.top + offset_y])

        if click:
            self.mouse_left_click()

    def mouse_left_click(self):
        win32api.mouse_event(
            win32con.MOUSEEVENTF_LEFTUP | win32con.MOUSEEVENTF_LEFTDOWN, 0, 0,
            0, 0)

    def screenshot(self):
        return ImageGrab.grab((self.left + 570, self.top + 125,
                               self.left + 875, self.top + 430))


class Ichengyun(object):
    def __init__(self):
        self.win = WinOperate()
        self.info = pandas.DataFrame(columns=["姓名", "注册号", "证书", "电话"])
        # df.drop(df.index,inplace=True)

        self.init_sql()

    def init_sql(self):
        self.engine = create_engine(
            "mysql+pymysql://{user}:{passwd}@{host}:{port}/{database}?charset={charset}"
            .format(**DATABASES))

    def get_word(self):
        pic = self.win.screenshot()
        byte_io = io.BytesIO()
        pic.save(byte_io, 'png')
        byte_io.seek(0)

        words = BaiduOCR().pic2word(byte_io.read())["words_result"]
        # words = FaceOcr().pic2word(byte_io.read())["result"]
        # print(words)
        # print("OCR Now")

        if words:
            # print("OCR OK")
            self.data_clean(words)
        else:
            print("OCR ERROR")
            print(words)
            print(set(list(pic.getdata())))

    def data_clean(self, words):
        info = {}
        register_list = []
        for item in words:
            word = item["words"]

            if ":" in word:
                temp = word.split(":")
                if "姓名" in temp[0]:
                    if "(" in temp[1]:
                        info["姓名"] = temp[1].split("(")[0]
                    elif "（" in temp[1]:
                        info["姓名"] = temp[1].split("（")[0]
                    elif "O" in temp[1]:
                        info["姓名"] = temp[1].split("O")[0]
                    elif "o" in temp[1]:
                        info["姓名"] = temp[1].split("o")[0]
                    elif "0" in temp[1]:
                        info["姓名"] = temp[1].split("0")[0]
                    elif "男)" in temp[1]:
                        info["姓名"] = temp[1].split("男)")[0]
                    elif "侽男)" in temp[1]:
                        info["姓名"] = temp[1].split("侽男)")[0]
                    else:
                        info["姓名"] = temp[1]
                elif "注册" in temp[0]:
                    info["注册号"] = temp[1]
            elif "~" in word:
                if "主册" in word:
                    word = word.replace("主册", "注册")
                register_list.append(word)

            elif len(word) == 11:
                info["电话"] = word

        level_list = []
        for index, item in enumerate(register_list):
            if "级" in item:
                level_temp = item.split("级")

                if len(level_temp) == 2:
                    if len(level_temp[0]) == 0:
                        level_list.append(True)
                    elif len(level_temp[0]) == 1:
                        level_list.append(level_temp[0])
                    else:
                        level_list.append(False)
                else:
                    level_list.append(False)
            else:
                level_list.append(False)

        if True in level_list:
            for item in level_list:
                if isinstance(item, str):
                    level_temp = item

            for index, item in enumerate(level_list):
                if item is True:
                    register_list[index] = "{}{}".format(
                        level_temp, register_list[index])

        info["证书"] = "\n".join(register_list)
        # print("ADD NOW")
        self.info = self.info.append(info, ignore_index=True)
        # print(len(self.info), "\n")

    def next_page(self):
        self.win.mouse_move(335, 565)
        hold_on(8)
        self.win.mouse_move(600, 375)

    def save_info(self):
        if len(self.info) > 76:
            self.info.to_excel(
                "./{}.xlsx".format(int(time.time() * 1000)), index=False)
            self.info.to_sql(
                "ichengyun", self.engine, if_exists="append", index=False)
            # del self.info
            # self.info = pandas.DataFrame(columns=["姓名", "注册号", "证书", "电话"])
            return False
        else:
            return True

    def loading_status(self):
        hold_on(1.5)
        while True:
            pic = self.win.screenshot()

            if judge_pixel(pic) == "colorful":
                hold_on(1)
                self.win.mouse_move(600, 345)
                hold_on(0.5)
                break
            else:
                hold_on(1)
                continue

    def auto_click(self):
        starttime = time.time()
        for index in range(16):
            offset = 24 * index
            self.win.mouse_move(230, 160 + offset)

            self.loading_status()

            self.get_word()

            if self.save_info() is False:
                hold_on(86400)
        self.next_page()

        for _ in range(84):
            self.win.mouse_move(230, 160)
            pic = self.win.screenshot()

            self.loading_status()

            self.win.mouse_move(555, 540)
            hold_on(1)

            self.get_word()

            if self.save_info() is False:
                hold_on(86400)


        self.save_info()
        print("next page")
        hold_on(5)

    def main(self):
        while True:
            self.auto_click()


def hold_on(second):
    time.sleep(second)


def judge_pixel(img):
    pixels = list(img.getdata())

    if (113, 166, 255) in pixels:
        return "blue"
    else:
        single = set(pixels)
        if len(single) > 1:
            return "colorful"
        elif (255, 255, 255) in single:
            return "white"


if __name__ == "__main__":
    Ichengyun().main()

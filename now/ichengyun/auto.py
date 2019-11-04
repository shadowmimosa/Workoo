import io
import time
from PIL import ImageGrab
import win32gui, win32api, win32con

from utils.baidu_ocr import BaiduOCR


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

    def get_word(self):
        pic = self.win.screenshot()
        byte_io = io.BytesIO()
        pic.save(byte_io, 'png')
        byte_io.seek(0)
        a = BaiduOCR().pic2word(byte_io.read())
        print(a['words_result'])

    def auto_click(self):
        for _ in range(10):
            self.win.mouse_move(230, 160)
            hold_on(5)

            self.win.mouse_move(555, 540)
            hold_on(2)

            self.get_word()

        self.win.mouse_move(335, 565)
        hold_on(5)

        self.win.mouse_move(600, 375)

    def main(self):
        for index in range(10):
            self.auto_click()


def hold_on(second):
    time.sleep(second)


if __name__ == "__main__":
    Ichengyun().main()
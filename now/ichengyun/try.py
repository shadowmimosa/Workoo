import time
# from win32 import win32gui
# from win32 import win32api, win32console
# import win32api

import win32gui, win32api, win32con

from PIL import ImageGrab

handle = win32gui.FindWindow(None, "CS")

win32gui.SetForegroundWindow(handle)
left, top, right, bottom = win32gui.GetWindowRect(handle)

for _ in range(10):
    win32api.SetCursorPos([left + 555, top + 540])
    time.sleep(1)
    win32api.mouse_event(
        win32con.MOUSEEVENTF_LEFTUP | win32con.MOUSEEVENTF_LEFTDOWN, 0, 0, 0,
        0)
    win32api.SetCursorPos([left + 230, top + 160])
    time.sleep(2)
    win32api.mouse_event(
        win32con.MOUSEEVENTF_LEFTUP | win32con.MOUSEEVENTF_LEFTDOWN, 0, 0, 0,
        0)
    win32api.SetCursorPos([left + 335, top + 565])
    win32api.mouse_event(
        win32con.MOUSEEVENTF_LEFTUP | win32con.MOUSEEVENTF_LEFTDOWN, 0, 0, 0,
        0)
    time.sleep(2)
    win32api.SetCursorPos([left + 600, top + 375])
    win32api.mouse_event(
        win32con.MOUSEEVENTF_LEFTUP | win32con.MOUSEEVENTF_LEFTDOWN, 0, 0, 0,
        0)
    time.sleep(2)

ImageGrab.grab((left + 570, top + 125, left + 875, top + 430)).show()
(230, 160)

(550, 540)

(570, 125, 875, 430)

qrcode = Image.open(io.BytesIO(self.qrcode)).resize((800, 800))
init_pic = Image.open("./static/wechat/images/init.jpg")
init_pic.paste(qrcode, (460, 1600))
byte_io = io.BytesIO()
init_pic.save(byte_io, 'jpeg')
byte_io.seek(0)
self.qrcode = byte_io

time.sleep(10)
print(handle)
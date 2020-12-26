import io
import cv2
import sys
import time
import pandas
import base64
import random
import atexit
import logging
import datetime
import keyboard
import tempfile
import win32gui
import pyperclip
import numpy as np
from pathlib import Path
from loguru import logger
from multiprocessing import freeze_support
from earthtest.core.api import touch, Template, connect_device, keyevent
from earthtest.aircv import crop_image, imwrite
from earthtest.core.cv import loop_find
from earthtest.core.settings import Settings
from earthtest.core.error import TargetNotFoundError
from earthtest.core.helper import G

from utils.signer import magic
from utils import mysql, ocr, run_func

Settings.CVSTRATEGY = ['tpl', 'kaze', 'brisk', 'akaze', 'orb']
Settings.THRESHOLD = 0.7
Settings.FIND_TIMEOUT = 30
Settings.LOG_DIR = ''
Settings.SNAPSHOT_QUALITY = 99

logging.getLogger("earthtest.core.api").setLevel(logging.ERROR)
logging.getLogger("earthtest.aircv.template_matching").setLevel(logging.ERROR)
logging.getLogger("earthtest.aircv.keypoint_base").setLevel(logging.ERROR)


class Images(object):
    def __init__(self) -> None:
        if getattr(sys, 'frozen', False):
            self.application_path = sys._MEIPASS
        elif __file__:
            self.application_path = '.'

        self.decrypt_path = self.save(
            'iVBORw0KGgoAAAANSUhEUgAAACAAAAAUCAIAAABj86gYAAAACXBIWXMAAA7EAAA' +
            'OxAGVKw4bAAAAEXRFWHRTb2Z0d2FyZQBTbmlwYXN0ZV0Xzt0AAACwSURBVDiN7V' +
            'VBDoAgDAND/Ayv4OW+ws94wQOG1M1uaoIne1piN9oVYqy1hpGYhk7/9oBtWbdlf' +
            'THCbow9AyTNJeueuWRBs9H4Cafj3F4bhzEgP+npdrP4ii29Rs6xImZceNIChT+t' +
            'kt6iJuRSFPPUChFVYm3Mkw5GbwnhrOhSqSsCmdRBMGPXwTDQA1gny5zxH6yIDWX' +
            '1LQd3XoYNKwMX6Jvt4PSSDZ6Am1BH/H84HnZZBJWvlzgIPQAAAABJRU5ErkJggg==',
            'decrypt')

        self.next_one_path = self.save(
            'iVBORw0KGgoAAAANSUhEUgAAAAwAAAAMCAIAAADZF8uwAAAACXBIWXMAAA7EAAAOx\
            AGVKw4bAAAAEXRFWHRTb2Z0d2FyZQBTbmlwYXN0ZV0Xzt0AAABwSURBVBiVrY+xDcA\
            gDARNlNagjMEIbOIxWMuTsA4gkQ6TAgmhNFBwlfX+l9+q1gor7tba2iQih0w75+CdI\
            KJngoi6rkopI5BScs7lnAFAax1CMMYAwCUTiMjMPcDMiNj1f3Frrfe+D2OlYoxnvts\
            yfWjtVjKayh9bAAAAAElFTkSuQmCC', 'next_one')

        self.hundred_path = self.save(
            'iVBORw0KGgoAAAANSUhEUgAAABsAAAAPCAYAAAAVk7TYAAAA00lEQVQ4jeWUMQ6CQ\
                BBFP8YOD2GotF5KLEy4gCZaidegsoRDUOAN9AZwC7Fh4SbfBlBRYdeCQn8yxcw\
                    r/v7MZA2SxEAaDWX0l2YpPHuPULbnBcLtAhO7qu0RmQ7nkxLuhENTODSFx\
                        yB/piffoeknX/cts0p5TPvFLOGuPctj2uLAkxIn1XcmS1zfghKZVOD\
                            QPpAp5tZDa00x0+CaZvdXAniTppuPlX1eUtSq0/RxrWRLrN0CY\
                                ZQ2k3MUI3OXWClxdJ1+VZuYl4ZLBptPrJ8b5I9+xDfosDq\
                                    8kQHEGgAAAABJRU5ErkJggg==', 'hundred')

        self.next_page_path = self.save(
            'iVBORw0KGgoAAAANSUhEUgAAADEAAAAeCAYAAACFZvb/AAAA6UlEQVRYhe2XPRKE \
                IAyFkx07vY2Wenpbj2OfbfYnQlwIy0hk+DocBvLIS0AkIoKb8ygdQA6aCCtUI \
                    aLjA0QsFYcKtxd1oQnWkA66CjtVIcKz0xUM0xI9d9/W4BzkNzYiAhFl3y \
                        SGYVriAn7FeIAYzvBDP87i91xo1pdiLGInAN9SUvZjs6wSEZvyWH6 \
                            tpbG0qjvt26pa/CrUdnoL4aeYoxH8k+WkmnCF5LRYClVcdqZa \
                                bD/Owb2kGIu1WIBvLbm2dL+HKPrsOAuSi0l+dlhGirGKw \
                                    m4irOAV9l3+szkHEdaL+owq7NREWOEJlfDGzavKdq \
                                        sAAAAASUVORK5CYII=', 'next_page')

        self.confirm_path = self.save(
            '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', 'confirm')

    def save(self, dataurl, name):
        img_string = base64.b64decode(dataurl)
        file_path = Path(self.application_path).joinpath(f'{name}.png')

        with tempfile.NamedTemporaryFile('wb', delete=False) as png:
            png.write(img_string)
            return png.name

        with open(file_path, 'wb') as fn:
            fn.write(img_string)

        return file_path


IMAGES = Images()


@run_func()
def get_window_handle(name='CS'):
    '''获取窗口句柄'''

    handle = win32gui.FindWindow(None, name)

    if handle == 0:
        print('没获取到应用句柄')
        exit()
    else:
        return handle


@atexit.register
def clean():
    Path(IMAGES.decrypt_path).unlink(missing_ok=True)
    Path(IMAGES.next_one_path).unlink(missing_ok=True)


@run_func()
def magic_time():
    time.sleep(random.uniform(0, 5))


class Ichengyun(object):
    def __init__(self) -> None:
        self.win = connect_device(f'Windows:///{get_window_handle()}')

        self.pos_company = (660, 155)
        self.pos_name = (660, 180)
        self.pos_register = (660, 205)

        self.info = pandas.DataFrame(columns=[
            'name', 'company', 'sex', 'phone', 'register', 'achievement',
            'changes', 'levels'
        ])

        super().__init__()

    @run_func()
    def _copy(self, pos):
        touch(pos)
        keyevent('^a')
        keyevent('^c')
        return pyperclip.paste()

    @run_func()
    def deal_image(self):
        screen = G.DEVICE.snapshot()
        screen = crop_image(screen, (577, 222, 884, 450))

        hsv = cv2.cvtColor(screen, cv2.COLOR_BGR2HSV)

        lower_solid_red = np.array([0, 255, 255])
        upper_solid_red = np.array([0, 255, 255])

        lower_orange = np.array([11, 43, 46])
        upper_orange = np.array([25, 255, 255])

        mask_solid_red = cv2.inRange(hsv, lower_solid_red, upper_solid_red)
        mask_orange = cv2.inRange(hsv, lower_orange, upper_orange)

        white_color = [255, 255, 255]

        img = np.copy(screen)

        img[mask_solid_red != 0] = white_color
        img[mask_orange != 0] = white_color

        filename = "%(time)d.png" % {'time': time.time() * 1000}
        filedir = Path('./images')
        filedir.mkdir(exist_ok=True)
        filepath = filedir.joinpath(filename)
        imwrite(filepath, img, 99)

        self.img = img

    @run_func()
    def get_level(self):
        white_color = [255, 255, 255]
        lower_red = np.array([0, 43, 46])
        upper_red = np.array([10, 255, 255])

        hsv = cv2.cvtColor(self.img, cv2.COLOR_BGR2HSV)
        mask_red = cv2.inRange(hsv, lower_red, upper_red)

        img_mask = np.copy(self.img)
        img_mask[mask_red != 0] = white_color

        is_success, buffer = cv2.imencode('.png', img_mask)
        io_buf = io.BytesIO(buffer)
        words = ocr.pic2word(io_buf.read())["words_result"]

        levels = ''
        for word in words:
            levels += word.get('words')
            levels += '\n'

        return levels.strip('\n')

    @run_func()
    def get_phone(self):
        low_hsv = np.array([0, 43, 46])
        high_hsv = np.array([10, 255, 255])

        hsv = cv2.cvtColor(self.img, cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(hsv, lowerb=low_hsv, upperb=high_hsv)

        is_success, buffer = cv2.imencode('.png', mask)
        io_buf = io.BytesIO(buffer)

        words = ocr.pic2word(io_buf.read())["words_result"]

        return words[0].get('words')

    @run_func()
    def auto_page(self, y=0):
        info = {}
        touch((230, 162 + y))
        touch(Template(IMAGES.decrypt_path))

        info['company'] = self._copy(self.pos_company)
        temp_name = self._copy(self.pos_name).split(' ')
        info['name'] = temp_name[0].strip('\ufeff')
        info['sex'] = temp_name[1].replace('(', '').replace(')', '')
        info['changes'] = temp_name[2].replace('变更(', '').replace(')', '')
        info['achievement'] = temp_name[3].replace('业绩(', '').replace(')', '')
        info['register'] = self._copy(self.pos_register)

        self.deal_image()

        info['levels'] = self.get_level()
        info['phone'] = self.get_phone()
        mysql.insert(info)
        self.info = self.info.append(info, ignore_index=True)
        logger.info("--->Info: No.{} is down".format(len(self.info)))

        if not y:
            touch(Template(IMAGES.next_one_path))

    @run_func()
    def save(self):
        if len(self.info) > 0:
            self.info.to_excel("./{}.xlsx".format(int(time.time() * 1000)),
                               index=False)
            del self.info
            self.info = pandas.DataFrame(columns=[
                'name', 'company', 'sex', 'phone', 'register', 'achievement',
                'changes', 'levels'
            ])

            logger.info("--->Info: save info")

    @run_func()
    def _sleep(self):
        logger.info("--->Info: sleep 24 hours now")
        sleep_time = 86400
        while not self.start_status and sleep_time > 0:
            time.sleep(1)
            sleep_time -= 1

    @run_func()
    def judge_time(self):
        start_time = datetime.datetime.strptime(
            str(datetime.datetime.now().date()) + '8:10', '%Y-%m-%d%H:%M')
        end_time = datetime.datetime.strptime(
            str(datetime.datetime.now().date()) + '20:50', '%Y-%m-%d%H:%M')
        now_time = datetime.datetime.now()

        if start_time < now_time < end_time:
            return True
        else:
            self._sleep()
            self.judge_time()

    @run_func()
    def run(self):
        self.start_status = True
        y = 0
        while True:
            if not self.start_status:
                self._sleep()

            self.judge_time()

            self.win.set_foreground()
            self.auto_page(y)
            # magic_time()

            try:
                pos = loop_find(Template(IMAGES.hundred_path),
                                timeout=1,
                                threshold=0.95)
            except TargetNotFoundError:
                pos = None

            if pos and pos[0] < 50:
                y += 24

            if y > 360:
                touch(Template(IMAGES.next_page_path))
                touch(Template(IMAGES.confirm_path))
                y = 0

    @run_func()
    def _exit(self):
        self.start_status = False
        self.save()
        # sys.exit()


clawer = Ichengyun()

keyboard.add_hotkey('win + f9', clawer.run)
keyboard.add_hotkey('win + f10', clawer._exit, suppress=True)
keyboard.wait('win + f11', suppress=True)

if __name__ == "__main__":
    freeze_support()
    if int(time.time()) < 1629729356:
        magic()

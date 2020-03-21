import os
import bs4
import time
import logging
import concurrent_log
from concurrent_log import ConcurrentTimedRotatingFileHandler
from concurrent_log_handler import ConcurrentRotatingFileHandler
from bs4 import BeautifulSoup
from multiprocessing_logging import install_mp_handler
from logging.handlers import RotatingFileHandler, TimedRotatingFileHandler, BaseRotatingHandler


class DealSoup(object):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def find_tag_by_attr(self):
        if self.all_tag is False:
            return self.soup.find(attrs=self.attr)
        else:
            return self.soup.find_all(attrs=self.attr)

    def find_tag_by_name(self):
        if self.all_tag is False:
            return self.soup.find(self.attr)
        else:
            return self.soup.find_all(self.attr)

    def find_tag(self):
        if isinstance(self.attr, dict):
            return self.find_tag_by_attr()
        elif isinstance(self.attr, str):
            return self.find_tag_by_name()

    def init_soup(self):
        if isinstance(self.content, str):
            self.soup = BeautifulSoup(self.content, "lxml")
        elif isinstance(self.content, bs4.Tag):
            self.soup = self.content
        elif isinstance(self.content, bs4.BeautifulSoup):
            print("略略略")

    def judge(self, content, attr: dict = None, all_tag: bool = False):
        self.content = content
        self.attr = attr
        self.all_tag = all_tag

        self.init_soup()

        if self.attr is None:
            return self.soup
        else:
            return self.find_tag()


class MultiProcessSafeDailyRotatingFileHandler(BaseRotatingHandler):
    """Similar with `logging.TimedRotatingFileHandler`, while this one is
    - Multi process safe
    - Rotate at midnight only
    - Utc not supported
    """
    def __init__(self,
                 filename,
                 encoding=None,
                 delay=False,
                 utc=False,
                 **kwargs):
        self.utc = utc
        self.suffix = "%Y-%m-%d %H%M%S"
        self.baseFilename = filename
        self.currentFileName = self._compute_fn()
        BaseRotatingHandler.__init__(self, self.currentFileName, 'a', encoding,
                                     delay)

    def shouldRollover(self, record):
        if self.currentFileName != self._compute_fn():
            return 1
        return 0

    def doRollover(self):
        if self.stream:
            self.stream.close()
            self.stream = None
        self.currentFileName = self._compute_fn()

    def _compute_fn(self):
        if 'txt' in self.baseFilename:
            return self.baseFilename
        else:
            return self.baseFilename + time.strftime(self.suffix,
                                                     time.localtime()) + '.txt'

    def _open(self):
        if self.encoding is None:
            stream = open(self.currentFileName, self.mode)
        else:
            stream = open(self.currentFileName,
                          self.mode,
                          encoding=self.encoding)
        # simulate file name structure of `logging.TimedRotatingFileHandler`
        if os.path.exists(self.baseFilename):
            try:
                os.remove(self.baseFilename)
            except OSError:
                pass
        try:
            os.symlink(self.currentFileName, self.baseFilename)
        except OSError:
            pass
        return stream


def init_log():

    logger = logging.getLogger(__name__)
    logger.propagate = False
    logger.setLevel(level=logging.INFO)
    if not logger.handlers:
        try:
            handler = TimedRotatingFileHandler("./log/run.log",
                                               "D",
                                               backupCount=100,
                                               encoding='utf-8')
        except FileNotFoundError as exc:
            os.makedirs("./log/")
            return init_log()

        handler.setLevel(logging.DEBUG)
        formatter = logging.Formatter(
            '%(asctime)s - %(funcName)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)

        console = logging.StreamHandler()
        console.setLevel(logging.INFO)

        logger.addHandler(handler)
        logger.addHandler(console)
        
    return logger


def remove_charater(content: str):
    return content.replace('\n', '').replace('\t',
                                             '').replace('\r',
                                                         '').replace(' ', '')


soup = DealSoup().judge
logger = init_log()

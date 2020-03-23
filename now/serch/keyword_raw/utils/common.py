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

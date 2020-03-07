import json
import time
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from bs4 import BeautifulSoup


class OperaChrome(object):
    def __init__(self):
        self.init_chrome()
        self.run()

    def init_chrome(self):
        url = "http://q.10jqka.com.cn/"
        options = webdriver.ChromeOptions()
        options.add_argument("disable-infobars")
        options.add_argument("disable-web-security")
        # options.add_argument("--headless")
        options.add_argument("--start-maximized")
        options.add_argument('--log-level=3')
        options.add_argument('--ignore-certificate-errors')
        prefs = {"profile.managed_default_content_settings.images": 2}
        options.add_experimental_option("prefs", prefs)
        driver = webdriver.Chrome(executable_path="./chromedriver.exe",
                                  options=options)
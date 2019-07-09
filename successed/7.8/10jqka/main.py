import json
import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class OperaChrome(object):
    def __init__(self):
        # self.option = "window.open('{}')"
        self.info_ = pd.DataFrame()
        self.init_chrome()
        self.run()
        self.driver.close()

    def init_chrome(self):
        url = "http://q.10jqka.com.cn/"
        options = webdriver.ChromeOptions()
        options.add_argument("disable-infobars")
        options.add_argument("disable-web-security")
        options.add_argument("--headless")
        options.add_argument("--start-maximized")
        options.add_argument('--log-level=3')
        options.add_argument('--ignore-certificate-errors')
        driver = webdriver.Chrome(
            executable_path="./chromedriver.exe", chrome_options=options)
        driver.get(url)
        WebDriverWait(driver, 90, 0.25).until(
            EC.presence_of_element_located((By.CSS_SELECTOR,
                                            "#maincont > table")))
        item = driver.find_element_by_css_selector("#maincont > table")
        driver.execute_script("arguments[0].scrollIntoView(true);", item)

        self.driver = driver

    def extract_data(self):
        if len(self.info_) == 0:
            self.info_ = pd.read_html(self.driver.page_source)[1]
        else:
            self.info_ = pd.concat(
                [self.info_,
                 pd.read_html(self.driver.page_source)[1]],
                ignore_index=True)

    def run(self):
        while True:
            try:
                # self.driver.find_element_by_css_selector(
                #     "#m-page > a:nth-child(6)").click()
                # time.sleep(1)
                # self.extract_data()
                for index in range(0, 176):
                    if index == 0:
                        pagenum = 6
                    else:
                        pagenum = 8
                    self.extract_data()
                    self.driver.find_element_by_css_selector(
                        "#m-page > a:nth-child({})".format(pagenum)).click()
                    time.sleep(2)

            except NoSuchElementException:
                if index == 175:
                    print("666")
                    self.info_.to_excel(
                        "./data_{}.xlsx".format(
                            time.strftime("%Y-%m-%d-%H-%M-%S",
                                          time.localtime())),
                        index=False)
                    break
                else:
                    print("6")
                    continue
            except StaleElementReferenceException:
                print("777")
                continue
            else:
                self.info_.to_excel(
                    "./data_{}.xlsx".format(
                        time.strftime("%Y-%m-%d-%H-%M-%S", time.localtime())),
                    index=False)
                break

                
def main():
    start_time = time.time()
    OperaChrome()
    print("time is {}".format(time.time() - start_time))


if __name__ == "__main__":
    import os
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    main()

import unittest
import time
from appium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions


class Untitled(unittest.TestCase):
    reportDirectory = 'reports'
    reportFormat = 'xml'
    dc = {}
    testName = 'Untitled'
    driver = None

    def setUp(self):
        self.dc['reportDirectory'] = self.reportDirectory
        self.dc['reportFormat'] = self.reportFormat
        self.dc['testName'] = self.testName
        self.dc['udid'] = 'd19b1585'
        self.dc['appPackage'] = 'com.experitest.ExperiBank'
        self.dc['appActivity'] = '.LoginActivity'
        self.dc['platformName'] = 'android'
        self.driver = webdriver.Remote('http://localhost:4723/wd/hub', self.dc)

    def testUntitled(self):
        self.driver.press_keycode(3)  # home
        self.driver.swipe(297, 1157, -240, 1300, 77)
        self.driver.find_element_by_xpath(
            "xpath=//*[@id='item3' and ./parent::*[./parent::*[(./preceding-sibling::* | ./following-sibling::*)[@contentDescription='亲人']]]]"
        ).click()
        self.driver.find_element_by_xpath(
            "xpath=//*[@id='icon_icon' and @contentDescription='微信']").click()
        self.driver.swipe(515, 510, 602, 1837, 375)
        self.driver.find_element_by_xpath(
            "xpath=//*[@id='yp' and ./parent::*[(./preceding-sibling::* | ./following-sibling::*)[@text='美团外卖']]]"
        ).click()
        self.driver.swipe(425, 1285, 432, 612, 1076)
        self.driver.find_element_by_xpath(
            "xpath=//*[@text='wx2c348cf579062e56:pages/index/index.html:VISIBLE']"
        ).click()
        WebDriverWait(self.driver, 10).until(
            expected_conditions.presence_of_element_located((
                By.XPATH,
                '//*[@text=\'wx2c348cf579062e56:pages/restaurant/restaurant.html:VISIBLE\']'
            )))
        self.driver.find_element_by_xpath(
            "xpath=//*[@text='wx2c348cf579062e56:pages/restaurant/restaurant.html:VISIBLE']"
        ).click()
        WebDriverWait(self.driver, 120).until(
            expected_conditions.presence_of_element_located((
                By.XPATH,
                '//*[@id=\'oo\' and ./parent::*[./parent::*[./parent::*[./parent::*[./parent::*[(./preceding-sibling::* | ./following-sibling::*)[./*[./*[./*[./*[./*[./*[./*[@text=\'wx2c348cf579062e56:pages/restaurant/restaurant.html:INVISIBLE\']]]]]]]]]]]]]]'
            )))
        self.driver.find_element_by_xpath(
            "xpath=//*[@id='oo' and ./parent::*[./parent::*[./parent::*[./parent::*[./parent::*[(./preceding-sibling::* | ./following-sibling::*)[./*[./*[./*[./*[./*[./*[./*[@text='wx2c348cf579062e56:pages/restaurant/restaurant.html:INVISIBLE']]]]]]]]]]]]]]"
        ).click()
        self.driver.find_element_by_xpath("xpath=//*[@text='美团外卖']").click()
        WebDriverWait(self.driver, 120).until(
            expected_conditions.presence_of_element_located(
                (By.XPATH, '//*[@text=\'美团外卖\']')))
        self.driver.find_element_by_xpath("xpath=//*[@text='美团外卖']").click()
        text = self.driver.find_element_by_xpath(
            "(//*[@class='android.view.View']/*/*/*[@text and @class='android.view.View' and (./preceding-sibling::* | ./following-sibling::*)[./*[@class='android.widget.Image']]])[3]"
        ).text
        print(text)

    def tearDown(self):
        self.driver.quit()


class AppiumRun(object):
    def __init__(self):
        pass

    def run(self):
        pass


def main():
    AppiumRun().run()


if __name__ == '__main__':
    main()

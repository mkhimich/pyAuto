import subprocess
import unittest
import os
import datetime

from appium import webdriver
from time import sleep


class WebViewIOSTests(unittest.TestCase):
    def setUp(self):
        # set up appium

        self.process = subprocess.Popen(['appium'],
                                        shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        sleep(10)
        dir_path = os.path.dirname(os.path.realpath(__file__))
        app = dir_path + '/iosapp/' + 'ApiumTest.app'
        app = os.path.abspath(app)
        self.driver = webdriver.Remote(
            command_executor='http://127.0.0.1:4723/wd/hub',
            desired_capabilities={
                'app': app,
                'deviceName': 'iPhone 6s Plus',
                'platformName': 'iOS',
                'platformVersion': '9.3'
            })

    def tearDown(self):
        self.driver.quit()
        self.process.terminate()

    def test_get_url(self):
        add_el = self.driver.find_element_by_xpath('//UIAApplication[1]/UIAWindow[1]/UIANavigationBar[1]/UIAButton[3]')
        add_el.click()
        current_time = str(datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S +0000"))
        sleep(1)
        added_el = self.driver.find_element_by_xpath(
            '//UIAApplication[1]/UIAWindow[1]/UIATableView[1]/UIATableCell[1]/UIAStaticText[1]')
        added_time = str(added_el.get_attribute("value"))
        self.assertEquals(current_time, added_time, "Time is incorrect, expected:" + current_time + " but was " + added_time)


if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(WebViewIOSTests)
    unittest.TextTestRunner(verbosity=2).run(suite)

import subprocess
import unittest
import os
import datetime
import logging

from appium import webdriver
from time import sleep


class WebViewIOSTests(unittest.TestCase):

    def setUp(self):
        # set up appium
        logging.basicConfig(filename='test_' + str(datetime.datetime.utcnow()) + '.log', level=logging.INFO)
        logging.info("Starting appium")
        self.process = subprocess.Popen(['appium'],
                                        shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        sleep(10)
        dir_path = os.path.dirname(os.path.realpath(__file__))
        app = dir_path + '/iosapp/' + 'ApiumTest.ipa'  # for real device use .ipa, for emulator .app
        app = os.path.abspath(app)
        logging.info("Starting driver")
        self.driver = webdriver.Remote(
            command_executor='http://127.0.0.1:4723/wd/hub',
            desired_capabilities={
                'app': app,
                'appName': 'AppiumTest',
                #'deviceName': 'iPhone 6s Plus',  # emulator name
                'deviceName': 'iphone spredfast',  # real device name
                'udid': 'f14bcd4c08d3456b74a45107514217e6ba57c3da',  # udid of real device
                'platformName': 'iOS',
                'platformVersion': '8.4.'
            })

    def tearDown(self):
        logging.info("Test Ended")
        self.driver.quit()
        self.process.terminate()

    def test_get_url(self):
        logging.info("Finding element")
        add_el = self.driver.find_element_by_xpath('//UIAApplication[1]/UIAWindow[1]/UIANavigationBar[1]/UIAButton[3]')
        add_el.click()
        current_time = str(datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S +0000"))
        logging.info("Current time" + current_time)
        sleep(1)
        added_el = self.driver.find_element_by_xpath(
            '//UIAApplication[1]/UIAWindow[1]/UIATableView[1]/UIATableCell[1]/UIAStaticText[1]')
        added_time = str(added_el.get_attribute("value"))
        logging.info("Comparing Time")
        self.assertEquals(current_time, added_time, "Time is incorrect, expected:" + current_time + " but was " + added_time)


if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(WebViewIOSTests)
    unittest.TextTestRunner(verbosity=2).run(suite)

import datetime
import getopt
import logging
import os
import subprocess
import sys
import unittest
from time import sleep

from selenium import webdriver

import properties
import db

PATH = lambda p: os.path.abspath(
    os.path.join(os.path.dirname(__file__), p)
)


class BaseTestCase(unittest.TestCase):
    start_time = datetime.datetime.utcnow()
    logfile = str('test_' + str(start_time) + '.log')
    logging.basicConfig(filename=logfile, level=logging.INFO)
    browser_name = properties.browser
    currentResult = None

    def getDriver(self, browser_type):
        os_type = sys.platform
        logging.info(str(sys.argv))
        if os_type == "darwin":
            os_name = "mac"
        elif os_type == "windows":
            os_name = "win"
        else:
            raise RuntimeError("Os not recognized")
        dir_path = os.path.dirname(os.path.realpath(__file__))
        chromedriver = dir_path + "/webdriver/" + os_name + "/2.22/chromedriver"
        os.environ["webdriver.chrome.driver"] = chromedriver
        if browser_type == "Chrome":
            driver = webdriver.Chrome(chromedriver)
        elif browser_type == "Firefox":
            driver = webdriver.Firefox()
        elif browser_type == "Edge":
            if os_name == "mac":
                raise RuntimeError("Edge is not supported on platform " + os_name)
            driver = webdriver.Edge
        elif browser_type == "IE":
            if os_name == "mac":
                raise RuntimeError("IE is not supported on platform " + os_name)
            driver = webdriver.Ie()
        elif browser_type == "Safari":
            if os_name == "win":
                raise RuntimeError("Safari is not supported on platform " + os_name)
            driver = webdriver.Safari()
        elif browser_type == "Android":
            driver = self.getAndroidDriver()
        elif browser_type == "IOS":
            driver = self.getIOSDriver()
        else:
            raise RuntimeError("Browser not supported")
        return driver

    def getIOSDriver(self):
        # set up appium
        logging.info("Starting appium for IOS")
        path = PATH('../pyAuto/iosapp/ApiumTest.ipa')  # for real device use .ipa, for emulator .app
        desired_caps = {}
        desired_caps['app'] = path
        desired_caps['appName'] ='AppiumTest'
        desired_caps['deviceName'] = properties.iosDeviceName
        #desired_caps['udid'] = properties.iosDeviceUDID
        desired_caps['platformName'] = 'iOS'
        desired_caps['platformVersion'] = '9.3'
        logging.info("Starting driver")
        self.process = subprocess.Popen(['appium'],
                                        shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        sleep(10)
        driver = webdriver.Remote('http://localhost:4723/wd/hub', desired_caps)
        return driver

    def getAndroidDriver(self):
        logging.info("Starting appium for Android")
        path = PATH('../androidapp/ApiDemos-debug.apk')
        desired_caps = {}
        desired_caps['device'] = 'Android'
        desired_caps['platformName'] = 'Android'
        desired_caps['platformVersion'] = '4.4'
        desired_caps['deviceName'] = 'Android'
        desired_caps['udid'] = '5e1b87f2'

        desired_caps['app'] = path
        self.process = subprocess.Popen([
            'appium'],
            shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        sleep(10)
        driver = webdriver.Remote('http://localhost:4723/wd/hub', desired_caps)
        return driver

    def getParams(self):
        opts = ''
        argv = sys.argv[1:]
        browser_name = ''
        try:
            opts, args = getopt.getopt(argv, "b:")
        except getopt.GetoptError:
            logging.info('no params, using browser from properties')
        for opt, arg in opts:
            if opt in "-b":
                browser_name = arg
        if not browser_name:
            browser_name = properties.browser
        logging.info('Selected browser is ' + browser_name)
        return browser_name

    def run(self, result=None):
        self.currentResult = result  # remember result for use in tearDown
        unittest.TestCase.run(self, result)  # call superclass run method

    def setUp(self):
        logging.info('Getting webdriver')
        self.driver = self.getDriver(self.getParams())

    def tearDown(self):
        errors = self.currentResult.errors
        failures = self.currentResult.failures
        if (len(errors) == 0) & (len(failures) == 0):
            result = "passed"
        else:
            result = "failed"
        message = str(errors) + "\n" + str(failures)
        db.insert_result(self._testMethodName, self.browser_name, self.start_time,
                         result, message)

        logging.info('Finishing test')
        self.driver.quit()
        try:
            self.process.terminate()
            subprocess.Popen(['killall qemu-system-i386'], shell=True)
        except AttributeError:
            logging.info('Appium process terminated')


if __name__ == "__main__":
    unittest.main()

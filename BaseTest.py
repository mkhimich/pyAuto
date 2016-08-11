import datetime
import getopt
import logging
import os
import sys
import unittest

from selenium import webdriver

import Properties
import db


class BaseTestCase(unittest.TestCase):
    start_time = datetime.datetime.utcnow()
    logfile = str('test_' + str(start_time) + '.log')
    logging.basicConfig(filename=logfile, level=logging.INFO)
    browser_name = Properties.browser
    currentResult = None

    @staticmethod
    def getDriver(browser_type):
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
                raise RuntimeError("Safary is not supported on platform " + os_name)
            driver = webdriver.Safari()
        else:
            raise RuntimeError("Browser not supported")
        return driver

    def getParams(self):
        argv = sys.argv[1:]
        browser_name = ''
        try:
            opts, args = getopt.getopt(argv, "b:")
        except getopt.GetoptError:
            logging.info('no params, using browser from properties')
        for opt, arg in opts:
            if opt in "-b":
                browser_name = arg
        logging.info('Selected browser is ' + browser_name)
        return browser_name

    def run(self, result=None):
        self.currentResult = result  # remember result for use in tearDown
        unittest.TestCase.run(self, result)  # call superclass run method

    def setUp(self):
        logging.info('Getting webdriver')
        self.driver = self.getDriver(self.getParams())

    def tearDown(self):
        ok = self.currentResult.wasSuccessful()
        errors = self.currentResult.errors
        failures = self.currentResult.failures
        if ok:
            result = "passed"
        else:
            result = "failed"
        message = str(errors) + "\n" + str(failures)
        db.insert_result(self._testMethodName, self.browser_name, self.start_time,
                         result, message)

        logging.info('Finishing test')
        self.driver.close()


if __name__ == "__main__":
    unittest.main()

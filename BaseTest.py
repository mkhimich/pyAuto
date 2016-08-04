import getopt
import os
import sys
import unittest
import Properties

from selenium import webdriver


class BaseTestCase(unittest.TestCase):
    @staticmethod
    def getDriver(browser_type):
        os_type = sys.platform
        print(str(sys.argv))
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
        browserName = ''
        try:
            opts, args = getopt.getopt(argv, "b:")
        except getopt.GetoptError:
            print('no params, using browser from properties')
        for opt, arg in opts:
            if opt in "-b":
                browserName = arg
        if not browserName:
            browserName = Properties.browser
        print('Selected browser is ', browserName)
        return browserName

    def setUp(self):
        self.driver = self.getDriver(self.getParams())

    def tearDown(self):
        self.driver.close()


if __name__ == "__main__":
    unittest.main()

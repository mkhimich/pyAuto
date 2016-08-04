import unittest
import os

from selenium import webdriver


class BaseTestCase(unittest.TestCase):
    def setUp(self):
        dir_path = os.path.dirname(os.path.realpath(__file__))
        chromedriver = dir_path + "/webdriver/mac/2.22/chromedriver"
        print chromedriver
        os.environ["webdriver.chrome.driver"] = chromedriver
        self.driver = webdriver.Chrome(chromedriver)

    def tearDown(self):
        self.driver.close()


if __name__ == "__main__":
    unittest.main()

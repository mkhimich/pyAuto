import unittest

from selenium import webdriver


class BaseTestCase(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Firefox()

    def tearDown(self):
        self.driver.close()


if __name__ == "__main__":
    unittest.main()

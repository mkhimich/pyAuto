import unittest
import datetime
import logging

from time import sleep

from basetest import BaseTestCase


class WebViewIOSTests(BaseTestCase):

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

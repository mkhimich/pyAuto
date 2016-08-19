import datetime
import logging

from time import sleep


def test_get_url(setup):
    logging.info("Finding element")
    add_el = setup.driver.find_element_by_xpath('//UIAApplication[1]/UIAWindow[1]/UIANavigationBar[1]/UIAButton[3]')
    add_el.click()
    current_time = str(datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S +0000"))
    logging.info("Current time" + current_time)
    sleep(1)
    added_el = setup.driver.find_element_by_xpath(
        '//UIAApplication[1]/UIAWindow[1]/UIATableView[1]/UIATableCell[1]/UIAStaticText[1]')
    added_time = str(added_el.get_attribute("value"))
    logging.info("Comparing Time")
    assert current_time == added_time, "Time is incorrect, expected:" + current_time + " but was " + added_time

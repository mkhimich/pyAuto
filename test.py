# coding=utf-8
import pytest
from selenium.webdriver.common.keys import Keys

import page
import properties
import time
from time import sleep


@pytest.mark.skipif(not properties.suite == 'smoke',
                    reason="incorrect suite")
def test_search_in_spice_web(setup):
    """
    Tests search feature. Searches for the word "Спайсы" then verified that no results show up.
    Note that it does not look for any particular text in search results page. This test verifies that
    the results were not empty.
    """
    print("Start 1 " + str(time.localtime()))
    # setup.driver.get("https://10.129.140.24/")
    setup.driver.get("https://10.129.140.24/")
    # Load the main page.
    main_page = page.MainPage(setup.driver)

    setup.driver.find_element_by_id("//aasd")
    # Checks if the word "Спайсы" is in title
    assert main_page.is_title_matches(), "title doesn't match."
    # Click page example button
    main_page.click_page_example()
    main_page.search_text_element = u"Спайсы" + Keys.ENTER
    search_results_page = main_page.SearchResultsPage(setup.driver)
    # Verifies that the results page is not empty
    assert search_results_page.is_results_found(), "Some results found."
    sleep(20)
    print("End 1 " + str(time.localtime()))


@pytest.mark.skip(reason="no way of currently testing this")
def test_my_skipped_test(setup):
    setup.driver.get("https://10.129.140.24/")


@pytest.mark.skipif(not properties.suite == 'smoke',
                    reason="incorrect suite")
def test_my_grouped(setup):
    print("Start 2 " + str(time.localtime()))
    setup.driver.get("https://10.129.140.24/")
    sleep(0)
    print("End 2 " + str(time.localtime()))

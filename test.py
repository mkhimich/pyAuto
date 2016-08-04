# coding=utf-8
import unittest

from selenium import webdriver
from selenium.webdriver.common.keys import Keys

import page


class PythonOrgSearch(unittest.TestCase):
    """A sample test class to show how page object works"""

    def setUp(self):
        self.driver = webdriver.Chrome("./webdriver/mac/2.22/chromedriver")
        self.driver.get("https://10.129.140.24/")

    def test_search_in_spice_web(self):
        """
        Tests search feature. Searches for the word "Спайсы" then verified that no results show up.
        Note that it does not look for any particular text in search results page. This test verifies that
        the results were not empty.
        """

        # Load the main page.
        main_page = page.MainPage(self.driver)
        # Checks if the word "Спайсы" is in title
        assert main_page.is_title_matches(), "title doesn't match."
        # Click page example button
        main_page.click_page_example()
        main_page.search_text_element = u"Спайсы" + Keys.ENTER
        search_results_page = main_page.SearchResultsPage(self.driver)
        # Verifies that the results page is not empty
        assert search_results_page.is_results_found(), "Some results found."

    def tearDown(self):
        self.driver.close()


if __name__ == "__main__":
    unittest.main()

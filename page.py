# coding=utf-8
from selenium.webdriver.common.by import By

from element import BasePageElement
from locators import MainPageLocators


class SearchTextElement(BasePageElement):
    """This class gets the search text from the specified locator"""

    # The locator for search box where search string is entered
    locator = '.searchform input'
    by = By.CSS_SELECTOR


class BasePage(object):
    """Base class to initialize the base page that will be called from all pages"""

    def __init__(self, driver):
        self.driver = driver
        self.inject_jquery(driver)

    @staticmethod
    def inject_jquery(driver):
        with open('jquery/jquery.min.js', 'r') as jquery_js:
            jquery = jquery_js.read()  # read the jquery from a file
            driver.execute_script(jquery)


class MainPage(BasePage):
    """Home page action methods come here."""

    search_text_element = SearchTextElement()

    def is_title_matches(self):
        """Verifies that the hardcoded text "Спайсы Соли Миксы" appears in page title"""
        return u"Спайсы Соли Миксы" in self.driver.title

    def click_page_example(self):
        """Triggers the search"""
        element = self.driver.find_element(*MainPageLocators.PAGE_EXAMPLE_BUTTON)
        element.click()

    class SearchResultsPage(BasePage):
        """Search results page action methods come here"""

        def is_results_found(self):
            # Probably should search for this text in the specific page
            # element, but as for now it works fine
            return "Sorry no post matched your criteria!" in self.driver.page_source

from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions


class BasePage(object):
    def __init__(self, factory):
        self.factory = factory

    def is_displayed(self):
        raise NotImplementedError("Override the is_displayed method in your page class")

    def wait_if_element_visible(self, element):
        try:
            self.factory.wait.until(expected_conditions.visibility_of(element))
            return True
        except TimeoutException:
            return False

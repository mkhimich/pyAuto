from selenium.webdriver.support.ui import WebDriverWait


class BasePageElement(object):
    """Base page class that is initialized on every page object class."""

    def __set__(self, obj, value):
        """Sets the text to the value supplied"""
        driver = obj.driver
        WebDriverWait(driver, 100).until(
            lambda driver: driver.find_element(self.by, self.locator))
        driver.find_element(self.by, self.locator).send_keys(value)

    def __get__(self, obj):
        """Gets the text of the specified object"""
        driver = obj.driver
        WebDriverWait(driver, 100).until(
            lambda driver: driver.find_element(self.by, self.locator))
        element = driver.find_element(self.by, self.locator)
        return element.get_attribute("value")

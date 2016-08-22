from webtest.pages.base_page import BasePage


class LandPage(BasePage):
    def is_displayed(self):
        raise NotImplementedError("Override the is_displayed method in your page class")


class NotesPage(LandPage):
    def is_displayed(self):
        return self.wait_if_element_visible(self.factory.driver.find_element_by_xpath("//span[@class='gb_wc'][text()='Notes']"))
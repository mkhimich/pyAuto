from webtest.elements.simple_elements import Button
from webtest.pages.base_page import BasePage


class LandPage(BasePage):
    def is_displayed(self):
        raise NotImplementedError("Override the is_displayed method in your page class")

    def get_menu_button(self):
        return Button(self.factory.driver.find_element_by_xpath("//*[@aria-label='Main menu'"))

    def get_create_new_label_menu_item(self):
        return Button(self.factory.driver.find_element_by_xpath("//*[text()='Create new label']"))

class NotesPage(LandPage):
    def is_displayed(self):
        return self.wait_if_element_visible(self.factory.driver.find_element_by_xpath("//span[@class='gb_wc'][text()='Notes']"))
from selenium.webdriver.common.by import By

from webtest.elements.simple_elements import Button
from webtest.elements.simple_elements import EditField
from webtest.elements.simple_elements import Text
from webtest.pages.base_page import BasePage


class LandPage(BasePage):
    def is_displayed(self):
        raise NotImplementedError("Override the is_displayed method in your page class")

    def get_menu_button(self):
        return Button(self.factory.driver.find_element_by_xpath("//*[@aria-label='Main menu']"))

    def get_create_new_label_menu_item(self):
        return Button(self.factory.driver.find_element_by_xpath("//*[text()='Create new label']"))

    def click_new_label_menu_item(self):
        self.get_create_new_label_menu_item().click()
        return self.factory.get_edit_labels_dialog()

    def get_label_menu_item(self, name):
        return Button(self.factory.driver.find_element_by_xpath("//a/span[text()='" + name + "']"))

    def if_label_menu_item_present(self, name):
        self.wait_if_element_present((By.XPATH, "//a/span[text()='" + name + "']"))


class NotesPage(LandPage):
    def is_displayed(self):
        return self.wait_if_element_visible(
            self.factory.driver.find_element_by_xpath("//span[@class='gb_wc'][text()='Notes']"))


class EditLabelsDialog(BasePage):
    def is_displayed(self):
        return self.wait_if_element_visible(self.get_edit_labels_dialog_title().element)

    def get_new_label_input(self):
        return EditField(self.factory.driver.find_element_by_xpath("//*[@aria-label='Create new label']"))

    def get_create_label_button(self):
        return Button(self.factory.driver.find_element_by_xpath("//*[@aria-label='Create label']"))

    def get_first_delete_label_button(self):
        return Button(self.factory.driver.find_element_by_xpath("//*[@aria-label='Delete label']"))

    def get_edit_labels_dialog_title(self):
        return Text(self.factory.driver.find_element_by_xpath("//div[text()='Edit labels']"))

    def get_done_button(self):
        return Button(self.factory.driver.find_elements_by_xpath("//div[text()='Done']")[1])

    def create_label(self, name):
        self.get_new_label_input().set_text(name)
        self.get_create_label_button().click()

    def get_first_edit_label_input(self):
        return EditField(self.factory.driver.find_element_by_xpath("//*[@aria-label='Enter label name']"))

    def delete_first_label(self):
        self.get_first_delete_label_button().click()
        self.get_delete_confirm_button().click()

    def get_delete_confirm_button(self):
        return Button(self.factory.driver.find_element_by_xpath("//div[text()='Delete']"))

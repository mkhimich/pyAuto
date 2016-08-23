from webtest.elements.simple_elements import Button
from webtest.elements.simple_elements import EditField
from webtest.pages.base_page import BasePage


class GoogleLoginPage(BasePage):
    def is_displayed(self):
        return self.get_next_button().is_displayed()

    def get_login_input(self):
        return EditField(self.factory.driver.find_element_by_id("Email"))

    def get_next_button(self):
        return Button(self.factory.driver.find_element_by_id("next"))

    def input_login_and_next(self, login):
        self.get_login_input().set_text(login)
        self.get_next_button().click()
        return self.factory.get_google_password_page()


class GooglePasswordPage(BasePage):
    def get_password_input(self):
        return EditField(self.factory.driver.find_element_by_id("Passwd"))

    def get_sign_in_button(self):
        return Button(self.factory.driver.find_element_by_id("signIn"))

    def input_password_and_submit(self, login):
        from time import sleep
        sleep(3)
        self.get_password_input().set_text(login)
        self.get_sign_in_button().click()
        return self.factory.get_notes_page()

    def is_displayed(self):
        return self.wait_if_element_visible(self.get_sign_in_button().element)

import unittest

from baseTest import BaseTestCase


class TestSimpleAndroidTests(BaseTestCase):

    def test_caption(self):
        el = self.driver.find_element_by_android_uiautomator("new UiSelector().text(\"Заметки\")")

        assert el.is_displayed()

    def test_go_to_reminders(self):
        menu = self.driver.find_element_by_android_uiautomator(
            "new UiSelector().description(\"Открыть панель навигации\")")
        menu.click()

        reminders_menu_item = self.driver.find_element_by_id('com.google.android.keep:id/drawer_navigation_reminders')
        reminders_menu_item.click()

        reminders_caption = self.driver.find_element_by_android_uiautomator("new UiSelector().text(\"Напоминания\")")

        assert reminders_caption.is_displayed()

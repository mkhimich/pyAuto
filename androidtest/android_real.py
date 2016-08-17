import os
import subprocess
import unittest
from time import sleep

from appium import webdriver

# Returns abs path relative to this file and not cwd
PATH = lambda p: os.path.abspath(
    os.path.join(os.path.dirname(__file__), p)
)


class TestSimpleAndroidTests(unittest.TestCase):
    def setUp(self):
        path = PATH('../androidapp/keep.apk')
        desired_caps = {}
        desired_caps['device'] = 'Android'
        desired_caps['platformName'] = 'Android'
        desired_caps['platformVersion'] = '6.0.1'
        desired_caps['deviceName'] = 'Nexus 5x'

        desired_caps['app'] = path
        self.process = subprocess.Popen([
            'appium --debug-log-spacing --automation-name "Appium" --platform-name "Android" --platform-version "4.4" --app "' + path + '"'],
            shell=True)
        sleep(5)
        self.driver = webdriver.Remote('http://localhost:4723/wd/hub', desired_caps)

    def tearDown(self):
        # end the session
        self.driver.quit()
        self.process.terminate()

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

import unittest

# Returns abs path relative to this file and not cwd
from baseTest import BaseTestCase


class SimpleAndroidTests(BaseTestCase):
    def test_find_elements(self):
        el = self.driver.find_element_by_accessibility_id('Graphics')
        el.click()
        el = self.driver.find_element_by_accessibility_id('Arcs')
        assert el is not None

        self.driver.back()

        el = self.driver.find_element_by_accessibility_id("App")
        assert el is not None

        els = self.driver.find_elements_by_android_uiautomator("new UiSelector().clickable(true)")
        assert 12 >= len(els)

        self.driver.find_element_by_android_uiautomator('text("API Demos")')

    def test_simple_actions(self):
        el = self.driver.find_element_by_accessibility_id('Graphics')
        el.click()

        el = self.driver.find_element_by_accessibility_id('Arcs')
        el.click()

        self.driver.find_element_by_android_uiautomator('new UiSelector().text("Graphics/Arcs")')


if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(SimpleAndroidTests)
    unittest.TextTestRunner(verbosity=2).run(suite)

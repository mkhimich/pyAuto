import allure
import pytest
import logging


class SoftAssert:
    def __init__(self, driver, logger):
        self.driver = driver
        self.logger = logger
        self.failure_count = 0
        self.report = {}

    def assert_true(self, message, expected):
        try:
            assert expected
        except AssertionError as e:
            self.driver.get_screenshot_as_file("foo.png")
            self.logger.warning(message + " " + expected + " is false")
            self.logger.warning(e)
            self.failure_count += 1
            self.report[self.failure_count] = e
            allure.attach(e)

    def assert_equals(self, message, actual, expected):
        try:
            assert actual == expected
        except AssertionError as e:
            self.driver.get_screenshot_as_file("bar.png")
            self.logger.warning(message + ", expected: " + expected+", actual: " + actual)
            self.logger.warning(e)
            self.failure_count += 1
            self.report[self.failure_count] = e
            allure.attach(e)

    def collect_results(self):
        if self.failure_count == 0:
            self.report[0] = "passed"
        else:
            self.report[0] = "failed"
        return self.report

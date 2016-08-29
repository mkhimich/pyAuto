import datetime
import getopt
import logging
import os
import subprocess
import sys
import pytest
from time import sleep

from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait

import properties
import db
import soft_assert

SCREENSHOTS = "screenshots"

FAILED = "failed"

PATH = lambda p: os.path.abspath(
    os.path.join(os.path.dirname(__file__), p)
)


class PageFactory(object):
    def __init__(self, driver, logger):
        self.driver = driver
        self.logger = logger
        self.soft_assert = soft_assert.SoftAssert(self.driver, self.logger)

    def get_first_page(self):
        self.driver.get(properties.app_url)
        return self.get_google_login_page()

    def get_google_login_page(self):
        from webtest.pages.google_login_pages import GoogleLoginPage
        return GoogleLoginPage(self)

    def get_google_password_page(self):
        from webtest.pages.google_login_pages import GooglePasswordPage
        return GooglePasswordPage(self)

    def get_notes_page(self):
        from webtest.pages.keep_pages import NotesPage
        return NotesPage(self)

    def get_edit_labels_dialog(self):
        from webtest.pages.keep_pages import EditLabelsDialog
        return EditLabelsDialog(self)


def get_driver(browser_type):
    os_type = sys.platform
    logging.info(str(sys.argv))
    if os_type == "darwin":
        os_name = "mac"
    elif os_type == "windows":
        os_name = "win"
    else:
        raise RuntimeError("Os not recognized")
    dir_path = os.path.dirname(os.path.realpath(__file__))
    chromedriver = dir_path + "/webdriver/" + os_name + "/2.22/chromedriver"
    os.environ["webdriver.chrome.driver"] = chromedriver
    if browser_type == "Chrome":
        driver = webdriver.Chrome(chromedriver)
    elif browser_type == "Firefox":
        driver = webdriver.Firefox()
    elif browser_type == "Edge":
        if os_name == "mac":
            raise RuntimeError("Edge is not supported on platform " + os_name)
        driver = webdriver.Edge
    elif browser_type == "IE":
        if os_name == "mac":
            raise RuntimeError("IE is not supported on platform " + os_name)
        driver = webdriver.Ie()
    elif browser_type == "Safari":
        if os_name == "win":
            raise RuntimeError("Safari is not supported on platform " + os_name)
        driver = webdriver.Safari()
    elif browser_type == "Android":
        driver = get_android_driver()
    elif browser_type == "IOS":
        driver = get_ios_driver()
    else:
        raise RuntimeError("Browser not supported")
    driver.implicitly_wait(properties.implicit_wait)
    return driver


def get_ios_driver():
    # set up appium
    logging.info("Starting appium for IOS")
    logging.info("Starting driver")
    # self.process = subprocess.Popen(['appium'],
    #                                 shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    # sleep(10)
    from appium import webdriver
    driver = webdriver.Remote('http://10.129.140.95:4723/wd/hub', properties.ios_desired_caps)
    return driver


def get_android_driver():
    logging.info("Starting appium for Android")
    path = PATH('androidapp/keep.apk')
    desired_caps = {'device': 'Android',
                    'platformName': 'Android',
                    'platformVersion': '6.0.1',
                    'deviceName': 'Android',
                    'app': path}
    logging.info("Starting driver")
    # self.process = subprocess.Popen([
    #     'appium'],
    #     shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    # sleep(10)
    from appium import webdriver
    driver = webdriver.Remote('http://localhost:4723/wd/hub', desired_caps)
    return driver


def get_params():
    opts = ''
    argv = sys.argv[1:]
    browser_name = ''
    try:
        opts, args = getopt.getopt(argv, "b:")
    except getopt.GetoptError:
        logging.info('no params, using browser from properties')
    for opt, arg in opts:
        if opt in "-b":
            browser_name = arg
    if not browser_name:
        browser_name = properties.browser
        logging.info('Selected browser is ' + browser_name)
    return browser_name


# def run(self, result=None):
#     self.currentResult = result  # remember result for use in tearDown
#     unittest.TestCase.run(self, result)  # call superclass run method


def setup_logger(start_time):
    # logfile = str('test_' + str(start_time) + '.log')
    # logging.basicConfig(filename=logfile, level=logging.INFO)
    logger = logging.getLogger('DSL logger')
    logger.setLevel(logging.INFO)
    ch = logging.StreamHandler()
    ch.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    ch.setFormatter(formatter)
    logger.addHandler(ch)
    # self.browser_name = properties.browser
    # self.currentResult = None
    return logger


@pytest.mark.hookwrapper
@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    # execute all other hooks to obtain the report object
    pytest_html = item.config.pluginmanager.getplugin('html')
    outcome = yield
    rep = outcome.get_result()
    extra = getattr(rep, 'extra', [])
    setattr(item, "rep_" + rep.when, rep)
    # we only look at actual failing test calls, not setup/teardown
    if rep.when == "call":
        extra.append(pytest_html.extras.image(item.funcargs['setup'].driver.get_screenshot_as_base64()))
        rep.extra = extra  # adds screenshot to the report

#todo fix soft assert check
        # if rep.outcome == "passed":
        #     rep.outcome = str(item.funcargs['setup'].soft_assert.collect_results().get(0))
        #     if rep.outcome == "failed":
        #         from py._code.code import ReprExceptionInfo
        #         from py._code.code import ReprFileLocation
        #         rep.longrepr = ReprExceptionInfo("All hail dynamic typification",
        #                                          ReprFileLocation(0, "", "Some Soft Asserts failed. TBD: get some exception messages here"))
        mode = "a" if os.path.exists("failures") else "w"
        with open("failures", mode) as f:
            # let's also access a fixture for the fun of it
            if "tmpdir" in item.fixturenames:
                extra = " (%s)" % item.funcargs["tmpdir"]
            else:
                extra = ""

            f.write('Test in suite ' + rep.nodeid + ' has failed' + extra + "\n")
            # db.insert_result(rep.nodeid, properties.browser_name, '', 'failed', extra)


@pytest.fixture()
def setup(request):
    start_time = datetime.datetime.utcnow()
    logger = setup_logger(start_time)
    browser_name = get_params()
    logging.info('Getting driver')
    factory = PageFactory(get_driver(browser_name), logger)
    factory.wait = WebDriverWait(factory.driver, properties.implicit_wait)

    def tear_down():
        result = "passed"
        message = ""
        if request.node.rep_setup.failed:
            print("setting up a test failed!", request.node.nodeid)
            result = FAILED
            message = request.node.rep_setup.longrepr.reprcrash.message
        elif request.node.rep_setup.passed:
            if request.node.rep_call.failed:
                print("executing test failed", request.node.nodeid)
                result = FAILED
                message = request.node.rep_call.longrepr.reprcrash.message

        if result == FAILED:
            if not factory.driver.get_screenshot_as_file("SCREENSHOTS" + "/"
                                                                 + request.node.nodeid.replace("/", "..")
                                                                 + "_"
                                                                 + str(start_time) + ".png"):
                logger.warn("Couldn't take a screenshot for " + request.node.nodeid)

        factory.driver.quit()

        try:
            db.insert_result(request.node.nodeid, browser_name, start_time,
                             result, message)
        except db.DatabaseError as e:
            logger.error("Failed to log to db with exception " + str(e))

        logging.info('Finishing test')
        # try:
        #     factory.process.terminate()
        #     subprocess.Popen(['killall qemu-system-i386'], shell=True)
        # except AttributeError:
        #     factory.logger.info('Appium process terminated')

    request.addfinalizer(tear_down)

    return factory


@pytest.fixture(autouse=True, scope="session")
def before_suite():
    """This is launched before all the tests"""
    try:
        os.mkdir(SCREENSHOTS)
    except OSError as e:
        print(SCREENSHOTS + " folder was not created because of " + str(e))

    import selenium

    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

    from selenium.webdriver.common.by import By

    # Monkey patching is real!

    original_find_element = selenium.webdriver.remote.webdriver.WebDriver.find_element

    def find_element_with_logging(self, by=By.ID, value=None):
        selector = str(by) + " :: " + value
        logging.info("Looking for element by ___ " + selector)

        element = original_find_element(self, by, value)

        setattr(element, "selector", selector)

        return element

    selenium.webdriver.remote.webdriver.WebDriver.find_element = find_element_with_logging

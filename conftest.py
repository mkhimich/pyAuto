import datetime
import getopt
import logging
import os
import subprocess
import sys
import pytest
from time import sleep

from selenium import webdriver

import properties
import db

PATH = lambda p: os.path.abspath(
    os.path.join(os.path.dirname(__file__), p)
)


class PageFactory(object):
    def __init__(self, driver, logger):
        self.driver = driver
        self.logger = logger


def get_driver(logger, browser_type):
    os_type = sys.platform
    logger.info(str(sys.argv))
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
        driver = get_android_driver(logger)
    elif browser_type == "IOS":
        driver = get_ios_driver(logger)
    else:
        raise RuntimeError("Browser not supported")
    return driver


def get_ios_driver(logger):
    # set up appium
    logger.info("Starting appium for IOS")
    path = PATH('../pyAuto/iosapp/ApiumTest.ipa')  # for real device use .ipa, for emulator .app
    desired_caps = {'app': path,
                    'appName': 'AppiumTest',
                    'deviceName': properties.iosDeviceName,
                    'platformName': 'iOS',
                    'platformVersion': '9.3'}
    # desired_caps['udid'] = properties.iosDeviceUDID
    logger.info("Starting driver")
    # self.process = subprocess.Popen(['appium'],
    #                                 shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    # sleep(10)
    from appium import webdriver
    driver = webdriver.Remote('http://localhost:4723/wd/hub', desired_caps)
    return driver


def get_android_driver(logger):
    logger.info("Starting appium for Android")
    path = PATH('androidapp/keep.apk')
    desired_caps = {'device': 'Android',
                    'platformName': 'Android',
                    'platformVersion': '6.0.1',
                    'deviceName': 'Android',
                    'app': path}

    # self.process = subprocess.Popen([
    #     'appium'],
    #     shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    # sleep(10)
    from appium import webdriver
    driver = webdriver.Remote('http://localhost:4723/wd/hub', desired_caps)
    return driver


def get_params(logger):
    opts = ''
    argv = sys.argv[1:]
    browser_name = ''
    try:
        opts, args = getopt.getopt(argv, "b:")
    except getopt.GetoptError:
        logger.info('no params, using browser from properties')
    for opt, arg in opts:
        if opt in "-b":
            browser_name = arg
    if not browser_name:
        browser_name = properties.browser
        logger.info('Selected browser is ' + browser_name)
    return browser_name


# def run(self, result=None):
#     self.currentResult = result  # remember result for use in tearDown
#     unittest.TestCase.run(self, result)  # call superclass run method


def setup_logger(start_time):
    logfile = str('test_' + str(start_time) + '.log')
    logging.basicConfig(filename=logfile, level=logging.INFO)
    logger = logging.getLogger('simple_example')
    logger.setLevel(logging.INFO)
    ch = logging.StreamHandler()
    ch.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    ch.setFormatter(formatter)
    logger.addHandler(ch)
    # self.browser_name = properties.browser
    # self.currentResult = None
    return logger


@pytest.fixture()
def setup(request):
    start_time = datetime.datetime.utcnow()
    logger = setup_logger(start_time)
    browser_name = get_params(logger)
    factory = PageFactory(get_driver(logger, browser_name), logger)
    logger.info('Getting webdriver')

    def tear_down():
        result = "passed"
        message = ""
        if request.node.rep_setup.failed:
            print("setting up a test failed!", request.node.nodeid)
            result = "failed"
            message = request.node.rep_setup.longrepr.reprcrash.message
        elif request.node.rep_setup.passed:
            if request.node.rep_call.failed:
                print("executing test failed", request.node.nodeid)
                result = "failed"
                message = request.node.rep_call.longrepr.reprcrash.message

        db.insert_result(request.node.nodeid, browser_name, start_time,
                         result, message)

        factory.logger.info('Finishing test')
        factory.driver.quit()
        # try:
        #     factory.process.terminate()
        #     subprocess.Popen(['killall qemu-system-i386'], shell=True)
        # except AttributeError:
        #     factory.logger.info('Appium process terminated')

    request.addfinalizer(tear_down)

    return factory


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    # execute all other hooks to obtain the report object
    outcome = yield
    rep = outcome.get_result()

    # set an report attribute for each phase of a call, which can
    # be "setup", "call", "teardown"

    setattr(item, "rep_" + rep.when, rep)

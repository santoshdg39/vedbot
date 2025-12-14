import os
import platform
import shutil

import allure
import pytest
import logging as py_logging
from allure_commons.types import AttachmentType

from Config import global_var

if platform.system() == "Windows":
    path_divider = "\\"
else:
    path_divider = "/"


@pytest.fixture(scope="session")
def rp_logger():
    logger = py_logging.getLogger(__name__)
    py_logging.basicConfig(level=py_logging.INFO, format='%(message)s')
    return logger


def pytest_addoption(parser):
    parser.addoption("--browser", action="store", default="chrome", help="browser")
    parser.addoption("--headless", action="store", default="false", help="Run browser in headless mode")
    parser.addoption("--allureReport", action="store", default="true", help="Enable Allure report")


@pytest.hookimpl()
def pytest_configure(config):
    allure_report = config.getoption("--allureReport")

    if allure_report.lower() == "true":
        if os.path.exists(global_var.ALLURE_RESULTS_PATH):
            shutil.rmtree(global_var.ALLURE_RESULTS_PATH)

        config.option.allure_report_dir = global_var.ALLURE_RESULTS_PATH


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item):
    outcome = yield
    report = outcome.get_result()

    if report.when == "call" and report.failed:
        driver = item.funcargs.get("init_driver")
        if driver:
            allure.attach(
                driver.get_screenshot_as_png(),
                name="Failure Screenshot",
                attachment_type=AttachmentType.PNG
            )


def _capture_screenshot(name, driver):
    driver.save_screenshot(name)

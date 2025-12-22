import os
import platform
import shutil
import time

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
        driver = getattr(item.instance, "driver", None)

        # Try to get driver from fixture if class-level driver not found
        for arg in item.funcargs.values():
            if hasattr(arg, "driver"):
                driver = arg.driver
                break

        if driver is None:
            print(f"Driver not found for test: {item.name}")
            return

        screenshots_dir = os.path.join(global_var.ROOT_DIR, "Artifacts", "screenshots")
        os.makedirs(screenshots_dir, exist_ok=True)

        timestamp = int(time.time())
        screenshot_path = os.path.join(screenshots_dir, f"{item.name}_{timestamp}.png")

        driver.save_screenshot(screenshot_path)
        print(f"Screenshot saved at: {screenshot_path}")

        allure.attach(
            driver.get_screenshot_as_png(),
            name=f"Failure Screenshot - {item.name}",
            attachment_type=AttachmentType.PNG
        )


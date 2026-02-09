import os
import platform
import shutil
import time

import allure
import pytest
import logging as py_logging
from allure_commons.types import AttachmentType

from Config import global_var
from HelperMethods.csv_helper import CSVHelper
from HelperMethods.test_data_generator_helper import DataGenerator

if platform.system() == "Windows":
    path_divider = "\\"
else:
    path_divider = "/"


@pytest.fixture(scope="session")
def rp_logger():
    logger = py_logging.getLogger("Ved_Bot")
    logger.setLevel(py_logging.INFO)

    if not logger.handlers:
        console_handler = py_logging.StreamHandler()
        formatter = py_logging.Formatter(
            "%(asctime)s - %(levelname)s - %(message)s"
        )
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)

    logger.propagate = False
    return logger


def pytest_addoption(parser):
    parser.addoption("--browser", action="store", default="chrome", help="browser")
    parser.addoption("--headless", action="store", default="false", help="Run browser in headless mode")
    parser.addoption("--allureReport", action="store", default="true", help="Enable Allure report")
    parser.addoption("--env", action="store", default="local", help="Test environment to use: local, sanity, regression")


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


@pytest.fixture(scope="function")
def prepare_employee_csv_data():
    # Create / clear Excel file
    CSVHelper.clear_and_create(
        global_var.IMPORT_EMPLOYEE_CSV_PATH
    )

    # Generate test employee data
    employee_data = [DataGenerator.create_user()]

    # Add data rows to Excel
    CSVHelper.add_rows(
        global_var.IMPORT_EMPLOYEE_CSV_PATH,
        employee_data
    )

    # Pass the file path to the test
    yield global_var.IMPORT_EMPLOYEE_CSV_PATH

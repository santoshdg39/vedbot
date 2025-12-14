import pytest

from HelperMethods.config_parser import ReadProp
from HelperMethods.drivermanager import DriverManager
from Pages.dashboard.dashboard_page import DashboardPage
from Pages.dashboard.dashboard_page_locators import DashBoardPageLocators
from Pages.login.login_page import LoginPage
from Pages.login.login_page_locators import LoginPageLocators

""" Initialize driver, browser and redirect to URL and after completing test close the driver"""


class BaseTest:

    @pytest.fixture(autouse=True)
    def init_driver(self, request, rp_logger):
        browser = request.config.getoption("--browser")
        headless = False
        self.category = request.config.getoption("-m")
        if self.category == "":
            self.category = "sanity"
        self.url = ReadProp.get_config_data("site_config.ini", self.category, "site_url")
        self.log = rp_logger
        self.log.info("URL: " + self.url)
        self.driver = DriverManager.drivermanager(browser, headless)
        self.driver.maximize_window()
        self.driver.get(self.url)
        yield self.driver
        self.driver.close()
        self.driver.quit()

    @pytest.fixture()
    def load_pages(self):
        # Initialize the LoginPage object with driver, logger, and category
        self.loginPage = LoginPage(self.driver, self.log, self.category)
        self.dashboardPage = DashboardPage(self.driver, self.log, self.category)
        # Initialize the locators as an instance
        self.loginpagelocators = LoginPageLocators()
        self.dashboardPageLocators = DashBoardPageLocators()

        # Read credentials from the config file
        self.username = ReadProp.get_config_data("site_config.ini", self.category, "username")
        self.password = ReadProp.get_config_data("site_config.ini", self.category, "password")

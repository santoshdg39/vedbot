import pytest

from HelperMethods.config_parser import ReadProp
from HelperMethods.driver_manager import DriverManager
from Pages.admin.admin_page import AdminPage
from Pages.admin.admin_page_locators import AdminPageLocators
from Pages.dashboard.dashboard_page import DashboardPage
from Pages.dashboard.dashboard_page_locators import DashBoardPageLocators
from Pages.login.login_page import LoginPage
from Pages.login.login_page_locators import LoginPageLocators
from Pages.pim.pim_page import PimPage
from Pages.pim.pim_page_locators import PimPageLocators

""" Initialize driver, browser and redirect to URL and after completing test close the driver"""

class BaseTest:

    @pytest.fixture(autouse=True)
    def init_driver(self, request, rp_logger):
        browser = request.config.getoption("--browser")
        headless = request.config.getoption("--headless").lower() == "true"

        self.category = request.config.getoption("-m")

        # Detect marker from the test
        if request.node.get_closest_marker("local"):
            self.category = "local"
        elif request.node.get_closest_marker("regression"):
            self.category = "regression"
        else:
            self.category = "sanity"  # default

        self.url = ReadProp.get_config_data("site_config.ini", self.category, "site_url")

        self.log = rp_logger
        self.log.info("URL: " + self.url)

        self.driver = DriverManager.drivermanager(browser, headless)

        # CRITICAL LINE (for screenshot hook)
        request.cls.driver = self.driver


        self.driver.get(self.url)

        yield self.driver

        self.driver.close()
        self.driver.quit()

    @pytest.fixture()
    def load_pages(self):
        # Initialize the LoginPage object with driver, logger, and category
        self.loginPage = LoginPage(self.driver, self.log, self.category)
        self.dashboardPage = DashboardPage(self.driver, self.log, self.category)
        self.pimPage = PimPage(self.driver, self.log, self.category)
        self.adminPage = AdminPage(self.driver, self.log, self.category)
        # Initialize the locators as an instance
        self.loginpagelocators = LoginPageLocators()
        self.dashboardPageLocators = DashBoardPageLocators()
        self.pimPageLocators = PimPageLocators()
        self.adminPageLocators = AdminPageLocators()

        # Read credentials from the config file
        self.username = ReadProp.get_config_data("site_config.ini", self.category, "username", decrypt=True)
        self.password = ReadProp.get_config_data("site_config.ini", self.category, "password", decrypt=True)



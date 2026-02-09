# features/environment.py

from HelperMethods.config_parser import ReadProp
from HelperMethods.driver_manager import DriverManager
from Pages.login.login_page import LoginPage
from Pages.dashboard.dashboard_page import DashboardPage
from Pages.pim.pim_page import PimPage
from Pages.admin.admin_page import AdminPage
from Pages.login.login_page_locators import LoginPageLocators
from Pages.dashboard.dashboard_page_locators import DashBoardPageLocators
from Pages.pim.pim_page_locators import PimPageLocators
from Pages.admin.admin_page_locators import AdminPageLocators

from HelperMethods.logger_helper import get_logger  # or define above


def before_scenario(context, scenario):
    """Initialize logger, driver, page objects, locators, credentials"""

    # Logger first
    context.log = get_logger()  # ✅ safe, no BaseTest needed
    context.log.info(f"STARTING SCENARIO: {scenario.name}")

    # Config / CLI = Command Line Interface
    # behave -D browser=chrome -D env=local -D headless=false
    browser = context.config.userdata.get("browser", "chrome")
    headless = str(context.config.userdata.get("headless", "false")).lower() == "true"
    context.category = context.config.userdata.get("env", "local")

    # URL
    context.url = ReadProp.get_config_data("site_config.ini", context.category, "site_url")

    # Driver Initialization
    context.driver = DriverManager.drivermanager(browser, headless)
    context.driver.get(context.url)

    # Page Objects
    context.loginPage = LoginPage(context.driver, context.log, context.category)
    context.dashboardPage = DashboardPage(context.driver, context.log, context.category)
    context.pimPage = PimPage(context.driver, context.log, context.category)
    context.adminPage = AdminPage(context.driver, context.log, context.category)

    # Locators
    context.loginpagelocators = LoginPageLocators()
    context.dashboardPageLocators = DashBoardPageLocators()
    context.pimPageLocators = PimPageLocators()
    context.adminPageLocators = AdminPageLocators()

    # Credentials
    context.username = ReadProp.get_config_data("site_config.ini", context.category, "username", decrypt=True)
    context.password = ReadProp.get_config_data("site_config.ini", context.category, "password", decrypt=True)


def after_scenario(context, scenario):
    """Quit driver after each scenario"""
    if hasattr(context, "driver") and context.driver:
        context.log.info(f"ENDING SCENARIO: {scenario.name}")
        context.driver.quit()
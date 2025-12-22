import time

from Config import navigate_urls
from Pages.BasePage.base_page import BasePage
from Pages.dashboard.dashboard_page import DashboardPage
from Pages.login.login_page import LoginPage


class PimPage(BasePage):
    def __init__(self, driver, logger, category):
        super().__init__(driver)
        self.log = logger
        self.category = category
        self.driver = driver
        self.loginPage = LoginPage(self.driver, self.category, self.log)

    def navigate_pim(self):
        time.sleep(2)
        self.open_page(self.get_base_url()+navigate_urls.pim_page)
        time.sleep(1)
        assert "viewEmployeeList" in self.driver.current_url, "Not navigated to pim page"

    def add_employee(self, username, password):
        self.log.info("Login Started")

        try:
            self.send_keys(self.loginPageLocators.user_name, username)
            self.log.info(f"Entered username: {username}")

            self.send_keys(self.loginPageLocators.password, password)
            self.log.info("Entered password")

            self.click_after_wait(self.loginPageLocators.login_button)
            self.log.info("Clicked login button")

        except Exception as e:
            self.log.error("Login action failed", exc_info=True)
            raise



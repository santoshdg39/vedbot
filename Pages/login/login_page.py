from Pages.BasePage.base_page import BasePage
from Pages.dashboard.dashboard_page import DashboardPage


class LoginPage(BasePage):
    def __init__(self, driver, logger, category):
        super().__init__(driver)
        self.log = logger
        self.category = category
        self.driver = driver
        self.dashboardPage = DashboardPage(self.driver, self.category, self.log)

    def login(self, username, password):
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

    def logout_employee(self):
        self.click_after_wait(self.loginPageLocators.user_profile_dropdown)
        self.click_after_wait(self.loginPageLocators.logout_button)
        assert self.is_displayed(self.loginPageLocators.login_page), "Login page is not displayed"

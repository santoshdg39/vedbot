
from Pages.BasePage.base_page import BasePage


class DashboardPage(BasePage):
    def __init__(self, driver, logger, category):
        super().__init__(driver)
        self.driver = driver
        self.log = logger
        self.category = category

    def is_dashboard_displayed(self):
        return self.is_displayed(self.dashboardPageLocators.dashboard_page_link)




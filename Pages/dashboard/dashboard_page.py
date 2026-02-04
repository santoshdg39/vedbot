from selenium.common import NoSuchElementException

from Pages.BasePage.base_page import BasePage


class DashboardPage(BasePage):
    def __init__(self, driver, logger, category):
        super().__init__(driver)
        self.driver = driver
        self.log = logger
        self.category = category

    def is_dashboard_displayed(self):
        dashboard_page_heading = self.get_text(self.dashboardPageLocators.dashboard_page_heading)
        self.log.info(dashboard_page_heading)
        return dashboard_page_heading


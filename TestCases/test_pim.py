import allure
import pytest
from TestCases.basetest import BaseTest


class TestLogin(BaseTest):

    @pytest.mark.sanity
    def test_login_001(self, load_pages):
        self.log.info("created login page")
        self.loginPage.login(self.username, self.password)
        assert self.dashboardPage.is_dashboard_displayed(), "Login failed: Dashboard not displayed"

    @pytest.mark.sanity
    def test_login_002(self, load_pages):
        self.log.info("created login page")
        self.loginPage.login(self.username, "admin123dd")
        assert self.loginPage.is_login_error_displayed(), "Invalid credentials message is not displayed"



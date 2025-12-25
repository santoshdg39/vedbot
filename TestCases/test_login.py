import allure
import pytest
from TestCases.basetest import BaseTest


class TestLogin(BaseTest):

    # Verify that admin can log in using valid credentials.
    @pytest.mark.sanity
    def test_001_login(self, load_pages):
        self.log.info("created login page")
        self.loginPage.login(self.username, self.password)
        assert self.dashboardPage.is_dashboard_displayed(), "Login failed: Dashboard not displayed"

    # Verify that login fails with invalid credentials and an appropriate error message is shown
    @pytest.mark.sanity
    def test_002_login(self, load_pages):
        self.log.info("created login page")
        self.loginPage.login(self.username, "admin123dd")
        assert self.loginPage.is_login_error_displayed(), "Invalid credentials message is not displayed"



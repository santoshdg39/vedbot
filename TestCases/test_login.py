import allure
import pytest

import TestData.messages
from TestCases.basetest import BaseTest


class TestLogin(BaseTest):

    # Verify that admin can log in using valid credentials.
    @pytest.mark.local
    @pytest.mark.sanity
    def test_001_login_with_valid_password(self, load_pages):
        self.log.info("TEST STARTED: login_with_valid_password")
        self.loginPage.login(self.username, self.password)
        actual_heading = self.dashboardPage.is_dashboard_displayed()
        self.log.info(f"Successfully logged in {actual_heading}")
        assert TestData.messages.dashboard_page_heading_text == actual_heading, f"{actual_heading} Login failed: " \
                                                                                f"Dashboard not displayed "

    # Verify that login fails with invalid credentials and an appropriate error message is shown
    @pytest.mark.local
    @pytest.mark.sanity
    def test_002_login_with_invalid_password(self, load_pages):
        self.log.info("TEST STARTED: login_with_invalid_password")
        self.loginPage.login(self.username, "admin123dd")
        login_error_message = self.loginPage.get_text_value(self.loginpagelocators.ERROR_MESSAGE)
        assert TestData.messages.invalid_password_error_message_text in login_error_message, "Invalid credentials " \
                                                                                             "message is not displayed "



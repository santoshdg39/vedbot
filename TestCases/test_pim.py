import time

import allure
import pytest
from TestCases.basetest import BaseTest


class TestPim(BaseTest):

    # Verify adding an employee without login details and ensure the employee appears in the employee list.
    @pytest.mark.sanity
    def test_001_add_employee_without_login(self, load_pages):
        self.loginPage.login(self.username, self.password)
        employee_id, full_name, _, _ = self.pimPage.add_employee(include_login_details=False)
        # _, _ Use _ to ignore unused returns
        assert self.pimPage.is_displayed(self.pimPageLocators.employee_name_listPage), "Employee not added"
        self.pimPage.search_employee(employee_id, full_name)
        self.pimPage.delete_employee(employee_id, full_name)

    # Verify that an employee can be added with login details, has an enabled status, and can successfully log in.
    @pytest.mark.sanity
    def test_002_add_employee_with_login(self, load_pages):
        self.loginPage.login(self.username, self.password)
        employee_id, full_name, username, password = self.pimPage.add_employee(include_login_details=True, status="enabled")
        assert self.pimPage.is_displayed(self.pimPageLocators.employee_name_listPage), "Employee not added"
        self.loginPage.logout_employee()
        self.loginPage.login(username, password)
        actual_employee_display_name = self.loginPage.get_text_value(self.loginpagelocators.user_dropdown_name)
        full_name_list = full_name.split()
        expected_employee_display_name = " ".join([full_name_list[0], full_name_list[-1]])
        assert actual_employee_display_name == expected_employee_display_name, "Incorrect employee logged in"


import time

import allure
import pytest

import TestData.messages
from TestCases.basetest import BaseTest


class TestPim(BaseTest):

    # Verify adding an employee without login details and ensure the employee appears in the employee list.
    @pytest.mark.sanity
    def test_001_add_employee_without_login_details(self, load_pages):
        self.log.info("TEST STARTED: add_employee_without_login_details")
        self.loginPage.login(self.username, self.password)
        self.log.info("Logged in as Admin")
        employee_id, full_name, _, _ = self.pimPage.add_employee(include_login_details=False)
        # _, _ Use _ to ignore unused returns
        self.log.info(f"Employee is added: employee_id: {employee_id} full_name: {full_name}")
        personal_details_text = self.pimPage.get_text_value(self.pimPageLocators.personal_details_text_on_listPage)
        self.log.info(f"Employee is added successfully {personal_details_text}")
        assert TestData.messages.personal_details_text_on_listPage in personal_details_text, "Employee not added"
        self.pimPage.search_employee(employee_id, full_name)
        self.pimPage.delete_employee(employee_id, full_name)

    # Verify that an employee can be added with login details, has an enabled status, and can successfully log in.
    @pytest.mark.sanity
    def test_002_add_employee_with_login_details(self, load_pages):
        self.log.info("TEST STARTED: add_employee_with_login_details")
        self.loginPage.login(self.username, self.password)
        self.log.info("Logged in as Admin")
        employee_id, full_name, username, password = self.pimPage.add_employee(include_login_details=True, status="enabled")
        self.log.info(f"Employee is added: employee_id: {employee_id} full_name: {full_name}, username: {username},"
                      f"password: {password} ")
        personal_details_text = self.pimPage.get_text_value(self.pimPageLocators.personal_details_text_on_listPage)
        self.log.info(f"Employee is added successfully {personal_details_text}")
        assert TestData.messages.personal_details_text_on_listPage in personal_details_text, "Employee not added"
        self.log.info("Logged out Admin user")
        self.loginPage.logout_employee()
        self.loginPage.login(username, password)
        self.log.info(f"Enabled status employee logged in")
        actual_employee_display_name = self.loginPage.get_text_value(self.loginpagelocators.user_dropdown_name)
        full_name_list = full_name.split()
        expected_employee_display_name = " ".join([full_name_list[0], full_name_list[-1]])
        assert actual_employee_display_name == expected_employee_display_name, "Incorrect employee logged in"

    # Verify that a disabled employee with login details cannot log in.
    @pytest.mark.sanity
    def test_003_add_employee_with_login_details_status_disabled(self, load_pages):
        self.log.info("TEST STARTED: add_employee_with_login_details_status_disabled")
        self.loginPage.login(self.username, self.password)
        self.log.info("Logged in as Admin")
        employee_id, full_name, username, password = self.pimPage.add_employee(include_login_details=True,
                                                                               status="disabled")
        self.log.info(f"Employee is added: employee_id: {employee_id} full_name: {full_name}, username: {username},"
                      f"password: {password} ")
        personal_details_text = self.pimPage.get_text_value(self.pimPageLocators.personal_details_text_on_listPage)
        self.log.info(f"Employee is added successfully {personal_details_text}")
        assert TestData.messages.personal_details_text_on_listPage in personal_details_text, "Employee not added"
        self.log.info("Logged out Admin user")
        self.loginPage.logout_employee()
        self.loginPage.login(username, password)
        account_disabled_msg = self.pimPage.get_text_value(self.loginpagelocators.account_disabled_msg)
        self.log.info(f"Disabled status employee is trying to login {personal_details_text}")
        assert TestData.messages.account_disabled_msg_text in account_disabled_msg, "account is active"

    # Verify employee data import successfully using an CSV file
    @pytest.mark.regression
    def test_004_import_employee(self, load_pages, prepare_employee_csv_data):
        self.log.info("TEST STARTED: Import employee using csv file")
        self.loginPage.login(self.username, self.password)
        self.log.info("Logged in as Admin")
        file_path = prepare_employee_csv_data
        self.log.info(f"CSV file ready at path: {file_path}")
        self.pimPage.import_data(file_path)
        self.log.info("CSV import action triggered")
        import_details_text = self.pimPage.get_text_value(self.pimPageLocators.import_details)
        self.log.info(f"Import success message displayed: {import_details_text}")
        assert TestData.messages.import_detail_text in import_details_text, "Import failed"


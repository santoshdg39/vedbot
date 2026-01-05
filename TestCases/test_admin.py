import time

import allure
import pytest

import TestData.messages
from HelperMethods.db_helper import DatabaseHelper
from HelperMethods.test_data_generator_helper import DataGenerator
from TestCases.basetest import BaseTest


class TestAdmin(BaseTest):

    # 001 Verify employee creation via CSV import and read csv to update the employee’s role to Admin through the UI,
    # then validate details in the system Users table.
    @pytest.mark.local
    def test_employee_creation_using_csv_and_role_update_to_admin_from_ui(self, load_pages, prepare_employee_csv_data):
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
        employee_id, full_name = self.pimPage.get_employees_from_csv()
        self.log.info(f"Employee data read from csv: {employee_id} {full_name}")
        e_username, e_password = DataGenerator.generate_user_credentials()
        full_name_list = full_name.split()
        expected_employee_display_name = " ".join([full_name_list[0], full_name_list[-1]])
        exp_role = "Admin"
        exp_status = "Enabled"
        expected_role, expected_status = self.adminPage.map_role_and_status(exp_role, exp_status)
        user_data = self.adminPage.add_roll_of_employee(e_username, e_password, full_name, expected_role, expected_status)
        self.log.info(f"Employee data after role update: {user_data}")
        assert user_data[
                   "employee_name"] == expected_employee_display_name, f"{expected_employee_display_name} employee " \
                                                                       f"not found."
        assert user_data["user_role"] == exp_role, f"{exp_role} roll is not updated."
        self.pimPage.delete_employee(employee_id, full_name)

    # 002 Verify updating an employee’s role from No Role → Admin → ESS and status from Enabled → Disabled through the
    # UI, and validate the changes in the database.
    @pytest.mark.local
    def test_role_and_status_update_from_ui_and_validate_from_database(self, load_pages, prepare_employee_csv_data):
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
        employee_id, full_name = self.pimPage.get_employees_from_csv()
        e_username, e_password = DataGenerator.generate_user_credentials()
        exp_role = "Admin"
        exp_status = "Enabled"
        expected_role, expected_status = self.adminPage.map_role_and_status(exp_role, exp_status)
        self.log.info(f"Updating roll to {exp_role} and status to {exp_status}")
        user_data = self.adminPage.add_roll_of_employee(e_username, e_password, full_name, expected_role, expected_status)
        username = user_data["username"]
        user_data_db = DatabaseHelper.get_user_status_and_role_by_username(username)
        self.log.info(f"{username} the user_data_db is {user_data_db}")
        assert user_data_db["username"] == username, f"Expected {username} not found in db"
        assert user_data_db["status"] == exp_status, f"Expected {exp_status} not found in db"
        assert user_data_db["role"] == exp_role, f"Expected {exp_role} not found in db"
        self.loginPage.logout_employee()
        time.sleep(2)
        self.loginPage.login(self.username, self.password)
        self.log.info("Logged in as Admin")
        exp_role = "ESS"
        exp_status = "Disabled"
        expected_role, expected_status = self.adminPage.map_role_and_status(exp_role, exp_status)
        self.log.info(f"Updating roll to {exp_role} and status to {exp_status}")
        user_data = self.adminPage.edit_roll_of_employee(e_username, full_name, expected_role, expected_status)
        username = user_data["username"]
        user_data_db = DatabaseHelper.get_user_status_and_role_by_username(e_username)
        self.log.info(f"{username} the user_data_db is {user_data_db}")
        assert user_data_db["username"] == username, f"Expected {username} not found in db"
        assert user_data_db["status"] == exp_status, f"Expected {exp_status} not found in db"
        assert user_data_db["role"] == exp_role, f"Expected {exp_role} not found in db"
        self.pimPage.delete_employee(employee_id, full_name)

from datetime import datetime
import random
import string
import time

from selenium.common import TimeoutException
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By

from Config import navigate_urls
from HelperMethods import test_data_generator_helper
from HelperMethods.test_data_generator_helper import DataGenerator
from Pages.BasePage.base_page import BasePage
from Pages.dashboard.dashboard_page import DashboardPage
from Pages.login.login_page import LoginPage
from TestData import messages


class AdminPage(BasePage):
    def __init__(self, driver, logger, category):
        super().__init__(driver)
        self.log = logger
        self.category = category
        self.driver = driver
        self.loginPage = LoginPage(self.driver, self.category, self.log)

    def navigate_admin(self):
        time.sleep(2)
        self.open_page(self.get_base_url() + navigate_urls.admin_page)
        time.sleep(1)
        assert "viewSystemUsers" in self.driver.current_url, "Not navigated to admin page"

    def add_roll_of_employee(self, e_username, e_password, full_name, expected_role, expected_status):
        self.navigate_admin()
        self.click_after_wait(self.adminPageLocators.add_admin)
        self.select_dropdown_by_keyboard(self.adminPageLocators.user_role_dropdown, expected_role)
        self.type_and_select(self.adminPageLocators.employee_name, full_name)
        self.select_dropdown_by_keyboard(self.adminPageLocators.status, expected_status)
        self.send_keys_after_wait(self.adminPageLocators.username, e_username)
        self.send_keys_after_wait(self.adminPageLocators.password, e_password)
        self.send_keys_after_wait(self.adminPageLocators.conf_password, e_password)
        self.click_after_wait(self.adminPageLocators.save_button)
        time.sleep(5)
        self.wait_for_element_and_refresh(self.adminPageLocators.system_users)
        time.sleep(5)
        self.search_system_users(e_username, full_name)
        user_data = self.get_user_details(e_username)
        assert user_data["username"] == e_username, f"{e_username} not found"
        return user_data

    def edit_roll_of_employee(self, e_username, full_name, expected_role, expected_status):
        self.navigate_admin()
        self.search_system_users(e_username, full_name)
        self.open_edit_employee_section(e_username)
        self.select_dropdown_by_keyboard(self.adminPageLocators.user_role_dropdown, expected_role)
        self.select_dropdown_by_keyboard(self.adminPageLocators.status, expected_status)
        self.click_after_wait(self.adminPageLocators.save_button)
        self.wait_for_element_and_refresh(self.adminPageLocators.system_users)
        self.search_system_users(e_username, full_name)
        user_data = self.get_user_details(e_username)
        assert user_data["username"] == e_username, f"{e_username} not found"
        return user_data

    def search_system_users(self, e_username, full_name):
        self.send_keys_after_wait(self.adminPageLocators.username, e_username)
        self.type_and_select(self.adminPageLocators.employee_name, full_name)
        self.click_after_wait(self.adminPageLocators.search_button)


    def get_user_details(self, e_username):
        row_xpath = self.adminPageLocators.user_name_in_user_management_table.format(e_username)
        try:
            # 1. Get the row
            row = self.wait_for_visibility_by_xpath(row_xpath)

            cells = self.find_child_elements_by_xpath(row, self.adminPageLocators.user_management_table_cells)

            user_data = {
                "username": cells[1].text.strip(),
                "user_role": cells[2].text.strip(),
                "employee_name": cells[3].text.strip(),
                "status": cells[4].text.strip()
            }

            self.log.info(user_data)
            return user_data

        except TimeoutException:
            assert False, f"User not found in table: {e_username}"

    def map_role_and_status(self, expected_role, expected_status):
        role = 1 if expected_role == "Admin" else 2
        status = 1 if expected_status == "Enabled" else 2
        return role, status

    def open_edit_employee_section(self, e_username):
        """
        Opens Edit User page for the given username from System Users table
        """
        row_xpath = self.adminPageLocators.edit_admin_button.format(e_username)

        try:
            edit_button = self.wait_for_visibility_by_xpath(row_xpath)
            edit_button.click()
            self.log.info(f"Clicked Edit button for user: {e_username}")
        except TimeoutException:
            assert False, f"Edit button not found for username: {e_username}"

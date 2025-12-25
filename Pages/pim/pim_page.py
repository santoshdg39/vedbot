from datetime import datetime
import random
import string
import time

from Config import navigate_urls
from HelperMethods.test_data_generator_helper import DataGenerator
from Pages.BasePage.base_page import BasePage
from Pages.dashboard.dashboard_page import DashboardPage
from Pages.login.login_page import LoginPage


class PimPage(BasePage):
    def __init__(self, driver, logger, category):
        super().__init__(driver)
        self.log = logger
        self.category = category
        self.driver = driver
        self.loginPage = LoginPage(self.driver, self.category, self.log)

    def navigate_pim(self):
        time.sleep(2)
        self.open_page(self.get_base_url() + navigate_urls.pim_page)
        time.sleep(1)
        assert "viewEmployeeList" in self.driver.current_url, "Not navigated to pim page"

    def add_login_details(self):
        username = "emp_" + ''.join(
            random.choices(string.ascii_lowercase + string.digits, k=6)
        )
        # password = "Test@" + ''.join(
        #     random.choices(string.ascii_letters + string.digits, k=6)
        # )
        password = "Santosh24#"
        time.sleep(10)
        self.send_keys_after_wait(self.pimPageLocators.userName, username)
        self.send_keys_after_wait(self.pimPageLocators.passWord, password)
        self.send_keys(self.pimPageLocators.confirmPassword, password)
        return username, password

    def add_employee(self, include_login_details=False, status="enabled"):
        self.navigate_pim()
        self.click_after_wait(self.pimPageLocators.add_employee)
        unique_text = DataGenerator.generate_unique_text()
        firstname = "f_" + unique_text
        middleman = "m_" + unique_text
        lastname = "l_" + unique_text
        self.send_keys(self.pimPageLocators.firstName, firstname)
        self.send_keys(self.pimPageLocators.middleName, middleman)
        self.send_keys(self.pimPageLocators.lastName, lastname)
        full_name = " ".join([firstname, middleman, lastname])
        # employee_Id = "E" + datetime.now().strftime("%d%H%M%S")
        # self.clear_send_keys_using_backspace(self.pimPageLocators.employee_id)
        # self.send_keys_after_wait(self.pimPageLocators.employee_id, employee_Id)
        employee_Id = self.get_text_value(self.pimPageLocators.employee_id)
        username = password = None
        if include_login_details:
            # Ensure checkbox is visible and clickable
            self.click_after_wait(self.pimPageLocators.createLoginDetailCheckbox)
            username, password = self.add_login_details()

            if status == "disabled":
                self.click_after_wait(self.pimPageLocators.status_disabled)

        # Save employee
        self.click_after_wait(self.pimPageLocators.saveButton)
        return employee_Id, full_name, username, password

    def search_employee(self, employee_id, full_name):
        self.navigate_pim()
        self.click_after_wait(self.pimPageLocators.employee_list)
        self.send_keys_after_wait(self.pimPageLocators.employee_full_name, full_name)
        self.send_keys_after_wait(self.pimPageLocators.employee_id_listPage, employee_id)
        self.click_after_wait(self.pimPageLocators.search_button)
        result_employee_id = self.get_text_value(self.pimPageLocators.employee_id_listPage)
        assert result_employee_id == employee_id, "Employee not found"

    def delete_employee(self, employee_id, full_name):
        self.search_employee(employee_id, full_name)
        self.click_after_wait(self.pimPageLocators.select_employee_zero)
        self.click_after_wait(self.pimPageLocators.delete_employee_button)
        self.click_after_wait(self.pimPageLocators.yes_deleted_button)
        self.wait_for_element_and_refresh(self.pimPageLocators.employee_list)
        self.search_employee(employee_id, full_name)
        assert self.is_displayed(self.pimPageLocators.no_records_found), "Employee not deleted"

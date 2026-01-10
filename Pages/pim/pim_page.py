from datetime import datetime
import random
import string
import time

from Config import navigate_urls, global_var
from HelperMethods.csv_helper import CSVHelper
from HelperMethods.test_data_generator_helper import DataGenerator
from Pages.BasePage.base_page import BasePage
from Pages.dashboard.dashboard_page import DashboardPage
from Pages.login.login_page import LoginPage
from TestData import messages


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
        password = "Santosh24011992#"
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
        self.wait_for_element_and_refresh(self.pimPageLocators.employee_information)
        self.search_employee(employee_id, full_name)
        assert self.is_displayed(self.pimPageLocators.no_records_found), "Employee not deleted"

    def import_data(self, file_path):
        self.navigate_pim()
        self.click_after_wait(self.pimPageLocators.configuration)
        self.click_after_wait(self.pimPageLocators.data_import)
        text_before_file_upload = self.get_text_value(self.pimPageLocators.no_file_selected).strip()
        assert messages.no_file_selected_text in text_before_file_upload, \
            f"Expected '{messages.no_file_selected_text}' but got {text_before_file_upload}"
        self.log.info(f"[INFO] Uploading employee file from path: {file_path}")
        self.upload_file(file_path)
        uploaded_file_name = self.get_text_value(self.pimPageLocators.file_uploaded).strip()
        assert messages.file_uploaded_text in uploaded_file_name, \
            f"File upload failed. Text shown: {uploaded_file_name}"
        self.click_after_wait(self.pimPageLocators.upload_csv_button)

    def upload_file(self, file_path):
        self.log.info(f"[UPLOAD] {file_path}")
        file_input = self.find_element(self.pimPageLocators.file_input)
        file_input.send_keys(file_path)

    def get_employees_from_csv(self):
        """
        Reads employees from the CSV file and returns a list of dicts
        containing first_name, last_name, and employee_id
        """
        rows = CSVHelper.read_rows(global_var.IMPORT_EMPLOYEE_CSV_PATH)
        if not rows:
            self.log.warning("CSV file is empty")
            return None, None, None, None

        first_row = rows[0]  # Take the first employee
        first_name = first_row.get("first_name", "")
        middle_name = first_row.get("middle_name", "")
        last_name = first_row.get("last_name", "")
        employee_id = first_row.get("employee_id", "")

        full_name = " ".join(name for name in [first_name, middle_name, last_name] if name)

        self.log.info(f"Employee: {full_name} ({employee_id})")
        return employee_id, full_name


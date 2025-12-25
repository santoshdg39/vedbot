import time
from datetime import datetime

import allure
from selenium.common import NoSuchElementException, TimeoutException, ElementNotInteractableException
from selenium.webdriver import Keys, ActionChains
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from Pages.dashboard.dashboard_page_locators import DashBoardPageLocators
from Pages.login.login_page_locators import LoginPageLocators
from Pages.pim.pim_page_locators import PimPageLocators


class BasePage:

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(self.driver, 120)
        self.loginPageLocators = LoginPageLocators
        self.dashboardPageLocators = DashBoardPageLocators
        self.pimPageLocators = PimPageLocators

    def open_page(self, url):
        self.driver.get(url)

    def find_element(self, locator):
        try:
            return self.wait.until(EC.presence_of_element_located(locator))
        except NoSuchElementException:
            assert False, f"Element not found: {locator}"
        except TimeoutException:
            assert False, f"Timeout waiting for element to be visible: {locator}"

    def find_elements(self, locator):
        try:
            return self.wait.until(EC.presence_of_element_located(locator))
        except NoSuchElementException:
            assert False, f"Element not found: {locator}"
        except TimeoutException:
            assert False, f"Timeout waiting for element to be visible: {locator}"

    def find_multiple_elements(self, locator):
        try:
            time.sleep(2)
            return self.wait.until(EC.presence_of_all_elements_located(locator))
        except NoSuchElementException:
            assert False, f"Element not found: {locator}"

    def is_displayed(self, locator):
        try:
            return self.find_element(locator).is_displayed()
        except NoSuchElementException:
            assert False, f"Element not found: {locator}"

    def is_selected(self, locator):
        try:
            return self.find_element(locator).is_selected()
        except NoSuchElementException:
            assert False, f"Element not found: {locator}"

    def get_count_elements(self, locator):
        try:
            return len(self.find_multiple_elements(locator))
        except NoSuchElementException:
            assert False, f"Element not found: {locator}"

    def highlight_element(self, locator):
        element = self.find_element(locator)
        self.driver.execute_script("arguments[0].setAttribute('style',arguments[1]);", element,
                                   "background: yellow; border: 2px solid red;")
        try:
            time.sleep(0.5)
            self.driver.execute_script("arguments[0].setAttribute('style', arguments[1]);", element, "")
        except Exception as e:
            print(str(e))

    def click(self, by_locator: object) -> object:
        try:
            self.wait.until(EC.presence_of_element_located(by_locator))
            self.wait.until(EC.visibility_of_element_located(by_locator))
            self.wait.until(EC.element_to_be_clickable(by_locator))
            self.highlight_element(by_locator)
        except TimeoutException:
            assert False, f"Request times out. '{by_locator}' not found"

    @staticmethod
    def get_date():
        today_date = datetime.now()
        return today_date.strftime("%d%b%y%H%M")

    def click_after_wait(self, by_locator, timeout=15):
        self.wait_for_loader_to_disappear(timeout=timeout)
        try:
            self.wait.until(EC.visibility_of_element_located(by_locator))
            element = self.wait.until(EC.element_to_be_clickable(by_locator))
            element.click()
        except TimeoutException:
            assert False, f"Element not clickable: {by_locator}"

    def send_keys(self, locator, text):
        try:
            self.highlight_element(locator)
            self.find_element(locator).send_keys(text)
        except NoSuchElementException:
            assert False, f"Element not found: {locator}"

    def send_keys_after_wait(self, locator, text):
        try:
            self.wait.until(EC.visibility_of_element_located(locator))
            element = self.wait.until(EC.element_to_be_clickable(locator))
            element.send_keys(text)
        except TimeoutException:
            assert False, f"Element not intractable: {locator}"

    def send_key_and_enter(self, locator, text):
        try:
            self.wait.until(EC.visibility_of_element_located(locator))
            element = self.wait.until(EC.element_to_be_clickable(locator))
            element.send_keys(text)
            element.send_keys(Keys.ENTER)
        except TimeoutException:
            assert False, f"Element not intractable: {locator}"

    def clear_and_send_keys(self, locator, text):
        try:
            element = self.wait.until(EC.element_to_be_clickable(locator))
            self.highlight_element(locator)
            element.clear()
            time.sleep(1)
            element.clear()
            element.send_keys(text)
        except (TimeoutException, ElementNotInteractableException):
            assert False, f"Element not intractable: {locator}"

    def clear_send_keys_using_backspace(self, locator):
        try:
            element = self.wait.until(EC.element_to_be_clickable(locator))
            element_text = element.get_attribute("value")
            time.sleep(1)
            element.send_keys(Keys.BACKSPACE * len(element_text))
            element.send_keys(Keys.ENTER)
        except (TimeoutException, ElementNotInteractableException):
            assert False, f"Element not intractable: {locator}"

    def hit_enter(self, locator):
        self.find_element(*locator).send_keys(Keys.ENTER)

    def wait_for_element_clickable(self, locator):
        try:
            element = self.wait.until(EC.element_to_be_clickable(locator))
            return element
        except TimeoutException:
            assert False, f"Element not clickable: {locator}"

    def wait_for_element_visible(self, locator):
        try:
            element = self.wait.until(EC.presence_of_element_located(locator))
            return element
        except TimeoutException:
            assert False, f"Element not visible: {locator}"

    def wait_for_element_invisible(self, locator):
        try:
            self.wait.until(EC.invisibility_of_element(locator))
            return True
        except TimeoutException:
            assert False, f"Element still visible: {locator}"

    def wait_for_element_and_refresh(self, locator, timeout=10, max_retries=5):
        retries = 0
        while retries < max_retries:
            try:
                element = WebDriverWait(self.driver, timeout).until(EC.visibility_of_element_located(locator))
                return element
            except TimeoutException:
                self.driver.refresh()
                retries += 1

    def get_text_value(self, locator):
        try:
            element = self.wait_for_element_visible(locator)
            if element.tag_name.lower() in ["input", "textarea"]:
                return element.get_attribute("value")
            else:
                return element.text
        except TimeoutException:
            assert False, f"Unable to get text value from: {locator}"

    def get_title(self):
        try:
            return self.driver.title
        except Exception as e:
            assert False, f"Unable to get page title. Error: {e}"

    def scroll_to_element(self, locator):
        try:
            element = self.find_element(locator)
            self.driver.execute_script("arguments[0].scrollIntoView(true);", element)
        except NoSuchElementException:
            assert False, f"Element not found: {locator}"

    def scroll_to_element_and_click(self, locator):
        try:
            element = self.driver.find_element(*locator)
            self.driver.execute_script("arguments[0].scrollIntoView()", element)
            element.click()
        except NoSuchElementException:
            assert False, f"Element not found: {locator}"

    def page_scroll(self):
        SCROLL_PAUSE_TIME = 2
        # get scroll height
        page_height = self.driver.execute_script("return document.body.scrollHeight")
        while True:
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(SCROLL_PAUSE_TIME)
            new_height = self.driver.execute_script("return document.body.scrollHeight")
            if new_height == page_height:
                break
            page_height = new_height

    def action_move_to_element_click(self, locator):
        try:
            action = ActionChains(self.driver)
            element = self.find_element(locator)
            action.move_to_element(element).click().perform()
        except NoSuchElementException:
            assert False, f"Element not found: {locator}"

    def action_move_to_element(self, locator):
        try:
            action = ActionChains(self.driver)
            element = self.find_element(locator)
            action.move_to_element(element).perform()
        except NoSuchElementException:
            assert False, f"Element not found: {locator}"

    def action_drag_drop_element(self, locator):
        try:
            action = ActionChains(self.driver)
            element = self.find_element(locator)
            action.drag_and_drop(element).perform()
        except NoSuchElementException:
            assert False, f"Element not found: {locator}"

    def is_element_present(self, locator):
        try:
            self.driver.find_element(*locator)
        except NoSuchElementException:
            return False
        return True

    def select_dropdown_list(self, locator, select_by, data):
        dropdown = Select(self.driver.find_element(locator))
        if select_by == "index":
            dropdown.select_by_index(int(data))
        elif select_by == "value":
            dropdown.select_by_value(str(data))
        elif select_by == "text":
            dropdown.select_by_visible_text(str(data))
        else:
            raise Exception("Invalid select_by type. Use: index / value / text")
        return dropdown

    def get_select_selected_value(self, locator, text_type="value"):
        try:
            dropdown = Select(self.driver.find_element(*locator))
            if text_type == "value":
                selected_value = dropdown.first_selected_option.get_attribute("value")
            else:
                selected_value = dropdown.first_selected_option.text
            return selected_value
        except NoSuchElementException:
            assert False, f"Dropdown not found: {locator}"

    def get_select_selected_text(self, locator):
        try:
            dropdown = Select(self.driver.find_element(*locator))
            selected_value_text = dropdown.first_selected_option.text
            return selected_value_text
        except NoSuchElementException:
            assert False, f"Element not found {locator}"

    def search_select_by_visible_text(self, locator, search_string):
        try:
            dropdown = Select(self.driver.find_element(*locator))
            desired_option = search_string
            option_available = False
            for option in dropdown.options:
                if option == desired_option:
                    option_available = True
                    break
            if option_available:
                dropdown.select_by_visible_text(desired_option)
        except NoSuchElementException:
            assert False, f"Option not found: {locator}"

    def get_multi_selected_values(self, locator, text_type):
        try:
            dropdown = Select(self.driver.find_element(*locator))
            if text_type == "text":
                return [option.text for option in dropdown.all_selected_options]
            else:
                return [option.get_attribute("value") for option in dropdown.all_selected_options]
        except NoSuchElementException:
            assert False, f"Dropdown not found: {locator}"

    def move_to_iframe(self, locator):
        try:
            self.wait.until(EC.frame_to_be_available_and_switch_to_it(locator))
        except TimeoutException:
            assert False, f"The element not found: {locator}"

    def count_of_elements(self, locator):
        try:
            elements = self.driver.find_elements(*locator)
            return len(elements)
        except NoSuchElementException:
            assert False, f"Elements not found: {locator}"

    def get_current_url(self):
        return self.driver.current_url

    def get_base_url(self):
        current_url_1 = (self.get_current_url()).split('/')[0:4]
        current_url_2 = '/'.join(current_url_1)
        return current_url_2

    def attach_screenshot_to_allure_report(self):
        allure.attach(self.driver.get_screenshot_as_png(),
                      name="Screenshot on pytest check fails",
                      attachment_type=allure.attachment_type.PNG)

    def wait_for_loader_to_disappear(self, timeout=15):
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.invisibility_of_element_located(
                    ("css selector", ".oxd-form-loader")
                )
            )
        except TimeoutException:
            # Sometimes loader flashes very fast – ignore safely
            pass

import time
from datetime import datetime

import allure
from selenium.common import NoSuchElementException, TimeoutException, ElementNotInteractableException, \
    StaleElementReferenceException, UnexpectedTagNameException
from selenium.webdriver import Keys, ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from Pages.admin.admin_page_locators import AdminPageLocators
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
        self.adminPageLocators = AdminPageLocators

    def open_page(self, url):
        self.driver.get(url)

    def find_element(self, locator):
        try:
            return self.wait.until(EC.visibility_of_element_located(locator))
        except TimeoutException as e:
            raise  TimeoutException (f"Timeout waiting for element to be visible: {locator}") from e

    def find_elements(self, locator):
        try:
            return self.wait.until(EC.visibility_of_all_elements_located(locator))
        except TimeoutException as e:
            raise TimeoutException(f"Timeout waiting for elements to be visible: {locator}") from e

    # Counting elements (visibility not required) Example: Number of records, Number of notifications, Pagination count
    def find_multiple_elements(self, locator):
        try:
            return self.wait.until(EC.presence_of_all_elements_located(locator))
        except TimeoutException as e:
            raise TimeoutException (f"Element not present in DOM: {locator}") from e

    # Waits until the element is visible and returns the WebElement.
    # Raises TimeoutException if the element is not visible within the wait time.
    # is_displayed() then returns True or False based on the element's visibility.

    def is_displayed(self, locator):
        return self.find_element(locator).is_displayed()

    def is_selected(self, locator):
        return self.find_element(locator).is_selected()

    def is_enabled(self, locator):
        return self.find_element(locator).is_enabled()

    def get_text(self, locator):
        return self.find_element(locator).text.strip()

    def get_count_elements(self, locator):
        return len(self.find_multiple_elements(locator))

    def js_click(self, locator):
        element = self.find_element(locator)
        self.driver.execute_script("arguments[0].click();", element)

    def scroll_to_element(self, locator):
        element = self.find_element(locator)
        self.driver.execute_script("arguments[0].scrollIntoView({block:'center'});", element)

    def scroll_to_element_and_click(self, locator):
        self.scroll_to_element(locator)
        self.click(locator)

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

    # Use when: send_keys() doesn’t work, React/Angular input issues
    def js_send_keys(self, locator, text):
        element = self.find_element(locator)
        self.driver.execute_script("arguments[0].value=arguments[1];", element, text)

    # Use when: .text returns empty, Hidden or dynamic text
    def js_get_text(self, locator):
        element = self.find_element(locator)
        return self.driver.execute_script("return arguments[0].innerText;", element)

    def highlight_element(self, locator, duration=0.5):
        element = self.find_element(locator)
        original_style = element.get_attribute("style")
        self.driver.execute_script("arguments[0].setAttribute('style',arguments[1]);", element,
                                   "background: yellow; border: 2px solid red;")
        time.sleep(duration)
        self.driver.execute_script("arguments[0].setAttribute('style', arguments[1]);", element, original_style)

    # Using all three ensures the element exists, is visible, and is interactable before performing actions.
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

    # Identify the loader element on the page (here using CSS selector after manual inspection).
    # If the loader disappears immediately, a TimeoutException may occur, which is safely ignored.
    def wait_for_loader_to_disappear(self, timeout=15):
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.invisibility_of_element_located(
                    (By.CSS_SELECTOR, ".oxd-overlay.oxd-overlay--flex-centered")
                )
            )
        except TimeoutException:
            # Sometimes loader flashes very fast – ignore safely
            pass

    def click_after_wait(self, by_locator, timeout=15):
        self.wait_for_loader_to_disappear(timeout=timeout)
        try:
            element = self.wait.until(EC.element_to_be_clickable(by_locator))
            element.click()
        except TimeoutException:
            assert False, f"Element not clickable: {by_locator}"

    def send_keys(self, locator, text):
        try:
            self.highlight_element(locator)
            self.find_element(locator).send_keys(text)
        except TimeoutException:
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
        try:
            self.find_element(locator).send_keys(Keys.ENTER)
        except (TimeoutException, StaleElementReferenceException, ElementNotInteractableException):
            assert False, f"Unable to hit ENTER on element: {locator}"

    # waits until the element is present, visible, and enabled,
    # then returns it as a WebElement so it can be clicked safely.
    # Use when you want to click a button, link, or checkbox.
    def wait_for_element_clickable(self, locator):
        try:
            element = self.wait.until(EC.element_to_be_clickable(locator))
            return element
        except TimeoutException:
            assert False, f"Element not clickable: {locator}"

    # Waits until an element exists in the DOM, visibility not required. Returns: WebElement
    def wait_for_element_visible(self, locator):
        try:
            element = self.wait.until(EC.presence_of_element_located(locator))
            return element
        except TimeoutException:
            assert False, f"Element not visible: {locator}"

    # Wait for loading spinners to disappear before continuing.
    # Example: Page loader or spinner while fetching search results. It returns True/Timeout.
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
        raise TimeoutException(
            f"Element not visible after {max_retries} refresh attempts: {locator}"
        )

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

    def action_move_to_element_click(self, locator):
        try:
            action = ActionChains(self.driver)
            element = self.find_element(locator)
            action.move_to_element(element).click().perform()
        except (TimeoutException, StaleElementReferenceException, ElementNotInteractableException):
            assert False, f"Unable to move to and click element: {locator}"


    """
    Finds the element (with explicit wait)
    Moves the mouse cursor to that element
    Does NOT click
    Leaves the cursor hovering over the element
    """
    def action_move_to_element(self, locator):
        try:
            action = ActionChains(self.driver)
            element = self.find_element(locator)
            action.move_to_element(element).perform()
        except (TimeoutException, StaleElementReferenceException, ElementNotInteractableException):
            assert False, f"Unable to move to and click element: {locator}"

    def action_drag_drop_element(self, source_locator, target_locator):
        try:
            action = ActionChains(self.driver)
            source = self.find_element(source_locator)
            target = self.find_element(target_locator)
            action.drag_and_drop(source, target).perform()
        except (TimeoutException, StaleElementReferenceException, ElementNotInteractableException):
            assert False, f"Unable to drag element {source_locator} to {target_locator}"

    """
    Checks immediately if an element exists in the DOM
    Returns: True → element is present and False → element is NOT present
    No wait, No visibility check
    """
    def is_element_present(self, locator):
        try:
            self.driver.find_element(*locator)
        except NoSuchElementException:
            return False
        return True

    # Select is a built-in Selenium class used to handle HTML <select> dropdown elements.
    # Use Select only if the HTML tag is <select>. It works with dropdowns that contain <option> tags.
    def select_dropdown_list(self, locator, select_by, data):
        try:
            element = self.find_element(locator)   # explicit wait
            dropdown = Select(element)
            if select_by == "index":
                dropdown.select_by_index(int(data))
            elif select_by == "value":
                dropdown.select_by_value(str(data))
            elif select_by == "text":
                dropdown.select_by_visible_text(str(data))
            else:
                raise ValueError("Invalid select_by type. User: index / value / text")
            return dropdown
        except (TimeoutException, StaleElementReferenceException, ElementNotInteractableException) as e:
            assert False, f"Dropdown selection failed for : {locator} : {e}"


    # This method gives the currently selected <option>
    # If it’s a single-select dropdown → returns the selected option
    # If it’s a multi-select dropdown → returns the first selected option
    def get_select_selected_value(self, locator, text_type="value"):
        try:
            element = self.find_element(locator)
            dropdown = Select(element)
            if text_type == "value":
                return dropdown.first_selected_option.get_attribute("value")
            elif text_type == "text":
                return dropdown.first_selected_option.text
            else:
                raise ValueError("text_type must be either 'value' or 'text'")
        except (TimeoutException, StaleElementReferenceException, ElementNotInteractableException) as e:
            assert False, f"Failed to get selected dropdown value for : {locator}  : {e}"

    # Search for an option in a dropdown and select it only if it exists
    def search_select_by_visible_text(self, locator, search_string):
        try:
            element = self.find_element(locator)
            dropdown = Select(element)
            desired_option = search_string
            for option in dropdown.options:
                if option.text == desired_option:
                    dropdown.select_by_visible_text(desired_option)
                    return
            assert False, f"Search string {search_string} not found in dropdown list: {locator}"
        except TimeoutException:
            assert False, f"Dropdown not found: {locator}"

    """
    Returns all currently selected values (text or value attribute) from a multi-select dropdown
    for validation or assertions in tests.
    """
    def get_multi_selected_values(self, locator, text_type):
        try:
            element = self.find_element(locator)
            dropdown = Select(element)
            if not dropdown.is_multiple:
                assert False, f"Dropdown is not multi-select : {locator}"
            if text_type == "text":
                return [option.text for option in dropdown.all_selected_options]
            elif text_type == "value":
                return [option.get_attribute("value") for option in dropdown.all_selected_options]
            else:
                raise ValueError("text_type must be either 'value' or 'text'")
        except (TimeoutException, UnexpectedTagNameException) as e:
            assert False, f"Failed to get selected values from dropdown : {locator} : {e}"

    def get_current_url(self):
        return self.driver.current_url

    def get_base_url(self):
        current_url_1 = (self.get_current_url()).split('/')[0:5]
        current_url_2 = '/'.join(current_url_1)
        return current_url_2

    def select_dropdown_by_keyboard(self, locator, down_count=1, delay=0.3):
        """
        Select dropdown option using keyboard (Arrow Down + Enter)

        :param locator: Locator tuple of dropdown element
        :param down_count: Number of ARROW_DOWN presses
                           1 = first option
                           2 = second option
        :param delay: Small delay between key presses
        """
        dropdown = self.find_element(locator)
        dropdown.click()

        for _ in range(down_count):
            dropdown.send_keys(Keys.ARROW_DOWN)
            time.sleep(delay)

        dropdown.send_keys(Keys.ENTER)

    def type_and_select(self, locator, text, arrow_count=1):
        """
        Types text into an element, then navigates options with Arrow Down and selects with Enter.

        :param locator: tuple, (By.<METHOD>, "locator_value")
        :param text: str, text to type first
        :param arrow_count: int, number of Arrow Down presses before Enter
        """
        try:
            element = self.driver.find_element(*locator)
            element.click()  # Focus on the element
            element.send_keys(text)  # Type text
            time.sleep(5)
            for _ in range(arrow_count):
                element.send_keys(Keys.ARROW_DOWN)
            element.send_keys(Keys.ENTER)
        except NoSuchElementException:
            assert False, f"Element not found: {locator}"

    def wait_for_visibility_by_xpath(self, xpath):
        try:
            return self.wait.until(
                EC.visibility_of_element_located((By.XPATH, xpath))
            )
        except TimeoutException:
            assert False, f"Element not visible for xpath: {xpath}"

    def find_child_elements_by_xpath(self, parent_element, child_xpath):
        """
        Finds multiple child elements inside a given parent element.

        parent_element : WebElement
        child_xpath     : relative XPath string (e.g., ".//div[@role='cell']")
        """
        try:
            # Return all child elements under the parent
            return parent_element.find_elements(By.XPATH, child_xpath)
        except TimeoutException:
            assert False, f"Child elements not found for xpath: {child_xpath}"
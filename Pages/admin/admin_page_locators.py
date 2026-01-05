from selenium.webdriver.common.by import By


class AdminPageLocators:
    add_admin = (By.XPATH, "//button[.//i[contains(@class,'bi-plus')] and normalize-space()='Add']")
    user_role_dropdown = (By.XPATH, "//label[normalize-space()='User Role'] /ancestor::div[contains(@class,"
                                    "'oxd-input-group')]  //div[contains(@class,'oxd-select-text-input')]")
    employee_name = (By.XPATH, "//input[@placeholder='Type for hints...']")
    status = (By.XPATH, "//label[normalize-space()='Status'] /ancestor::div[contains(@class,'oxd-input-group')]  "
                        "//div[contains(@class,'oxd-select-text-input')]")
    username = (By.XPATH, "//label[normalize-space()='Username']/following::input[1]")
    password = (By.XPATH, "//label[normalize-space()='Password']/ancestor::div[contains(@class,"
                          "'oxd-input-group')]//input[@type='password']")
    conf_password = (By.XPATH, "//label[normalize-space()='Confirm Password'] /ancestor::div[contains(@class,"
                               "'oxd-input-group')]//input[@type='password']")
    save_button = (By.XPATH, "//button[@type='submit' and normalize-space()='Save']")
    # USER_ROLE_OPTION = "//div[@role='listbox']//span[text()='{role}']"
    USER_ROLE_OPTION = (By.XPATH, "//div[normalize-space()='admin']")
    system_users = (By.XPATH, "//h5[normalize-space()='System Users']")
    user_name_in_user_management_table = (
        "//div[@role='row' and contains(@class,'oxd-table-row')]"
        "//div[@role='cell'][2][normalize-space()='{}']"
        "/ancestor::div[@role='row']"
    )
    user_management_table_cells = ".//div[@role='cell']"
    edit_admin_button = (
        "//div[@role='row' and contains(@class,'oxd-table-row')]"
        "[.//div[@role='cell' and contains(normalize-space(), '{}')]]"
        "//button[@type='button'][2]"
    )
    search_button = (By.XPATH, "//button[@type='submit' and normalize-space()='Search']")










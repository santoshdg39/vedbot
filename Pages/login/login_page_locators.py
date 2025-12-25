from selenium.webdriver.common.by import By


class LoginPageLocators:
    user_name = (By.XPATH, "//input[@name='username']")
    password = (By.XPATH, "//input[@name='password']")
    login_button = (By.XPATH, "//button[@type='submit']")
    ERROR_MESSAGE = (By.XPATH, "/html/body/div/div[1]/div/div[1]/div/div[2]/div[2]/div/div[1]/div[1]/p")
    user_profile_dropdown = (By.XPATH, "//i[@class='oxd-icon bi-caret-down-fill oxd-userdropdown-icon']")
    logout_button = (By.XPATH, "//a[normalize-space()='Logout']")
    login_page = (By.XPATH, "//h5[@class='oxd-text oxd-text--h5 orangehrm-login-title']")
    user_dropdown_name = (By.XPATH, "//p[@class='oxd-userdropdown-name']")
    account_disabled_msg = (By.XPATH,"//p[contains(@class,'oxd-alert-content-text')]")




from selenium.webdriver.common.by import By


class LoginPageLocators:
    user_name = (By.XPATH, "//input[@name='username']")
    password = (By.XPATH, "//input[@name='password']")
    login_button = (By.XPATH, "//button[@type='submit']")
    ERROR_MESSAGE = (By.XPATH, "/html/body/div/div[1]/div/div[1]/div/div[2]/div[2]/div/div[1]/div[1]/p")

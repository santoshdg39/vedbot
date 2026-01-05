from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager


class DriverManager:

    @staticmethod
    def set_common_options(options, headless):
        """Set common options for browsers"""
        if headless:
            options.add_argument("--headless=new")  # works for latest Chrome
            options.add_argument("--disable-gpu")
            options.add_argument("--window-size=1920,1080")
            options.add_argument("--no-sandbox")
            options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-notifications")
        options.add_argument("--disable-extensions")
        options.add_argument("--disable-infobars")
        return options

    @staticmethod
    def drivermanager(browser: str, headless: bool = False):
        browser = browser.lower()

        if browser == 'chrome':
            options = ChromeOptions()
            options = DriverManager.set_common_options(options, headless)
            # Automatically downloads correct ChromeDriver
            driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)

        elif browser == 'firefox':
            options = FirefoxOptions()
            if headless:
                options.add_argument("--headless")
            # Automatically downloads correct GeckoDriver
            driver = webdriver.Firefox(service=FirefoxService(GeckoDriverManager().install()), options=options)

        else:
            raise Exception(f"Incorrect Browser: {browser}. Supported browsers: Chrome, Firefox")

        driver.maximize_window()
        return driver

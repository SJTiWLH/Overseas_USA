import time

from selenium.webdriver.common.by import By
from src.utils.logger import setup_logger
logger = setup_logger(__name__)
class Login:
    def __init__(self, browser,username, password):
        self.browser = browser
        self.username = username
        self.password = password
        logger.info(self.username)
        logger.info(self.password)


    def login(self):
        self.browser.input_by_ID("user_email", self.username)
        self.browser.input_by_ID("user_password", self.password)
        time.sleep(2)
        self.browser.driver.find_element(By.CSS_SELECTOR, "div.icheckbox.icheck-item").click()
        self.browser.driver.find_element(By.NAME, "commit").click()
        self.browser.click_by_Class("button.primary.small")


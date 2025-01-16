import time
from telnetlib import EC

from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
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
    def not_pay_go_in(self):
        # 点击"Pay Visa Fee"按钮
        time.sleep(2)
        self.browser.driver.find_element(By.LINK_TEXT, "Pay Visa Fee").click()
        self.browser.click_by_Class("small-only-expanded")
    def paid_go_in(self,block_number):
        # 已经支付的人进入，根据护照号(block_number)进入
        time.sleep(2)
        # 根据护照号选客人
        self.select_people_for_passportNum(block_number)

    def select_people_for_passportNum(self, passport_num):
        # 根据护照号选客人
        WebDriverWait(self.browser.driver, 10).until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'application')))
        applications = self.browser.driver.find_elements(By.CLASS_NAME, 'application')
        for app in applications:
            try:
                WebDriverWait(app, 10).until(EC.presence_of_element_located((By.XPATH, f".//td[contains(text(), {passport_num})]")))
                # 如果找到了元素，执行点击等操作
                continue_button = app.find_element(By.XPATH, ".//a[contains(text(), 'Continue')]")
                continue_button.click()
                print("点击客人模块！")
                break  # 如果找到元素并点击了，可能需要跳出循环
            except :
                # 如果在当前app模块中没有找到元素，打印消息并继续下一个循环迭代
                print("在当前模块中未找到指定的护照号。")
                continue  # 继续检查下一个app模块
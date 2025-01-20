import time
import traceback
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
        # 登录账号密码
        self.browser.input_by_ID("user_email", self.username)
        self.browser.input_by_ID("user_password", self.password)
        time.sleep(2)
        self.browser.driver.find_element(By.CSS_SELECTOR, "div.icheckbox.icheck-item").click()
        self.browser.driver.find_element(By.NAME, "commit").click()

    def not_pay_go_in(self):
        # 进入未支付信息卡
        self.browser.click_by_Class("button.primary.small")
        # 点击"Pay Visa Fee"按钮
        time.sleep(2)
        self.browser.driver.find_element(By.LINK_TEXT, "Pay Visa Fee").click()
        self.browser.click_by_Class("small-only-expanded")
    def paid_go_in(self,block_number,xiugai):
        # 已经支付的人进入，根据护照号(block_number)进入
        time.sleep(2)
        # 根据护照号选客人
        self.select_people_for_passportNum(block_number)

        if xiugai == 0:
            # 第一次预约点0
            self.browser.driver.execute_script('document.getElementsByClassName("button small primary small-only-expanded")[0].click();')
        elif xiugai == 1:
            # 修改预约点3
            self.browser.driver.execute_script('document.getElementsByClassName("button small primary small-only-expanded")[3].click();')

    def select_people_for_passportNum(self, passport_num):
        # 根据护照号选客人
        applications = self.browser.driver.find_elements(By.CLASS_NAME, 'application')
        for app in applications:
            try:
                time.sleep(5)
                passport_elem = app.find_element(By.XPATH, ".//table[.//td[contains(@class,'show-for-medium')]]")
                passport_num = passport_elem.text  # 护照号所在的table全部信息都获取到
                if passport_num in passport_num:
                    continue_button = app.find_element(By.XPATH, ".//a[contains(text(), 'Continue')]")
                    continue_button.click()
                    print("点击客人模块！")
                break
            except :
                traceback.print_exc()
                print("在当前模块中未找到指定的护照号。")
                continue
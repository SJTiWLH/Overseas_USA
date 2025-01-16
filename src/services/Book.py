import logging
import time

from src.services.Browser import Browser
from src.services.Login import Login
from src.utils.logger import setup_logger
from src.config import AppConfig


logger = setup_logger(__name__)

class Book:
    def __init__(self,green_people_arr):
        self.green_people_arr = green_people_arr

    def Book_App(self):
        if len(self.green_people_arr) == 0:
            logger.info(f"无满足条件客人，退出预约操作。继续监控")
            return
        logger.info(f"开始预约操作")
        print(self.green_people_arr)
        for person in self.green_people_arr:
            self.Book_of_Thread(person["领区"],person["账号(Email)"],person["密码"],person["预约时间"],person["操作客人的护照号"])
        time.sleep(5000)

    def Book_of_Thread(self,lingqu,username,password,eTime,passport):
        print("-------------------")
        logger.info(f"{lingqu},{username},{password},{eTime},{passport}")
        # 开始预约操作。已经拿到信息。
        appConfig = AppConfig()
        TARGET_URL = appConfig.getUrl(None,lingqu)
        logger.info("启动应用程序！！！！！！！！")
        browser = Browser()
        browser.open_url(TARGET_URL)
        user_login = Login(browser, username, password)
        user_login.login()





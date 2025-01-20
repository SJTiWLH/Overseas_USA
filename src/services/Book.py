import logging
import time

from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select

from src.services.Browser import Browser
from src.services.Login import Login
from src.services.WatchData import WatchData
from src.utils.logger import setup_logger
from src.config import AppConfig


logger = setup_logger(__name__)

class Book:
    def __init__(self,green_people_arr,from_contry):
        self.green_people_arr = green_people_arr
        self.from_contry = from_contry

    def Book_App(self):
        if len(self.green_people_arr) == 0:
            logger.info(f"无满足条件客人，退出预约操作。继续监控")
            return
        logger.info(f"开始预约操作")
        print(self.green_people_arr)
        for person in self.green_people_arr:
            self.Book_of_Thread(person["领区"],person["账号(Email)"],person["密码"],person["预约时间"],person["操作客人的护照号"],person["是否修改"])
        time.sleep(5000)

    def Book_of_Thread(self,lingqu,username,password,eTime,passport,xiugai):
        print("-------------------")
        logger.info(f"领区:{lingqu}, 账号:{username}, 密码:{password}, 预约时间:{eTime}, 护照号:{passport}, 是否修改:{xiugai}")
        # 开始预约操作。已经拿到信息。
        appConfig = AppConfig()
        TARGET_URL = appConfig.getUrl(self.from_contry)
        logger.info("启动应用程序！！！！！！！！")
        browser = Browser()
        browser.open_url(TARGET_URL)
        user_login = Login(browser, username, password)
        user_login.login()
        user_login.paid_go_in(password,xiugai)
        watch = WatchData(browser, lingqu)
        watch.pay_getData(lingqu,eTime)

        time.sleep(2000)







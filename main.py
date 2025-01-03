import time

from src.services.Browser import Browser
from src.utils.logger import setup_logger
from src.config import AppConfig
from src.services.Login import Login

logger = setup_logger(__name__)

def main():
    logger.info("启动应用程序！！！！！！！！")
    browser = Browser()
    browser.open_url(AppConfig.TARGET_URL)
    user_login = Login(browser,"wuaivisa013@163.com","Xiaoxin123")
    user_login.login()
    time.sleep(2000)



if __name__ == '__main__':
    main()
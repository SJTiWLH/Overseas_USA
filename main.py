import time
import traceback

from src.services.Browser import Browser
from src.utils.logger import setup_logger
from src.config import AppConfig
from src.services.Login import Login
from src.services.WatchData import WatchData

logger = setup_logger(__name__)

def main():
    try:
        logger.info("启动应用程序！！！！！！！！")
        browser = Browser()
        browser.open_url(AppConfig.TARGET_URL)
        user_login = Login(browser, "wuaivisa013@163.com", "Xiaoxin123")
        user_login.login()
        user_login.not_pay_go_in()
        watch = WatchData(browser)
        watch.not_pay_getData()
        time.sleep(2000)
    except:
        traceback.print_exc()
        time.sleep(2000)



if __name__ == '__main__':
    main()


import time
import traceback

from src.services.Browser import Browser
from src.utils.logger import setup_logger
from src.config import AppConfig
from src.services.Login import Login
from src.services.WatchData import WatchData
from src.services.Book import Book
from src.services.get_excel import getExcel

logger = setup_logger(__name__)

def main():
    getuser = getExcel()
    all_Jiankong = getuser.username_jiankong()
    index = 0
    while True:
        try:
            jiankong_Person = all_Jiankong[index]
            index = (index + 1) % len(all_Jiankong) # 循环对监控账号进行登录。
            from_contry , username , password = jiankong_Person["国家"],jiankong_Person["账号"],jiankong_Person["密码"]
            appConfig= AppConfig()
            TARGET_URL = appConfig.getUrl(from_contry)
            logger.info("启动应用程序！！！！！！！！")
            browser = Browser()
            browser.open_url(TARGET_URL)
            user_login = Login(browser, username, password)
            user_login.login()
            user_login.not_pay_go_in()
            watch = WatchData(browser,from_contry)
            green_people_arr = watch.not_pay_getData()
            book = Book(green_people_arr,from_contry)
            book.Book_App()
            time.sleep(2)
            browser.close()

        except:
            time.sleep(20)
            traceback.print_exc()
            browser.close()




if __name__ == '__main__':
    main()
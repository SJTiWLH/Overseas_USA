from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait


class Browser:
    def __init__(self):

        # 设置为无头模式（即浏览器在后台运行，不显示界面），如果不需要可注释掉这行
        # ChromiumOptions.add_argument("--headless")
        # self.driver = webdriver.Chrome(options=self.ChromiumOptions)
        self.driver = webdriver.Chrome()
    def open_url(self, url):
        self.driver.get(url)

    def close(self):
        self.driver.close()
    def input_by_ID(self, ElmID,text):
        # 显示等待元素加载之后，根据ID，输入内容
        email_input = WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.ID, ElmID )))  # "user_email"
        email_input.send_keys(text)
    def click_by_Class(self, ElmClass):
        # 显示等待元素加载之后，根据Class，点击元素
        continue_button = WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.CLASS_NAME, ElmClass)))
        continue_button.click()





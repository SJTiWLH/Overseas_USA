from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from datetime import date
import traceback
import sys
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import re
import time
import subprocess
import requests

city_translations = {
    'Ottawa': '渥太华',
    'Toronto': '多伦多',
    'Vancouver': '温哥华',
    'Calgary': '卡尔加里',
    'Halifax': '哈利法克斯',
    'Montreal': '蒙特利尔',
    'Quebec City': '魁北克城',
    'London': '伦敦',
    'Belfast': '贝尔法斯特',
    'Buenos Aires' : '布宜诺斯艾利斯',
    'Santiago' : '圣地亚哥'
}
month_translations = {
    'January': '1',
    'February': '2',
    'March': '3',
    'April': '4',
    'May': '5',
    'June': '6',
    'July': '7',
    'August': '8',
    'September': '9',
    'October': '10',
    'November': '11',
    'December': '12'
}
old_data = {
    'Ottawa': 'No Appointments Available',
    'Toronto': 'No Appointments Available',
    'Vancouver': 'No Appointments Available',
    'Calgary': 'No Appointments Available',
    'Halifax': 'No Appointments Available',
    'Montreal': 'No Appointments Available',
    'Quebec City': 'No Appointments Available',
    'London': 'No Appointments Available',
    'Belfast': 'No Appointments Available',
    'Buenos Aires': 'No Appointments Available',
    'Santiago':'No Appointments Available'
}
city_need_data = {
    'Ottawa': '2023.11.24-2024.04.30',
    'Toronto': '2023.11.24-2024.05.31',
    'Vancouver': '2023.11.24-2024.04.30',
    'Calgary': '2023.11.24-2024.04.30',
    'Halifax': '2023.11.24-2024.05.31',
    'Montreal': '2023.11.24-2024.04.30',
    'Quebec City': '2023.11.24-2024.04.30',
    'London': '2023.12.18-2024.01.31',
    'Belfast': '2023.11.24-2023.12.30',
    'Buenos Aires':'2023.11.24-2024.05.31',
    'Santiago' : '2023.11.24-2024.05.31'
}
#封装发送邮件的函数
def send_email(sender, receiver, password,title,text_content):
    # QQ邮箱SMTP服务器设置
    smtp_server = 'smtp.qq.com'
    smtp_port = 465  # 使用SSL
    sender_email = sender  # 发件人邮箱地址
    receiver_emails = receiver  # 收件人邮箱地址
    password = password  # SMTP服务的授权码

    # 创建邮件对象
    message = MIMEMultipart("alternative")
    message["Subject"] = title
    message["From"] = sender_email
    message["To"] = ', '.join(receiver_emails)

    # 创建邮件内容
    text = f"""\
    {text_content}
    """

    # 将文本和HTML版本添加到邮件中
    part1 = MIMEText(text, "plain")
    message.attach(part1)
    server = None
    # 发送邮件
    try:
        # 连接到SMTP服务器
        server = smtplib.SMTP_SSL(smtp_server, smtp_port)  # 注意这里使用的是SMTP_SSL
        server.login(sender_email, password)

        # 发送邮件
        server.sendmail(sender_email, receiver_emails, message.as_string())
        print("Email sent successfully!")
    except Exception as e:
        # 打印任何错误消息
        print("An error occurred:", e)
    finally:
        if server is not None:
            server.quit()

#封装时间段转换为字符串
def generate_date_range_string(input_dates):
    from datetime import datetime, timedelta

    # 分割字符串以获取各个时间段
    date_ranges = input_dates.split(';')

    # 分别处理每个时间段
    all_dates = []
    for date_range in date_ranges:
        start_date_str, end_date_str = date_range.split('-')

        # 将字符串日期转换为datetime对象
        start_date = datetime.strptime(start_date_str, "%Y.%m.%d")
        end_date = datetime.strptime(end_date_str, "%Y.%m.%d")

        # 生成日期范围内的所有日期
        current_date = start_date
        while current_date <= end_date:
            all_dates.append(current_date.strftime("%Y-%m-%d"))
            current_date += timedelta(days=1)

    # 将所有日期列表转换为字符串
    return ','.join(all_dates)

Shen = "50269294@qq.com"
Liang = "1317095685@qq.com"
Hao = "2536608618@qq.com"
Tong = "1316151698@qq.com"
Hang = "2233852143@qq.com"
XiaoXin = "928781367@qq.com"
XiaoYi = "382308885@qq.com"
XiaoMi = "1951645633@qq.com"
XiaoMai = "540727185@qq.com"
Fanfan = "2194025327@qq.com"
Mail_send2 = [Tong,XiaoMi,XiaoXin,Shen]
nameid = 4
From_GuoJia = "加拿大"
if From_GuoJia == "英国":
    website = "https://ais.usvisa-info.com/en-gb/niv/users/sign_in"
    username = "wuaivisa015@163.com"
    username1 = "wuaivisa016@163.com"
    username2 = "wuaivisa017@163.com"
    username3 = "wuaivisa018@163.com"
    username4 = "wuaivisa019@163.com"
    username5 = "wuaivisa020@163.com"
    username6 = "wuaivisa021@163.com"
    username7 = "wuaivisa022@163.com"
    username8 = "wuaivisa023@163.com"
    username_arr = [username,username1,username2,username3,username4,username5,username6,username7,username8]
    print(username_arr)
    password = "Xiaoxin123"
elif From_GuoJia == "加拿大":
    website = "https://ais.usvisa-info.com/en-ca/niv/users/sign_in"
    username = "wuaivisa010@163.com"
    username1 = "wuaivisa011@163.com"
    username2 = "wuaivisa012@163.com"
    username3 = "wuaivisa013@163.com"
    username4 = "wuaivisa014@163.com"
    username_arr = [username, username1, username2, username3, username4]
    password = "Xiaoxin123"
elif From_GuoJia == "阿根廷":
    website = "https://ais.usvisa-info.com/en-ar/niv/users/sign_in"
    username = "wuaivisa024@163.com"
    username_arr = [username]
    password = "Xiaoxin123"
elif From_GuoJia == "智利":
    website = "https://ais.usvisa-info.com/en-cl/niv/users/sign_in"
    username = "wuaivisa025@163.com"
    username_arr = [username]
    password = "Xiaoxin123"


while True:
    try:
                nameid = nameid + 1
                if nameid > 4:
                    nameid = 0
                # 设置Chrome的WebDriver
                driver = webdriver.Chrome()
                # 打开网址
                driver.get(website)

                # 显式等待，直到邮箱输入框可见
                email_input = WebDriverWait(driver, 10).until(
                    EC.visibility_of_element_located((By.ID, "user_email"))
                )

                # 在邮箱输入框中填入指定的邮箱地址
                email_input.send_keys(username_arr[nameid])

                # 显式等待，直到密码输入框可见
                password_input = WebDriverWait(driver, 10).until(
                    EC.visibility_of_element_located((By.ID, "user_password"))
                )

                # 在密码输入框中填入指定的密码
                password_input.send_keys(password)

                # 定位可能遮挡复选框的元素
                div_element = driver.find_element(By.CSS_SELECTOR, "div.icheckbox.icheck-item")

                # 使用ActionChains来点击该元素
                ActionChains(driver).move_to_element(div_element).click().perform()

                # 定位“Sign In”按钮并单击
                sign_in_button = driver.find_element(By.NAME, "commit")
                sign_in_button.click()

                # 显式等待，contniue
                continue_button = WebDriverWait(driver, 10).until(
                    EC.visibility_of_element_located((By.CLASS_NAME, "button.primary.small"))
                )
                continue_button.click()

                # 显式等待，直到链接文本出现
                pay_visa_fee_link = WebDriverWait(driver, 10).until(
                    EC.visibility_of_element_located((By.LINK_TEXT, "Pay Visa Fee"))
                )
                # 单击链接
                pay_visa_fee_link.click()

                # 显式等待，直到"Pay Visa Fee"按钮可见 button small primary small-only-expanded
                continue_link = WebDriverWait(driver, 10).until(
                    EC.visibility_of_element_located((By.CLASS_NAME, "small-only-expanded"))
                )
                continue_link.click()

                # 正则表达式匹配文段中的城市
                pattern_city = r"London|Belfast|Ottawa|Toronto|Vancouver|Calgary|Halifax|Montreal|Quebec City|Buenos Aires|Santiago"
                # 正则表达式匹配文段中的月份
                pattern_months = r"\b(?:January|February|March|April|May|June|July|August|September|October|November|December)\b"
                # 正则表达式匹配四位数字
                pattern_four_digits = r"\b\d{4}\b"
                # 正则表达式匹配二位数字
                pattern_two_digits = r"\b\d{2}\b"
                # 正则表达式匹配一位数字
                pattern_one_digits = r"\b\d{1}\b"


                while True:
                    try:
                        # 某些可能引发异常的操作
                        print("这是一个死循环！")
                        # 定位所有class为"text-right"的元素
                        tr_elements = driver.find_elements(By.XPATH, "//td[@class='text-right']/ancestor::tr")
                        # 确定是否还在当前页面
                        if tr_elements == []:
                            print("不在日期页面，跳出死循环，重新启动浏览器。")
                            driver.quit()
                            break
                        for tr_element in tr_elements:
                            print("城市与日期："+tr_element.text)

                            # 匹配城市
                            matches_city = re.findall(pattern_city, tr_element.text)
                            city_english = matches_city[0]
                            print(city_english)

                            # 将英文地名翻译为中文
                            city_chinese = city_translations[city_english]
                            print(city_chinese)

                            #检查是否可查看日期
                            contains_No = "No Appointments Available" in tr_element.text
                            print(contains_No)

                            if contains_No :
                                #没有日期，将No Appointments Available 存入now_data
                                print("No Appointments Available")
                                Now_data_str = "No Appointments Available"
                            else:
                                #获取日期存入now_data

                                #获取年月日
                                #获取年
                                matches_year = re.findall(pattern_four_digits, tr_element.text)
                                year = matches_year[0]
                                print(year)
                                #获取月
                                matches_month = re.findall(pattern_months, tr_element.text)
                                month = month_translations[matches_month[0]]
                                print(month)
                                # 获取日
                                matches_day = re.findall(pattern_two_digits, tr_element.text)
                                if matches_day == []:
                                    matches_day = re.findall(pattern_one_digits, tr_element.text)
                                day = matches_day[0]
                                print(day)
                                year = int(year)
                                month = int(month)
                                day = int(day)
                                # 将年、月、日变量组合成一个date对象
                                Now_data = date(year, month, day)
                                Now_data_str = Now_data.strftime("%Y-%m-%d")
                            if Now_data_str == old_data[city_english]:
                                print("日期未发生变化")

                            elif Now_data_str != old_data[city_english]:
                                print("日期发生变化！")

                                #发邮件通知，sender：发件人； receiver：收件人； password：授权码； title：标题； text_content：内容；
                                title = "【" + From_GuoJia + "|美国】" + city_chinese
                                lingqu = city_chinese
                                text_content = "【" + From_GuoJia + "|美国】" + city_chinese + "\n最早日期发生变化\n当前最早日期为："+Now_data_str+"\nIP:8.130.11.0"

                                # ——————————发件人———收件人————授权码————标题————内容——————————
                                # send_email("1316151698@qq.com", '1316151698@qq.com', "xepktuqsdrtnjeaa", title, text_content)

                                old_data[city_english] = Now_data_str
                                #查看是否在需求范围内
                                input_dates = city_need_data[city_english]
                                date_string = generate_date_range_string(input_dates)
                                print(date_string)
                                is_in_need = Now_data_str in date_string
                                if is_in_need == True :
                                    print("日期在需求范围内")
                                    # ——————————发件人———收件人————授权码————标题————内容——————————
                                    title = "【" + From_GuoJia + "|美国】" + city_chinese + "需求范围内"
                                    text_content = "【" + From_GuoJia + "|美国】" + city_chinese + "\n最早日期在需求范围内，\n当前最早日期为：" + Now_data_str + "\n请立即进行登录预约。\nIP:8.130.11.0"
                                    send_email("1316151698@qq.com", Mail_send2, "xepktuqsdrtnjeaa", title, text_content)
                        print("当前最早日期集合：")
                        print(old_data)
                        time.sleep(10)
                        driver.refresh()
                        # 要发送的数据
                        data = {"ipAddr": "8.130.161.192", "task": "阿根廷刷美签"}
                        # 发送 POST 请求
                        response = requests.post("http://54.169.239.115:8808/wuai/system/sys/saveServiceLog", json=data, timeout=60)
                        print(response)
                        time.sleep(2)
                    except Exception as e:
                        print("发生错误：", e)
                        exc_type, exc_value, exc_traceback = sys.exc_info()
                        # 提取异常信息
                        traceback_details = traceback.extract_tb(exc_traceback)
                        # 获取错误发生的行号
                        line_number = traceback_details[-1].lineno
                        print(f"An error occurred on line: {line_number}")
                        time.sleep(5)
                        # 关闭浏览器
                        driver.quit()
                        break

    except Exception as e:
        print("发生了一个错误:", e)
        exc_type, exc_value, exc_traceback = sys.exc_info()
        # 提取异常信息
        traceback_details = traceback.extract_tb(exc_traceback)
        # 获取错误发生的行号
        line_number = traceback_details[-1].lineno
        print(f"An error occurred on line: {line_number}")
        # 关闭浏览器
        driver.quit()



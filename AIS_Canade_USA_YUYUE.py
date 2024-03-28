import inspect
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from datetime import date
import threading
import time
import openpyxl
from datetime import datetime
import traceback
import sys
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import re
import time
import subprocess
import requests
import logging
import pandas as pd
import lackey
import pywinauto
import click_quickq
# 配置日志格式，包括时间戳
# logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')


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
    'Santiago' : '圣地亚哥',
    'Brasilia': '巴西利亚',
    'Rio de Janeiro': '里约热内卢',
    'Sao Paulo': '圣保罗',
    'Recife': '累西腓',
    'Porto Alegre': '波尔图阿莱格里',
    'Abu Dhabi':'阿布扎比',
    'Dubai':'迪拜',
    'La Paz':'阿巴斯',
    'Paris':'巴黎'
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
    'Santiago':'No Appointments Available',
    'Brasilia':'No Appointments Available',
    'Rio de Janeiro':'No Appointments Available',
    'Sao Paulo':'No Appointments Available',
    'Recife':'No Appointments Available',
    'Porto Alegre':'No Appointments Available',
    'Abu Dhabi':'No Appointments Available',
    'Dubai':'No Appointments Available',
    'La Paz':'No Appointments Available',
    'Paris':'No Appointments Available'
}
city_need_data = {
    'Ottawa': '2023.11.24-2024.04.30',
    'Toronto': '2023.11.24-2024.05.31',
    'Vancouver': '2023.11.24-2024.04.30',
    'Calgary': '2023.11.24-2024.04.30',
    'Halifax': '2023.11.24-2024.05.31',
    'Montreal': '2023.11.24-2024.04.30',
    'Quebec City': '2023.11.24-2024.04.30',
    'London': '2023.12.18-2024.05.30',
    'Belfast': '2023.12.18-2024.05.30',
    'Buenos Aires':'2023.11.24-2024.05.31',
    'Santiago' : '2023.11.24-2024.05.31',
    'Brasilia':'2023.11.24-2024.04.30',
    'Rio de Janeiro':'2023.11.24-2024.04.30',
    'Sao Paulo':'2023.11.24-2024.04.30',
    'Recife':'2023.11.24-2024.04.30',
    'Porto Alegre':'2023.11.24-2024.04.30',
    'Abu Dhabi':'2023.11.24-2024.04.30',
    'Dubai':'2023.11.24-2024.04.30',
    'La Paz':'2023.11.24-2024.04.30',
    'Paris':'2023.11.24-2024.04.30'
}
# 正则表达式匹配文段中的城市
pattern_city = r"London|Belfast|Ottawa|Toronto|Vancouver|Calgary|Halifax|Montreal|Quebec City|Buenos Aires|Santiago|Brasilia|Rio de Janeiro|Sao Paulo|Recife|Porto Alegre|Abu Dhabi|Dubai|La Paz|Paris"
# 正则表达式匹配文段中的月份
pattern_months = r"\b(?:January|February|March|April|May|June|July|August|September|October|November|December)\b"
# 正则表达式匹配四位数字
pattern_four_digits = r"\b\d{4}\b"
# 正则表达式匹配二位数字
pattern_two_digits = r"\b\d{2}\b"
# 正则表达式匹配一位数字
pattern_one_digits = r"\b\d{1}\b"

def quickq ():
    number_two = 0
    path = 'C:/Users/Administrator/AppData/Local/QuickQ/QuickQ.exe'
    app = pywinauto.Application().start(path)

    # 给应用程序一些时间来加载
    time.sleep(5)  # 这里的时间可能需要根据应用程序的实际加载时间进行调整
    try:
        # 加载要点击的图片
        target_image = 'C:/Slot/UK/Other/img/quickq5.png'
        target_location = lackey.find(target_image)
        x, y = target_location.getX(), target_location.getY()
        new_x, new_y = x + 100, y + 100
        click_location = lackey.Location(new_x, new_y)
        lackey.click(click_location)
    except:
        target_image = 'C:/Slot/UK/Other/img/quickq1.png'
        lackey.click(target_image)
        number_two = 1

    if number_two == 0:
        target_image = 'C:/Slot/UK/Other/img/quickq1.png'
        if lackey.exists(target_image):
            lackey.click(target_image)
        else:
            print(f"未找到图像: {target_image}")
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

#封装 查找满足城市要求与日期要求的客人。
def find_all_target_data_within_date(file_name, target_value, given_date):
    # 加载 Excel 文件
    workbook = openpyxl.load_workbook(file_name)
    sheet = workbook.active
    # 用于存储找到的符合条件的所有行数据
    matching_rows = []
    # 遍历 B 列的所有单元格
    for row in range(1, sheet.max_row + 1):
        cell_value = sheet[f"B{row}"].value #获取B列的领区
        if cell_value is None:
            # 如果遇到空单元格，停止读取
            break
        if cell_value == target_value and sheet[f"G{row}"].value != "0":  #获取G列的预约是否为1
            # 获取 E 列的时间范围
            date_range = sheet[f"E{row}"].value
            string_data = generate_date_range_string(date_range)
            # 检查给定的日期是否在时间范围内
            if given_date in string_data:
                # 找到符合条件的数据，获取整行数据并添加到列表中
                matching_rows.append([cell.value for cell in sheet[row]])

    return matching_rows if matching_rows else []

def printtime(*args, **kwargs):
    current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    # 获取当前执行的代码行号
    frame = inspect.currentframe()
    caller = frame.f_back
    lineno = caller.f_lineno
    print(f"[{current_time} - Line {lineno}]",*args,**kwargs)

#---------------------------------------多线程预约函数-------------------------------------------
def data_start_end(date_range):
    date_ranges = date_range.split(';')  # 分割得到所有日期区间
    # 初始化开始和截止日期为第一个区间的值
    start_date_str, end_date_str = date_ranges[0].split('-')
    # 遍历所有日期区间
    for date_rangeone in date_ranges:
        start_str, end_str = date_rangeone.split('-')  # 分割每个日期区间得到开始和截止日期
        # 更新最早的开始日期和最晚的截止日期
        if start_str < start_date_str:
            start_date_str = start_str
        if end_str > end_date_str:
            end_date_str = end_str
    # 输出最早的开始日期和最晚的截止日期
    return start_date_str, end_date_str

def booking(lingqu,username,password,date_range,xiugai):
    from selenium.webdriver.common.action_chains import ActionChains
    from selenium import webdriver
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    from selenium.webdriver.support.ui import Select
    import datetime
    import traceback
    import sys
    import time
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

    city_translations = {
        '渥太华': 'Ottawa',
        '多伦多': 'Toronto',
        '温哥华': 'Vancouver',
        '卡尔加里': 'Calgary',
        '哈利法克斯': 'Halifax',
        '蒙特利尔': 'Montreal',
        '魁北克城': 'Quebec City',
        '伦敦': 'London',
        '贝尔法斯特': 'Belfast',
        '布宜诺斯艾利斯': 'Buenos Aires',
        '圣地亚哥': 'Santiago'
    }
    xiugai = int(xiugai)
    Chinese_lingqu = lingqu
    lingqu = city_translations[lingqu]
    print(lingqu)
    if lingqu == "Ottawa" or lingqu == "Toronto" or lingqu == "Vancouver" or lingqu == "Calgary" or lingqu == "Halifax" or lingqu == "Montreal" or lingqu == "Quebec City":
        website = "https://ais.usvisa-info.com/en-ca/niv/users/sign_in"
    elif lingqu == "London" or lingqu == "Belfast":
        website = "https://ais.usvisa-info.com/en-gb/niv/users/sign_in"
    elif lingqu == "Buenos Aires":
        website = "https://ais.usvisa-info.com/en-ar/niv/users/sign_in"
    elif lingqu == "Santiago":
        website = "https://ais.usvisa-info.com/en-cl/niv/users/sign_in"
    print(lingqu+"-"+username+"-"+password+"-"+date_range)
    print(website)
    thread_name = Chinese_lingqu+"-"+username+":"
    cyclic = 1
    while cyclic == 1:
        try:
            printtime("------------------------进程开始------------------------")
            # 设置Chrome的WebDriver
            driver = webdriver.Chrome()
            # 打开网址
            driver.get(website)
            # 显式等待，直到邮箱输入框可见
            email_input = WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located((By.ID, "user_email"))
            )
            email_input.send_keys(username)

            # 显式等待，直到密码输入框可见
            password_input = WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located((By.ID, "user_password"))
            )
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
            printtime("点击continiu成功，接下来进入预约。")
            # 点击查看日期
            print(xiugai)
            # 点击第一个按钮
            if xiugai == 0:
                # 第一次预约点0
                print("开始点击")
                try:
                    driver.execute_script(
                        'document.getElementsByClassName("button small primary small-only-expanded")[0].click();')
                    print("点击成功")
                except:
                    print("JS点击失败")

                # 等待页面加载
                time.sleep(5)
                # 下拉框选择领区
                select_element = driver.find_element(By.ID, "appointments_consulate_appointment_facility_id")
                # 创建 Select 对象
                select = Select(select_element)
                # 根据文本选择 "London"
                select.select_by_visible_text(lingqu)

            elif xiugai == 1:
                # 修改预约点3
                driver.execute_script(
                    'document.getElementsByClassName("button small primary small-only-expanded")[3].click();')
            # 打开日历
            input_element = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, ".yatri_date input"))
            )
            input_element.click()

            # 翻看日历
            try:
                # 等待日历加载
                driver.implicitly_wait(5)

                string_data = generate_date_range_string(date_range)
                print(string_data)
                # 将日期范围分割成开始日期和结束日期
                start_date_str, end_date_str = data_start_end(date_range)
                print(start_date_str, end_date_str)
                # 从每个日期中提取年和月
                start_year, start_month = map(int, start_date_str.split('.')[:2])
                end_year, end_month = map(int, end_date_str.split('.')[:2])

                start_date = (start_year, start_month)
                end_date = (end_year, end_month)

                while True:
                    # 获取左侧日历的年份和月份
                    left_calendar = driver.find_element(By.CSS_SELECTOR, ".ui-datepicker-group-first .ui-datepicker-title")
                    left_month, left_year = left_calendar.text.split()
                    left_month = datetime.datetime.strptime(left_month, "%B").month
                    left_year = int(left_year)

                    # 检查是否到达开始日期
                    if (left_year, left_month) >= start_date:
                        print(thread_name+"到达开始日期")
                        time.sleep(2)
                        break

                    # 点击向右翻页
                    next_button = driver.find_element(By.CSS_SELECTOR, ".ui-datepicker-next")
                    next_button.click()

                yuyue_state = 0
                while True:
                    # 获取右侧日历的年份和月份
                    right_calendar = driver.find_element(By.CSS_SELECTOR, ".ui-datepicker-group-last .ui-datepicker-title")
                    right_month, right_year = right_calendar.text.split()
                    right_month = datetime.datetime.strptime(right_month, "%B").month
                    right_year = int(right_year)
                    # 获取两个日历的月份和年份
                    calendars = driver.find_elements(By.CSS_SELECTOR, ".ui-datepicker-group")
                    for calendar in calendars:
                        header = calendar.find_element(By.CSS_SELECTOR, ".ui-datepicker-header .ui-datepicker-title")
                        month_year = header.text.split()
                        month = datetime.datetime.strptime(month_year[0], "%B").month
                        year = int(month_year[1])
                        print(f"{thread_name}日历月份: {month}, 日历年份: {year}")
                        # 获取可点击的日期
                        clickable_dates = calendar.find_elements(By.CSS_SELECTOR, "td:not(.ui-datepicker-unselectable) a")
                        for date in clickable_dates:
                            print(f"{thread_name}可点击的日期: {date.text}")
                            year = int(year)
                            month = int(month)
                            day = int(date.text)
                            green_date = "{:04d}-{:02d}-{:02d}".format(year, month, day)
                            print(green_date)
                            # 判断是否在日期内
                            if green_date in string_data:
                                print(green_date + "在需求范围内")
                                print(thread_name+"点击日期！")
                                date.click()
                                print(thread_name+"点击成功！")
                                # 选择时间
                                print("选择时间！")
                                times = None
                                attempts = 0
                                while attempts < 10 and times is None:
                                    try:
                                        times = driver.execute_script(
                                            'return document.getElementsByName("appointments[consulate_appointment][time]")[0].innerText;')
                                        if times:  # 如果times非空，跳出循环
                                            break
                                    except Exception as e:
                                        print("尝试获取元素时出错：", e)
                                    print("时间未加载完毕，循环获取中.........")
                                    time.sleep(1)  # 等待1秒后再次尝试
                                    attempts += 1
                                if times is None:
                                    print("无可选时间")
                                else:
                                    print("获取到的时间：", times)
                                if times != None:
                                    driver.execute_script(
                                        'document.getElementsByName("appointments[consulate_appointment][time]")[0].selectedIndex = 1;')
                                    print("选择成功！")
                                # 点击提交
                                # 定位到按钮元素
                                submit_button = driver.find_element(By.ID, "appointments_submit")
                                submit_button.click()
                                if xiugai == "1":
                                    # 修改预约，点击确定
                                    a = 1
                                yuyue_state = 1
                                break

                    if yuyue_state == 1:
                        print(thread_name+"预约成功。")
                        printtime("------------------------进程预约成功------------------------")
                        title = "【"+Chinese_lingqu+"|美签】"+green_date
                        text_content =  thread_name+ green_date + "\n预约成功！请立即登陆服务器确认。\nIP:"+ip
                        send_email("1316151698@qq.com", Mail_send2, "xepktuqsdrtnjeaa", title, text_content)
                        time.sleep(50000)
                        print("跳出循环")
                        cyclic = 0
                        break
                    if (right_year, right_month) == end_date:
                        print(thread_name+"到达截止日期，未发现可预约日期")
                        print("跳出循环")
                        cyclic = 0
                        break

                    # 点击向右翻页
                    next_button = driver.find_element(By.CSS_SELECTOR, ".ui-datepicker-next")
                    next_button.click()

            except Exception as e:
                print(thread_name + "线程异常")
                printtime("------------------------线程异常------------------------")
                exc_type, exc_value, exc_traceback = sys.exc_info()
                # 提取异常信息
                traceback_details = traceback.extract_tb(exc_traceback)
                # 获取错误发生的行号
                line_number = traceback_details[-1].lineno
                print(f"An error occurred: {e}")
                print(f"An error occurred on line: {line_number}")
                time.sleep(5)
        except Exception as e:
            print(thread_name + "线程异常")
            printtime("------------------------线程异常------------------------")
            exc_type, exc_value, exc_traceback = sys.exc_info()
            # 提取异常信息
            traceback_details = traceback.extract_tb(exc_traceback)
            # 获取错误发生的行号
            line_number = traceback_details[-1].lineno
            print(f"An error occurred: {e}")
            print(f"An error occurred on line: {line_number}")
            time.sleep(5)
            driver.quit()

#---------------------------------------------------------------------------------------------
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

# 将Excel文件路径替换成你的文件路径
#---------------------------------------------------------------------------------------------
# 设置单刷国家
From_GuoJia = "加拿大"
ip = "39.98.220.155"
#---------------------------------------------------------------------------------------------

file_path = r'C:\Users\Administrator\Desktop\境外美签监控.xlsx'
df = pd.read_excel(file_path)
city_need_data = pd.Series(df['监控范围/日期'].values, index=df['监控范围/领区']).to_dict()
solo_Jankong_df = df[(df['监控类型'] == 1) & (df['国家'] == From_GuoJia)]
print(solo_Jankong_df)
username_values = solo_Jankong_df['账号'].tolist()
print(username_values)
password_values = solo_Jankong_df['密码'].tolist()
print(password_values)
country_values = solo_Jankong_df['国家'].tolist()
print(country_values)

len(username_values)

cishu = 0

while True:
    try:
                all_Num = len(username_values)-1
                if cishu > all_Num:
                    cishu = 0
                From_GuoJia = country_values[cishu]
                if From_GuoJia == "英国":
                    website = "https://ais.usvisa-info.com/en-gb/niv/users/sign_in"
                elif From_GuoJia == "加拿大":
                    website = "https://ais.usvisa-info.com/en-ca/niv/users/sign_in"
                elif From_GuoJia == "阿根廷":
                    website = "https://ais.usvisa-info.com/en-ar/niv/users/sign_in"
                elif From_GuoJia == "智利":
                    website = "https://ais.usvisa-info.com/en-cl/niv/users/sign_in"
                elif From_GuoJia == "巴西":
                    website = "https://ais.usvisa-info.com/en-br/niv/users/sign_in"
                elif From_GuoJia == "阿联酋":
                    website = "https://ais.usvisa-info.com/en-ae/niv/users/sign_in"
                elif From_GuoJia == "玻利维亚":
                    website = "https://ais.usvisa-info.com/en-bo/niv/users/sign_in"
                elif From_GuoJia == "法国":
                    website = "https://ais.usvisa-info.com/en-fr/niv/users/sign_in"

                print(username_values[cishu])
                print(password_values[cishu])
                # 设置Chrome的WebDriver
                driver = webdriver.Chrome()
                # 打开网址
                driver.get(website)

                # 显式等待，直到邮箱输入框可见
                email_input = WebDriverWait(driver, 10).until(
                    EC.visibility_of_element_located((By.ID, "user_email"))
                )

                # 在邮箱输入框中填入指定的邮箱地址
                email_input.send_keys(username_values[cishu])

                # 显式等待，直到密码输入框可见
                password_input = WebDriverWait(driver, 10).until(
                    EC.visibility_of_element_located((By.ID, "user_password"))
                )

                # 在密码输入框中填入指定的密码
                password_input.send_keys(password_values[cishu])

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

                # while True:
                #     try:
                        # 某些可能引发异常的操作
                        # print("这是一个死循环！")
                # 定位所有class为"text-right"的元素
                tr_elements = driver.find_elements(By.XPATH, "//td[@class='text-right']/ancestor::tr")
                # 确定是否还在当前页面
                if tr_elements == []:
                    print("不在日期页面，跳出死循环，重新启动浏览器。")
                    driver.quit()
                    # break
                for tr_element in tr_elements:
                    print("-------------------------------------------------------------------")
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

                        #获取月
                        matches_month = re.findall(pattern_months, tr_element.text)
                        month = month_translations[matches_month[0]]

                        # 获取日
                        matches_day = re.findall(pattern_two_digits, tr_element.text)
                        if matches_day == []:
                            matches_day = re.findall(pattern_one_digits, tr_element.text)
                        day = matches_day[0]

                        year = int(year)
                        month = int(month)
                        day = int(day)
                        # 将年、月、日变量组合成一个date对象
                        Now_data = date(year, month, day)
                        Now_data_str = Now_data.strftime("%Y-%m-%d")
                    if Now_data_str == old_data[city_english]:
                        print("日期未发生变化，当前日期为"+Now_data_str)

                    elif Now_data_str != old_data[city_english]:
                        print("日期发生变化！，当前日期为"+Now_data_str)

                        #发邮件通知，sender：发件人； receiver：收件人； password：授权码； title：标题； text_content：内容；
                        title = "【" + From_GuoJia + "|美国】" + city_chinese
                        lingqu = city_chinese
                        text_content = "【" + From_GuoJia + "|美国】" + city_chinese + "\n最早日期发生变化\n当前最早日期为："+Now_data_str+"\nIP:"+ip
                        # ——————————发件人———收件人————授权码————标题————内容——————————
                        # send_email("1316151698@qq.com","1316151698@qq.com", "xepktuqsdrtnjeaa", title, text_content)

                        old_data[city_english] = Now_data_str
                        #查看是否在需求范围内
                        input_dates = city_need_data[city_english]
                        date_string = generate_date_range_string(input_dates)
                        print(date_string)
                        is_in_need = Now_data_str in date_string
                        if is_in_need == True :
                            print("日期在需求范围内,当前日期为："+Now_data_str)
                            title = "【" + From_GuoJia + "|美国】" + city_chinese + "需求范围内"
                            text_content = "【" + From_GuoJia + "|美国】" + city_chinese + "\n最早日期在需求范围内，\n当前最早日期为：" + Now_data_str + "\n请立即进行登录预约。\nIP:"+ip
                            # ——————————发件人———收件人————授权码————标题————内容——————————
                            send_email("1316151698@qq.com", Mail_send2, "xepktuqsdrtnjeaa", title, text_content)

                            driver.save_screenshot("英国美签放号截图.png")

                            green_date = Now_data_str
                            # 1.保存green_data（可预约日期）  和  city_chinese （领区）
                            print(city_chinese+"监控到日期："+green_date+"进入表格查询客人是否需要。")
                            result = find_all_target_data_within_date(
                                r"C:\Users\Administrator\Desktop\境外美签客人.xlsx", city_chinese, green_date)
                            print(result)
                            green_people = len(result)
                            print("下面是获取的客人数量：↓")
                            print(green_people)
                            if green_people == 0:
                                print(Now_data_str+",无满足要求的客人")
                            elif green_people > 0:
                                threads = []
                                for i in range(green_people):
                                    print("客人信息")
                                    print(result[i][1])
                                    print(result[i][2])
                                    print(result[i][3])
                                    print(result[i][4])
                                    print(result[i][5])
                                    thread = threading.Thread(target=booking, args=(result[i][1], result[i][2], result[i][3], result[i][4], result[i][5]))
                                    threads.append(thread)
                                    thread.start()
                                    time.sleep(2)
                                print("等待线程运行结束")
                                time.sleep(120)

                print("当前最早日期集合：")
                print(old_data)
                time.sleep(10)
                cishu = cishu + 1
                driver.quit()
                # 要发送的数据
                data = {"ipAddr": ip, "task": From_GuoJia+"刷美签"}
                # 发送 POST 请求
                response = requests.post("http://54.169.239.115:8808/wuai/system/sys/saveServiceLog", json=data,timeout=60)
                print(response)
                time.sleep(2)
                    # except Exception as e:
                    #     print("发生错误：", e)
                    #     exc_type, exc_value, exc_traceback = sys.exc_info()
                    #     # 提取异常信息
                    #     traceback_details = traceback.extract_tb(exc_traceback)
                    #     # 获取错误发生的行号
                    #     line_number = traceback_details[-1].lineno
                    #     print(f"An error occurred on line: {line_number}")
                    #     time.sleep(5)
                    #     # 关闭浏览器
                    #     driver.quit()
                    #     break

    except Exception as e:
        print("发生了一个错误:", e)
        exc_type, exc_value, exc_traceback = sys.exc_info()
        # 提取异常信息
        traceback_details = traceback.extract_tb(exc_traceback)
        # 获取错误发生的行号
        line_number = traceback_details[-1].lineno
        print(f"An error occurred on line: {line_number}")
        # try:
        #     click_quickq.quickq()
        #     print("切换VPN成功")
        # except:
        #     print("切换VPN失败")
        # 关闭浏览器
        driver.quit()



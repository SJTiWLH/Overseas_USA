import smtplib
import threading
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import requests
from selenium.common import TimeoutException

ip = "39.98.220.155"
Tong = "1316151698@qq.com"
Hang = "2233852143@qq.com"
XiaoXin = "928781367@qq.com"
XiaoMi = "1951645633@qq.com"
Fanfan = "2194025327@qq.com"
Mail_send2 = [Tong,Hang,XiaoMi,Fanfan]
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

def booking(lingqu,username,password,date_range,xiugai,block_number):
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
    print(block_number)
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
        '圣地亚哥': 'Santiago',
        '巴西利亚': 'Brasilia',
        '里约热内卢': 'Rio de Janeiro',
        '圣保罗': 'Sao Paulo',
        '累西腓': 'Recife',
        '波尔图阿莱格里': 'Porto Alegre',
        '阿布扎比': 'Abu Dhabi',
        '迪拜': 'Dubai',
        '阿巴斯': 'La Paz',
        '巴黎': 'Paris'
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
    elif lingqu =="Dubai" or lingqu =="Abu Dhabi":
        website = "https://ais.usvisa-info.com/en-ae/niv/users/sign_in"
    elif lingqu =="Paris":
        website = "https://ais.usvisa-info.com/en-fr/niv/users/sign_in"
    elif lingqu == "Sao Paulo" or lingqu == "Brasilia" or lingqu == "Rio de Janeiro" or lingqu == "Recife" or lingqu == "Porto Alegre":
        website = "https://ais.usvisa-info.com/en-br/niv/users/sign_in"
    print(lingqu+"-"+username+"-"+password+"-"+date_range)
    print(website)
    thread_name = Chinese_lingqu+"-"+username+":"
    cyclic = 1
    while cyclic == 1:
        try:
            print("------------------------进程开始------------------------")
            # 设置Chrome的WebDriver
            driver = webdriver.Chrome()
            # 打开网址
            driver.get(website)
            # time.sleep(50000)
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

            # 选择第几位客人
            # 根据护照号选客人
            WebDriverWait(driver, 10).until(
                EC.presence_of_all_elements_located((By.CLASS_NAME, 'application'))
            )
            applications = driver.find_elements(By.CLASS_NAME, 'application')
            for app in applications:
                try:
                    WebDriverWait(app, 10).until(
                        EC.presence_of_element_located((By.XPATH, f".//td[contains(text(), {block_number})]"))
                    )
                    # 如果找到了元素，执行点击等操作
                    continue_button = app.find_element(By.XPATH, ".//a[contains(text(), 'Continue')]")
                    continue_button.click()
                    print("点击客人模块！")
                    break  # 如果找到元素并点击了，可能需要跳出循环
                except TimeoutException:
                    # 如果在当前app模块中没有找到元素，打印消息并继续下一个循环迭代
                    print("在当前模块中未找到指定的护照号。")
                    continue  # 继续检查下一个app模块

            # 根据第几位选客人
            # blocks = WebDriverWait(driver, 10).until(
            #     EC.presence_of_all_elements_located((By.CLASS_NAME, "application"))
            # )
            # # 检查板块号是否有效
            # if block_number < 1 or block_number > len(blocks):
            #     print('操作的客人超过数组数量！！！！')
            # # 定位指定板块
            # block = blocks[block_number - 1]
            # # 在选定的板块内查找按钮并点击
            # button = block.find_element(By.CSS_SELECTOR, '.button.primary.small')
            # button.click()
            # print("点击continiu成功，接下来进入预约。")

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

            elif xiugai == 1:
                # 修改预约点3
                driver.execute_script(
                    'document.getElementsByClassName("button small primary small-only-expanded")[3].click();')
            jiankong_cycle = 1
            while jiankong_cycle ==1:
                if (xiugai == 0) or (xiugai == 1):
                    time.sleep(2)
                    # 下拉框选择领区
                    select_element = driver.find_element(By.ID, "appointments_consulate_appointment_facility_id")
                    # 创建 Select 对象
                    select = Select(select_element)
                    # 根据文本选择 "London"
                    select.select_by_visible_text(lingqu)
                    time.sleep(5)

                    # 打开日历
                try:
                    input_element = WebDriverWait(driver, 10).until(
                        EC.element_to_be_clickable((By.CSS_SELECTOR, ".yatri_date input"))
                    )
                    input_element.click()
                except:
                    # 指定要查找的文本
                    print("未查找到日历框！！！")
                    text_to_check = 'There are no available appointments at the selected location. Please try again later.'
                    # 使用XPath来查找包含特定文本的元素，不限定任何特定的标签或类
                    elements = driver.find_elements(By.XPATH, f"//*[contains(text(), '{text_to_check}')]")
                    # 根据元素是否被找到来返回1或0
                    result = 1 if elements else 0
                    if result == 1:
                        print(result)
                        print("No available appointments at the selected")
                        driver.refresh()
                        continue
                    elif result == 0:
                        time.sleep(5)


                time.sleep(5)

                # 翻看日历
                try:
                    # 等待日历加载
                    driver.implicitly_wait(5)
                    # time.sleep(5000)

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
                        left_calendar = driver.find_element(By.CSS_SELECTOR,
                                                            ".ui-datepicker-group-first .ui-datepicker-title")
                        left_month, left_year = left_calendar.text.split()
                        left_month = datetime.datetime.strptime(left_month, "%B").month
                        left_year = int(left_year)

                        # 检查是否到达开始日期
                        if (left_year, left_month) >= start_date:
                            print(thread_name + "到达开始日期")
                            time.sleep(2)
                            break

                        # 点击向右翻页
                        next_button = driver.find_element(By.CSS_SELECTOR, ".ui-datepicker-next")
                        next_button.click()

                    yuyue_state = 0
                    chack_data_cycle = 1
                    while chack_data_cycle == 1:
                        # 获取右侧日历的年份和月份
                        right_calendar = driver.find_element(By.CSS_SELECTOR,
                                                             ".ui-datepicker-group-last .ui-datepicker-title")
                        right_month, right_year = right_calendar.text.split()
                        right_month = datetime.datetime.strptime(right_month, "%B").month
                        right_year = int(right_year)
                        # 获取两个日历的月份和年份
                        calendars = driver.find_elements(By.CSS_SELECTOR, ".ui-datepicker-group")
                        for calendar in calendars:
                            header = calendar.find_element(By.CSS_SELECTOR,
                                                           ".ui-datepicker-header .ui-datepicker-title")
                            month_year = header.text.split()
                            month = datetime.datetime.strptime(month_year[0], "%B").month
                            year = int(month_year[1])
                            print(f"{thread_name}日历月份: {month}, 日历年份: {year}")
                            # 获取可点击的日期
                            clickable_dates = calendar.find_elements(By.CSS_SELECTOR,
                                                                     "td:not(.ui-datepicker-unselectable) a")
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
                                    # title = "【" + Chinese_lingqu + "|美签】" + green_date
                                    # text_content = green_date + "在需求范围内,尝试点击预约.........." + "\nIP:" + ip
                                    # send_email("1316151698@qq.com", Mail_send2, "xepktuqsdrtnjeaa", title, text_content)
                                    # 发送微信信息（1：预约 ，2：监控）
                                    url = "http://api.visa5i.com/wuai/system/wechat-notification/save"
                                    data = {
                                        "apptTime": green_date,
                                        "consDist": Chinese_lingqu,
                                        "ipAddr": ip,
                                        "monCountry": "美国",
                                        "status": 2,
                                        "sys": "AIS",
                                        "remark": ""
                                    }
                                    response = requests.post(url, json=data, timeout=60000)
                                    if response.status_code == 200:
                                        print("微信发送信息成功")
                                    else:
                                        print(f"微信发送信息失败，状态码: {response.status_code}")
                                    try:
                                        print(thread_name + "点击日期！")
                                        date.click()
                                        print(thread_name + "点击成功！")
                                        # 选择时间
                                        print("选择时间！")
                                        times = None
                                        times_len = 1
                                        attempts = 0
                                        while attempts < 10 and (times is None or times_len==1) :
                                            try:
                                                times = driver.execute_script(
                                                    'return document.getElementsByName("appointments[consulate_appointment][time]")[0].innerText;')
                                                times_len = driver.execute_script(
                                                    'return document.getElementsByName("appointments[consulate_appointment][time]")[0].length;')
                                                if times:  # 如果times非空，跳出循环
                                                    break
                                            except Exception as e:
                                                print("尝试获取元素时出错：", e)
                                            print("时间未加载完毕，循环获取中.........")
                                            time.sleep(1)  # 等待1秒后再次尝试
                                            attempts += 1
                                        if (times is None)or (times_len==1):
                                            print("无可选时间,下拉框长度：")
                                            print(times_len)
                                            title = "【" + Chinese_lingqu + "|美签】无可选日期"
                                            text_content = "已无可选时间段，继续监控.........." + "\nIP:" + ip
                                            send_email("1316151698@qq.com", Mail_send2, "xepktuqsdrtnjeaa", title,
                                                       text_content)
                                            print("继续监控！！！")
                                            chack_data_cycle == 1
                                            break
                                        else:
                                            print("获取到的时间：", times)
                                        if times != None:
                                            driver.execute_script(
                                                'document.getElementsByName("appointments[consulate_appointment][time]")[0].selectedIndex = 1;')
                                            print("选择成功！")
                                        # 点击提交
                                        if lingqu == "Sao Paulo1":
                                            try:
                                                print("选择录指纹时间。")
                                                # driver.execute_script(" document.getElementById('appointments_asc_appointment_facility_id').click()")
                                                # driver.execute_script(" document.getElementById('appointments_asc_appointment_facility_id').value = '60'")
                                                WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "appointments_asc_appointment_facility_id"))).click()
                                                driver.find_element(By.XPATH,"//option[text()='Sao Paulo ASC Unidade Vila Mariana']").click()
                                                time.sleep(2)
                                                input_element = WebDriverWait(driver, 10).until(
                                                    EC.element_to_be_clickable(
                                                        (By.CSS_SELECTOR, ".yatri_date input required stringish"))
                                                )
                                                input_element.click()  # 点击打开日历
                                                for i in range(0,1):
                                                    # 开始查看日历
                                                    right_calendar = driver.find_element(By.CSS_SELECTOR,
                                                                                         ".ui-datepicker-group-last .ui-datepicker-title")
                                                    right_month, right_year = right_calendar.text.split()
                                                    right_month = datetime.datetime.strptime(right_month, "%B").month
                                                    right_year = int(right_year)
                                                    # 获取两个日历的月份和年份
                                                    calendars = driver.find_elements(By.CSS_SELECTOR, ".ui-datepicker-group")
                                                    for calendar in calendars:
                                                        header = calendar.find_element(By.CSS_SELECTOR,
                                                                                       ".ui-datepicker-header .ui-datepicker-title")
                                                        month_year = header.text.split()
                                                        month = datetime.datetime.strptime(month_year[0], "%B").month
                                                        year = int(month_year[1])
                                                        print(f"录指纹{thread_name}日历月份: {month}, 日历年份: {year}")
                                                        # 获取可点击的日期
                                                        clickable_dates = calendar.find_elements(By.CSS_SELECTOR,
                                                                                                 "td:not(.ui-datepicker-unselectable) a")
                                                        for date in clickable_dates:
                                                            print(f"{thread_name}可点击的录指纹日期: {date.text}")
                                                            year = int(year)
                                                            month = int(month)
                                                            day = int(date.text)
                                                            green_date = "{:04d}-{:02d}-{:02d}".format(year, month, day)
                                                            print(green_date)
                                                            # 判断是否在日期内
                                                            Lstring_data = "2024-12-10,2024-12-11,2024-12-12,2024-12-13,2024-12-14,2025-01-10,2025-01-11,2025-01-12,2025-01-13,2025-01-14,2025-01-15,2025-01-16,2025-01-17,2025-01-18,2025-01-19,2025-01-20,2025-01-21,2025-01-22,2025-01-23,2025-01-24,2025-01-25"
                                                            if green_date in Lstring_data:
                                                                print(green_date + "在需求范围内")
                                                                print(thread_name + "点击日期！")
                                                                date.click()
                                                                print(thread_name + "点击成功！")
                                                                # 选择时间
                                                                print("选择时间！")
                                                            time.sleep(5000)
                                                    # 查看是否超过预约日期还么有录指纹日期
                                                    # 翻页
                                                    next_button = driver.find_element(By.CSS_SELECTOR,".ui-datepicker-next")
                                                    next_button.click()
                                            except:
                                                print("选择录指纹日期异常，请手动操作。")
                                                time.sleep(5000)
                                            time.sleep(5000)
                                        # 定位到按钮元素
                                        submit_button = driver.find_element(By.ID, "appointments_submit")
                                        # submit_button.click()
                                        if xiugai == "1":
                                            # 修改预约，点击确定
                                            a = 1


                                        yuyue_state = 1
                                        if yuyue_state == 1:
                                            print(thread_name + "预约成功。")
                                            print("------------------------进程预约成功------------------------")
                                            url = "http://api.visa5i.com/wuai/system/wechat-notification/save"
                                            data = {
                                                "apptTime": green_date,
                                                "consDist": Chinese_lingqu,
                                                "ipAddr": ip,
                                                "monCountry": "美国",
                                                "status": 1,
                                                "sys": "AIS",
                                                "remark": "检测到需求内日期！录指纹日期选择开发未完善，请立即登陆服务器进行操作。"
                                            }
                                            response = requests.post(url, json=data, timeout=60000)
                                            if response.status_code == 200:
                                                print("微信发送信息成功")
                                            else:
                                                print(f"微信发送信息失败，状态码: {response.status_code}")
                                            title = "【" + Chinese_lingqu + "|美签】" + green_date
                                            text_content = thread_name + green_date + "\n预约成功！请立即登陆服务器确认。\nIP:" + ip
                                            send_email("1316151698@qq.com", Mail_send2, "xepktuqsdrtnjeaa", title,
                                                       text_content)
                                            time.sleep(50000)
                                            print("跳出循环")
                                            cyclic = 0
                                            break

                                    except:
                                        print("点击提交异常，预约日期已空！")
                                        title = "【" + Chinese_lingqu + "|美签】点击提交异常"
                                        text_content = "点击提交异常，预约日期已空！继续监控..........." + "\nIP:" + ip
                                        send_email("1316151698@qq.com", Mail_send2, "xepktuqsdrtnjeaa", title,
                                                   text_content)

                        if (right_year, right_month) > end_date:
                            print(thread_name + "到达截止日期，未发现可预约日期")

                            print("没有日期，继续监控。")
                            jiankong_cycle = 1  # 继续监控就令jiankong_cycle = 1，没日期就结束，就令jiankong_cycle = 0
                            driver.refresh()
                            # jiankong_cycle = 0   # 继续监控就令jiankong_cycle = 1，没日期就结束，就令jiankong_cycle = 0
                            # cyclic = 0
                            # driver.quit()
                            break
                        # 点击向右翻页
                        next_button = driver.find_element(By.CSS_SELECTOR, ".ui-datepicker-next")
                        next_button.click()

                except Exception as e:
                    print(thread_name + "线程异常1")
                    traceback.print_exc()
                    print("------------------------线程异常------------------------")
                    time.sleep(50000)
                    driver.quit()

        except Exception as e:
            print(thread_name + "线程异常2")
            print("------------------------线程异常------------------------")
            traceback.print_exc()
            time.sleep(5)
            driver.quit()
            # break



city1 = '圣保罗'
username1 = '374010248@qq.com'
password1 = 'lee253515'
data1 = '2024.12.10-2024.12.15'
# data1 = '2024.12.10-2025.01.30'
xiugai1 = '0'
block_number1 = "EC3970995"   # 操作第几位客人


threads = []
thread1 = threading.Thread(target=booking, args=(city1, username1, password1, data1, xiugai1, block_number1))
thread1.start()
# thread2 = threading.Thread(target=booking, args=(city2, username2, password2, data2, xiugai2, block_number2))
# thread2.start()
# thread3 = threading.Thread(target=booking, args=(city3, username3, password3, data3, xiugai3, block_number3))
# thread3.start()


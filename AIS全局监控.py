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
import pandas as pd
import lackey
import pywinauto
import click_quickq

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
    'Paris':'巴黎',
    'Bridgetown':'布里奇顿'

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
    'Paris':'No Appointments Available',
    'Bridgetown':'No Appointments Available'
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

# 添加新的城市与领区说明：
# 1，old_data中添加判断日期发生变化的初始化信息。
# 2,city_translations中添加将城市名翻译成中文的字典信息。
# 3，pattern_city中天花正则表达匹配城市。
# 4，添加登陆的网址 website

# 正则表达式匹配文段中的城市
pattern_city = r"London|Belfast|Ottawa|Toronto|Vancouver|Calgary|Halifax|Montreal|Quebec City|Buenos Aires|Santiago|Brasilia|Rio de Janeiro|Sao Paulo|Recife|Porto Alegre|Abu Dhabi|Dubai|La Paz|Paris|Bridgetown"
# 正则表达式匹配文段中的月份
pattern_months = r"\b(?:January|February|March|April|May|June|July|August|September|October|November|December)\b"
# 正则表达式匹配四位数字
pattern_four_digits = r"\b\d{4}\b"
# 正则表达式匹配二位数字
pattern_two_digits = r"\b\d{2}\b"
# 正则表达式匹配一位数字
pattern_one_digits = r"\b\d{1}\b"
# 更换quickq

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
XiaoYi = "382308885@qq.com"
XiaoXin = "928781367@qq.com"
XiaoMi = "1951645633@qq.com"
XiaoMai = "540727185@qq.com"
Fanfan = "2194025327@qq.com"
Mail_send1 = [Tong,XiaoMi,Shen,XiaoXin] # Mail_send1发送范围内的日期。
Mail_send2 = [Tong,XiaoMi,Shen] # Mail_send2发送发生变化的日期。
ip = '39.98.88.235'
task = "境外刷美签"
nameid = 0

# 将Excel文件路径替换成你的文件路径
file_path = r'C:\Users\Administrator\Desktop\境外美签监控.xlsx'
df = pd.read_excel(file_path)
city_need_data = pd.Series(df['监控范围/日期'].values, index=df['监控范围/领区']).to_dict()
All_Jankong_df = df[df['监控类型'] == 2]
print(All_Jankong_df)
username_values = All_Jankong_df['账号'].tolist()
print(username_values)
password_values = All_Jankong_df['密码'].tolist()
print(password_values)
country_values = All_Jankong_df['国家'].tolist()
print(country_values)
print(len(username_values))

cishu = 0

while True:
    try:
                all_Num = len(username_values)-1
                if cishu > all_Num:
                    cishu = 0
                print(cishu)
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

                elif From_GuoJia == "巴巴多斯":
                    website = 'https://ais.usvisa-info.com/en-bb/niv/users/sign_in'

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



                # time.sleep(5000)
                # while True:
                #     try:
                # 某些可能引发异常的操作
                # print("这是一个死循环！")
                # 定位所有class为"text-right"的元素
                tr_elements = driver.find_elements(By.XPATH, "//td[@class='text-right']/ancestor::tr")
                # 确定是否还在当前页面
                if tr_elements == []:
                    print("不在日期页面，重新启动浏览器。")
                    driver.quit()

                for tr_element in tr_elements:
                    print("---------------------------------------------")
                    print("城市与日期："+tr_element.text)

                    # 匹配城市
                    matches_city = re.findall(pattern_city, tr_element.text)
                    city_english = matches_city[0]
                    # print(city_english)

                    # 将英文地名翻译为中文
                    city_chinese = city_translations[city_english]
                    print(city_chinese)

                    #检查是否可查看日期
                    contains_No = "No Appointments Available" in tr_element.text
                    # print(contains_No)

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

                        text_content = "【" + From_GuoJia + "|美国】" + city_chinese + "\n最早日期发生变化\n当前最早日期为："+Now_data_str+"\nIP:"+ip

                        # ——————————发件人———收件人————授权码————标题————内容——————————
                        send_email("1951645633@qq.com", Mail_send2, "hdoywzgrgaomdafe", title, text_content)

                        old_data[city_english] = Now_data_str

                        #查看是否在需求范围内
                        input_dates = city_need_data[city_english]
                        date_string = generate_date_range_string(input_dates)
                        print(date_string)
                        is_in_need = Now_data_str in date_string
                        if is_in_need == True :
                            print("日期在需求范围内")
                            # ——————————发件人———收件人————授权码————标题————内容——————————
                            text_content = "【" + From_GuoJia + "|美国】" + city_chinese + "\n最早日期在需求范围内，\n当前最早日期为：" + Now_data_str + "\n请立即进行登录预约。\nIP:"+ip
                            send_email("1951645633@qq.com", Mail_send1, "hdoywzgrgaomdafe", title, text_content)
                            url = "http://54.169.239.115:8808/visa/saveApptMonitor"
                            json_data = {
                                "apptTime": Now_data_str,
                                "consDist": From_GuoJia,
                                "apptType": city_chinese,
                                "ipAddr": ip,
                                "monCountry": '美国',
                                "status": '2',
                                "sys": 'AIS',
                                "userName": 'jiankong@163.com',
                                "passWord": '12345'
                            }
                            response = requests.post(url, json=json_data)
                            print(response)
                # print("当前最早日期集合：")
                # print(old_data)
                # driver.refresh()
                time.sleep(60)
                cishu = cishu + 1
                driver.quit()

                # break
                # 要发送的数据
                data = {"ipAddr": ip, "task": task}
                # 发送 POST 请求
                response = requests.post("http://54.169.239.115:8808/wuai/system/sys/saveServiceLog", json=data,timeout=60)
                print(response)
                time.sleep(2)

    except Exception as e:
        print("发生了一个错误:", e)
        exc_type, exc_value, exc_traceback = sys.exc_info()
        # 提取异常信息
        traceback_details = traceback.extract_tb(exc_traceback)
        # 获取错误发生的行号
        line_number = traceback_details[-1].lineno
        print(f"An error occurred on line: {line_number}")
        traceback.print_exc()
        try:
            click_quickq.quickq()
            print("切换VPN成功")
        except:
            print("切换VPN失败")
        # 关闭浏览器
        driver.quit()



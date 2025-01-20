import re
import time
from datetime import date, datetime
from telnetlib import EC

import pandas as pd
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.wait import WebDriverWait

from src.services.Tool import Tool
from src.utils.logger import setup_logger
from src.config import AppConfig
from src.services.get_excel import getExcel
logger = setup_logger(__name__)


class WatchData:
    def __init__(self,browser,from_contry):
        self.pattern_city = r"London|Belfast|Ottawa|Toronto|Vancouver|Calgary|Halifax|Montreal|Quebec City|Buenos Aires|Santiago|Brasilia|Rio de Janeiro|Sao Paulo|Recife|Porto Alegre|Abu Dhabi|Dubai|La Paz|Paris|Bridgetown|Dublin|Ciudad Juarez|Guadalajara|Hermosillo|Matamoros|Merida|Mexico City|Monterrey|Nogales|Nuevo Laredo|Tijuana"
        self.pattern_months = r"\b(?:January|February|March|April|May|June|July|August|September|October|November|December)\b"
        self.city_translations = {
            'Ottawa': '渥太华',
            'Toronto': '多伦多',
            'Vancouver': '温哥华',
            'Calgary': '卡尔加里',
            'Halifax': '哈利法克斯',
            'Montreal': '蒙特利尔',
            'Quebec City': '魁北克城',
            'London': '伦敦',
            'Belfast': '贝尔法斯特',
            'Buenos Aires': '布宜诺斯艾利斯',
            'Santiago': '圣地亚哥',
            'Brasilia': '巴西利亚',
            'Rio de Janeiro': '里约热内卢',
            'Sao Paulo': '圣保罗',
            'Recife': '累西腓',
            'Porto Alegre': '波尔图阿莱格里',
            'Abu Dhabi': '阿布扎比',
            'Dubai': '迪拜',
            'La Paz': '阿巴斯',
            'Paris': '巴黎',
            'Bridgetown': '布里奇顿',
            'Dublin': '都柏林',
            "Ciudad Juarez": "华雷斯城",
            "Guadalajara": "瓜达拉哈拉",
            "Hermosillo": "埃莫西约",
            "Matamoros": "马塔莫罗斯",
            "Merida": "梅里达",
            "Mexico City": "墨西哥城",
            "Monterrey": "蒙特雷",
            "Nogales": "诺加莱斯",
            "Nuevo Laredo": "新拉雷多",
            "Tijuana": "蒂华纳"
        }
        self.city_translations_c_to_e = {v: k for k, v in self.city_translations.items()}
        self.month_translations = {
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
        self.pattern_four_digits = r"\b\d{4}\b" # 正则表达式匹配四位,两位,一位数字
        self.pattern_two_digits = r"\b\d{2}\b"
        self.pattern_one_digits = r"\b\d{1}\b"
        self.browser = browser
        self.from_contry = from_contry
        self.tool = Tool()
        self.jiankong_excelPath = AppConfig.jiankong_excelPath
        self.getExcel = getExcel()
        self.city_need_data = self.getExcel.get_Jiankong_data_for_Excel()
        self.allPeople = self.getExcel.get_yuyue_data_for_Excel()

    def not_pay_getData(self):
        # 获取所有日期
        tr_elements = self.browser.driver.find_elements(By.XPATH, "//td[@class='text-right']/ancestor::tr")
        if tr_elements == []:
            print("不在日期页面，重新启动浏览器。")
            self.browser.driver.quit()
        green_people_arr = [] # 遍历每个城市的日期，拿到日期去客人表格对比，符合条件的放入该数组。遍历完所有城市，拿到所有满足条件的客人
        print("------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------")
        for tr_element in tr_elements:
            print("------------------------------------------------------------------------------------------")
            logger.info(f"城市与日期：{tr_element.text}")
            # 匹配城市英文名 获得领区中文名称，和显示日期，和当前城市需要的日期
            city_chinese,Now_data_str,Jiankong_data_Str= self.not_pay_processData(tr_element.text)
            logger.info(f"{self.from_contry}-{city_chinese}—监控到最早日期:{Now_data_str}")
            if Now_data_str in Jiankong_data_Str:
                self.tool.send_Jiankong_Wechat(city_chinese,self.from_contry,Now_data_str)
                logger.info("最早日期在监控范围内，发送微信通知")
                # 拿到最早日期，去查找是否有符合条件的客人
                green_people = self.find_people(city_chinese,Now_data_str)
                green_people_arr.extend(green_people)
        print("------------------------------------------------------------------------------------------")
        print("------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------")
        return green_people_arr
    def find_people(self,city_chinese,Now_data_str):
        # 拿监控的城市和监控到的日期，查看时候是需要预约的人，在范围内就返回该客人的全部信息，和总共有多少客人
        result = []
        for persion in self.allPeople:
            if persion["领区"] == city_chinese and persion["是否预约"] == 1:
                need_Time = persion["预约时间"]
                need_data = self.tool.generate_date_range_string(need_Time)
                if Now_data_str in need_data:
                    result.append(persion)
        return result
    def not_pay_processData(self, data):
        # 处理获取到的数据（页面右侧领区和最早日期 例如： London January 01 ）
        # 返回 城市中文名、显示的日期（如果没卡槽返回noslot提示）、在表中获取到的监控日期Str

        # 匹配数据中的城市英文名
        matches_city = re.findall(self.pattern_city, data)
        city_english = matches_city[0]
        # 使用英文名，获取该城市的监控需求日期
        Jiankong_data = self.city_need_data[city_english]
        Jiankong_data_Str = self.tool.generate_date_range_string(Jiankong_data)
        # 获取城市中文名
        city_chinese = self.city_translations[city_english]
        logger.info(f"{city_chinese}—监控范围：{Jiankong_data}")

        # 检查是否有卡槽
        contains_No = "No Appointments Available" in data

        if contains_No:
            # 该城市没有卡槽。
            # logger.info(f"{city_chinese}：No Appointments Available")
            return city_chinese, "No Appointments Available", Jiankong_data_Str
        else:
            # 获取年月日

            # 获取年
            matches_year = re.findall(self.pattern_four_digits, data)
            year = matches_year[0]
            year = int(year)
            # 获取月
            matches_month = re.findall(self.pattern_months, data)
            month = self.month_translations[matches_month[0]]
            month = int(month)
            # 获取日
            matches_day = re.findall(self.pattern_two_digits, data)
            if matches_day == []:
                matches_day = re.findall(self.pattern_one_digits, data)
            day = matches_day[0]
            day = int(day)

            # 将年、月、日变量组合成一个date对象
            Now_data = date(year, month, day)
            Now_data_str = Now_data.strftime("%Y-%m-%d")
            return city_chinese, Now_data_str, Jiankong_data_Str


    def pay_getData(self,lingqu,eTime):
        # 使用付费的账号进行监控和预约
        lingqu_e = self.city_translations_c_to_e.get(lingqu)  # 获取英文名一会要进行选择
        print(lingqu_e)
        self.pay_selectLingqu(lingqu_e)  # 选择领区
        self.open_data_table()  # 打开日历
        self.read_dada_table(eTime)
    def pay_selectLingqu(self,lingqu_e):
        # 下拉框选择领区
        select_element = self.browser.driver.find_element(By.ID, "appointments_consulate_appointment_facility_id")
        # 创建 Select 对象
        select = Select(select_element)
        # 根据文本选择 "London"
        select.select_by_visible_text(lingqu_e)
        time.sleep(5)
    def open_data_table(self):
        # 点击打开日历
        time.sleep(5)
        error_num = 0
        while True:
            try:
                self.browser.driver.execute_script("document.getElementsByClassName('label')[1].click()")
                break
            except:
                error_num += 1
                if error_num == 5:
                    break
    def read_dada_table(self,eTime):
        # 翻看日历
        # 等待日历加载
        self.browser.driver.implicitly_wait(5)
        time.sleep(5)

        string_data = self.tool.generate_date_range_string(eTime)
        print(string_data)
        # 将日期范围分割成开始日期和结束日期
        start_date_str, end_date_str = self.data_start_end(eTime)
        print(start_date_str, end_date_str)
        # 从每个日期中提取年和月
        start_year, start_month = map(int, start_date_str.split('.')[:2])
        end_year, end_month = map(int, end_date_str.split('.')[:2])

        start_date = (start_year, start_month)
        end_date = (end_year, end_month)

        while True:
            # 获取左侧日历的年份和月份
            left_calendar = self.browser.driver.find_element(By.CSS_SELECTOR,".ui-datepicker-group-first .ui-datepicker-title")
            left_month, left_year = left_calendar.text.split()
            print(left_month, left_year)
            left_month = datetime.datetime.strptime(left_month, "%B").month
            left_year = int(left_year)

            # 检查是否到达开始日期
            if (left_year, left_month) >= start_date:
                print("到达开始日期")
                time.sleep(2)
                break

            # 点击向右翻页
            next_button = self.browser.driver.find_element(By.CSS_SELECTOR, ".ui-datepicker-next")
            next_button.click()
        # 获取右侧日历的年份和月份
        right_calendar = self.browser.driver.find_element(By.CSS_SELECTOR,".ui-datepicker-group-last .ui-datepicker-title")
        right_month, right_year = right_calendar.text.split()
        right_month = datetime.datetime.strptime(right_month, "%B").month
        right_year = int(right_year)
        # 获取两个日历的月份和年份
        calendars = self.browser.driver.find_elements(By.CSS_SELECTOR, ".ui-datepicker-group")
        for calendar in calendars:
            header = calendar.find_element(By.CSS_SELECTOR,
                                           ".ui-datepicker-header .ui-datepicker-title")
            month_year = header.text.split()
            month = datetime.datetime.strptime(month_year[0], "%B").month
            year = int(month_year[1])
            print(f"日历月份: {month}, 日历年份: {year}")
            # 获取可点击的日期
            clickable_dates = calendar.find_elements(By.CSS_SELECTOR,"td:not(.ui-datepicker-unselectable) a")
            for date in clickable_dates:
                print(f"可点击的日期: {date.text}")
                year = int(year)
                month = int(month)
                day = int(date.text)
                green_date = "{:04d}-{:02d}-{:02d}".format(year, month, day)
                print(green_date)
                # 判断是否在日期内
                if green_date in string_data:
                    print(green_date + "在需求范围内")
                    # 发送微信通知
                    try:
                        print( "点击日期！")
                        date.click()
                        print("点击成功！")
                        # 选择时间
                        print("选择时间！")
                        times = None
                        times_len = 1
                        attempts = 0
                        while attempts < 10 and (times is None or times_len == 1):
                            try:
                                times = self.browser.driver.execute_script(
                                    'return document.getElementsByName("appointments[consulate_appointment][time]")[0].innerText;')
                                times_len = self.browser.driver.execute_script(
                                    'return document.getElementsByName("appointments[consulate_appointment][time]")[0].length;')
                                if times:  # 如果times非空，跳出循环
                                    break
                            except Exception as e:
                                print("尝试获取元素时出错：", e)
                            print("时间未加载完毕，循环获取中.........")
                            time.sleep(1)  # 等待1秒后再次尝试
                            attempts += 1
                        if (times is None) or (times_len == 1):
                            print("无可选时间,下拉框长度：")
                            print(times_len)
                            # 无可选时间段,继续监控
                            print("继续监控！！！")
                            break
                        else:
                            print("获取到的时间：", times)
                        if times != None:
                            self.browser.driver.execute_script(
                                'document.getElementsByName("appointments[consulate_appointment][time]")[0].selectedIndex = 1;')
                            print("选择成功！")
                        # 点击提交
                        # 定位到按钮元素
                        submit_button = self.browser.driver.find_element(By.ID, "appointments_submit")
                        # submit_button.click()

                        yuyue_state = 1
                        if yuyue_state == 1:
                            print( "预约成功。")
                            # 发送微信信息
                            time.sleep(50000)
                            print("跳出循环")
                            cyclic = 0
                            break

                    except:
                        print("点击提交异常，预约日期已空！")


        if (right_year, right_month) > end_date:
            print("到达截止日期，未发现可预约日期")

            print("没有日期，继续监控。")


    def data_start_end(self,date_range):
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






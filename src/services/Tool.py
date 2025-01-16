
import time
from datetime import datetime, timedelta,timezone

import lackey
import pywinauto
import requests
# from datetime import datetime, timedelta
from src.config import AppConfig

class Tool:
    def __init__(self):
        self.ip = AppConfig.ip
    def generate_date_range_string(self,input_dates):

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

    def send_Jiankong_Wechat(self,lingqu,from_contry,greentime):
        url = "http://api.visa5i.com/wuai/system/wechat-notification/save"
        json_data = {
            "apptTime": greentime,
            "consDist": from_contry,
            "apptType": lingqu,
            "ipAddr": self.ip,
            "monCountry": '美国',
            "status": '2',
            "sys": 'AIS',
            "remark": ""
        }
        response = requests.post(url, json=json_data)
        return response

    def send_Yuyue_Wechat(self,lingqu,guojia,greentime):
        url = "http://api.visa5i.com/wuai/system/wechat-notification/save"
        json_data = {
            "apptTime": greentime,
            "consDist": guojia,
            "apptType": lingqu,
            "ipAddr": self.ip,
            "monCountry": '美国',
            "status": '1',
            "sys": 'AIS',
            "remark": "预约提交成功，请登录服务器检查，是否预约成功。"
        }
        response = requests.post(url, json=json_data)
        return response

    def quickq(self):

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
            click_time = time.time()
            number_two = 1

        if number_two == 0:
            target_image = 'C:/Slot/UK/Other/img/quickq1.png'
            if lackey.exists(target_image):
                lackey.click(target_image)
                click_time = time.time()
            else:
                print(f"未找到图像: {target_image}")

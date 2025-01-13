import requests
from datetime import datetime, timedelta
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

    def send_Jiankong_Wechat(self,lingqu,guojia,greentime):
        url = "http://api.visa5i.com/wuai/system/wechat-notification/save"
        json_data = {
            "apptTime": greentime,
            "consDist": guojia,
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

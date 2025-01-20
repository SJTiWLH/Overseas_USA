import os
from datetime import date
import time
import pandas as pd


# def generate_date_range_string(input_dates):
#     from datetime import datetime, timedelta
#
#     # 分割字符串以获取各个时间段
#     date_ranges = input_dates.split(';')
#
#     # 分别处理每个时间段
#     all_dates = []
#     for date_range in date_ranges:
#         start_date_str, end_date_str = date_range.split('-')
#
#         # 将字符串日期转换为datetime对象
#         start_date = datetime.strptime(start_date_str, "%Y.%m.%d")
#         end_date = datetime.strptime(end_date_str, "%Y.%m.%d")
#
#         # 生成日期范围内的所有日期
#         current_date = start_date
#         while current_date <= end_date:
#             all_dates.append(current_date.strftime("%Y-%m-%d"))
#             current_date += timedelta(days=1)
#
#     # 将所有日期列表转换为字符串
#     return ','.join(all_dates)
# eTime = "2024.8.09-2024.8.20"
# need_data = generate_date_range_string(eTime)
# year = 2024
# month = 8
# day = 10
# # 将年、月、日变量组合成一个date对象
# Now_data = date(year, month, day)
# Now_data_str = Now_data.strftime("%Y-%m-%d")
# if Now_data_str in need_data:
#     print(need_data)

# jiankong_excelPath = '../境外美签监控.xlsx'
# absolute_path = os.path.abspath(jiankong_excelPath)
# print(absolute_path)
# green_people_arr = "123456789"
# green_people = [{'序号': 1, '领区': '巴黎'},{'序号': 2, '领区': '巴黎'}]
# # green_people_arr.append(green_people)
# print(green_people_arr)
# print(len(green_people_arr))
# if green_people_arr == []:
#     print("没东西")
# elif green_people_arr != []:
#     print("有东西")
# class test:
#     def getURL(self,guojia=None,lingqu=None):
#         if guojia=="英国" or lingqu == "伦敦":
#             url = "123"
#             return url
#         else:
#             return "没有找到对应国家的网站"
# test=test()
# a = test.getURL(None,"伦敦")
# print(a)
# e = ["1","2"]
# a = ["     123", "   456", "   789"]
# d = [a,e]
# print(d(a))
# d[a] = [c.strip() for c in d ]
# print(d[a])
# time.sleep(500)
# result = {
#     "JAN. 15": {
#         "normal_times": ['\n                            09:00\n                        ', '\n                            09:30\n                        ', '\n                            10:00\n                        ', '\n                            10:30\n                        ', '\n                            11:00\n                        ', '\n                            11:30\n                        ', '\n                            12:00\n                        ', '\n                            12:30\n                        ', '\n                            13:00\n                        ', '\n                            13:30\n                        ', '\n                            14:00\n                        ', '\n                            14:30\n                        ', '\n                            15:00\n                        '],
#         "prime_times": ['\n                            07:30\n                        ', '\n                            08:00\n                        ', '\n                            10:30\n                        ', '\n                            12:30\n                        ', '\n                            13:30\n                        ', '\n                            14:00\n                        ']
#     }
# }
#
# for date, time_dict in result.items():
#     print(f"日期: {date}")
#     # 使用列表推导式和 strip 方法处理普通时间列表元素，并更新原字典
#     time_dict['normal_times'] = [time.strip() for time in time_dict['normal_times']]
#     print(f"  普通时间: {time_dict['normal_times']}")
#     # 使用列表推导式和 strip 方法处理黄金时间列表元素，并更新原字典
#     time_dict['prime_times'] = [time.strip() for time in time_dict['prime_times']]
#     print(f"  黄金时间: {time_dict['prime_times']}")


class a:
    def __init__(self):
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

    def b(self):
        c = self.city_translations_c_to_e.get("渥太华")
        print(c)
A = a()
A.b()

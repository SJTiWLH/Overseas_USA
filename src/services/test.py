import os
from datetime import date

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
class test:
    def getURL(self,guojia=None,lingqu=None):
        if guojia=="英国" or lingqu == "伦敦":
            url = "123"
            return url
        else:
            return "没有找到对应国家的网站"
test=test()
a = test.getURL(None,"伦敦")
print(a)

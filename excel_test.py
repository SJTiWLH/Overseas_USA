# import pandas as pd
# # 将Excel文件路径替换成你的文件路径
# file_path = r'C:\Users\Administrator\Desktop\境外美签监控.xlsx'
# df = pd.read_excel(file_path)
# All_Jankong_df = df[df['监控类型'] == 2]
# print(All_Jankong_df)
# username_values = All_Jankong_df['账号'].tolist()
# print(username_values)
# password_values = All_Jankong_df['密码'].tolist()
# print(password_values)
# country_values = All_Jankong_df['国家'].tolist()
# print(country_values)
#
# len(username_values)
import openpyxl
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
city_chinese = '伦敦'
green_date = '2024-4-22'
result = find_all_target_data_within_date(
                                r"C:\Users\Administrator\Desktop\境外美签客人.xlsx", city_chinese, green_date)
print(result)

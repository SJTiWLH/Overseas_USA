#             保存这个green_data
#             确定登陆的账号密码和网站。
#             (如何确定呢？？？)
#                1.保存green_data（可预约日期）  和  city_chinese （领区）
#                2.开始读表，先确定领区，在确定是否预约，再判断是否满足要求。
#                3.先从表中找到该领区，然后确定预约值为:1,返回满足要求的值。没有的话就返回没有满足要求的客人
#                4.根据这些信息，写个循环，获取这些信息中的日期的起止日期，使用方法将其转化为字符串，并查找green_data是否包含其中，包含的将账号密码存入。
#                5.获取它的长度。来建立线程，
#              启动预约线程，（线程名，变量：账号，密码）



import openpyxl
from datetime import datetime


def find_all_target_data_within_date(file_name, target_value, given_date):
    # 加载 Excel 文件
    workbook = openpyxl.load_workbook(file_name)
    sheet = workbook.active

    # 将给定的日期字符串转换为 datetime 对象
    given_date = datetime.strptime(given_date, "%Y-%m-%d")

    # 用于存储找到的符合条件的所有行数据
    matching_rows = []

    # 遍历 B 列的所有单元格
    for row in range(1, sheet.max_row + 1):
        cell_value = sheet[f"B{row}"].value
        if cell_value is None:
            # 如果遇到空单元格，停止读取
            break
        if cell_value == target_value and sheet[f"G{row}"].value == "1":
            # 获取 E 列的时间范围
            date_range = sheet[f"E{row}"].value
            start_date, end_date = [datetime.strptime(date.strip(), "%Y.%m.%d") for date in date_range.split('-')]
            # 检查给定的日期是否在时间范围内
            if start_date <= given_date <= end_date:
                # 找到符合条件的数据，获取整行数据并添加到列表中
                matching_rows.append([cell.value for cell in sheet[row]])

    return matching_rows if matching_rows else "没有满足要求的客人。"


# 使用示例
Green_date = "2024-4-1"
result = find_all_target_data_within_date(r"C:\Users\Administrator\Desktop\境外美签客人.xlsx", "多伦多", Green_date)
print(result)
green_people = len(result)
for i in range(green_people):
    print(result[i][1])
    print(result[i][2])
    print(result[i][3])
    print(result[i][4])
    print(result[i][5])
print(green_people)



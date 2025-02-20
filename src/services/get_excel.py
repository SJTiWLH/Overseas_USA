import pandas as pd
from src.services.Tool import Tool

class getExcel:
    def get_Jiankong_data_for_Excel(self):
        # 获取各个领区的监控需求日期
        self.file_path = r"C:\Slot\UK\Overseas_USA\境外美签监控.xlsx"
        self.df = pd.read_excel(self.file_path)
        self.city_need_data = pd.Series(self.df['监控范围/日期'].values, index=self.df['监控范围/领区']).to_dict()
        return self.city_need_data
    def get_yuyue_data_for_Excel(self):
        self.file_path = r"C:\Slot\UK\Overseas_USA\境外美签客人.xlsx"
        self.df = pd.read_excel(self.file_path)
        # print(self.df)
        rows = []
        # 遍历 DataFrame 中的每一行
        for index, row in self.df.iterrows():
            # 将行数据存储在字典中，其中键是列名，值是该行对应列的值
            row_dict = dict(row)
            rows.append(row_dict)
        return rows


    def username_jiankong(self):
        file_path = r'C:\Slot\UK\Overseas_USA\境外美签监控.xlsx'
        df = pd.read_excel(file_path)
        self.All_Jankong_df = df[df['监控类型'] == 2]
        # print(All_Jankong_df)
        rows = []
        # 遍历 DataFrame 中的每一行
        for index, row in self.All_Jankong_df.iterrows():
            # 将行数据存储在字典中，其中键是列名，值是该行对应列的值
            row_dict = dict(row)
            rows.append(row_dict)
        return rows

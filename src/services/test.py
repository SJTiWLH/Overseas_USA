import os
from datetime import date
import time
import pandas as pd
from src.services.Tool import Tool
# class tool:
#     def send_Jiankong_Wechat(self, lingqu, from_contry, greentime, remark=None):
#         print(lingqu)
#         print(from_contry)
#         print(greentime)
#         print(remark)

tool = Tool()
tool.send_Jiankong_Wechat("测试","测试英国","2024-01-01","测试备注")


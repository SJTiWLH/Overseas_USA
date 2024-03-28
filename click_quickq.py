import pywinauto
import lackey
import time
from datetime import datetime

# 初始时间戳设置为None
last_timestamp = None

def quickq ():


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



# 获取当前时间戳
timestamp = time.time()


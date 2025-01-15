import logging

from src.utils.logger import setup_logger

logger = setup_logger(__name__)

class Book:
    def __init__(self,green_people_arr):
        self.green_people_arr = green_people_arr

    def Book_App(self):
        if len(self.green_people_arr) == 0:
            logger.info(f"无满足条件客人，退出预约操作。继续监控")
            return
        logger.info(f"开始预约操作")
        print(self.green_people_arr)



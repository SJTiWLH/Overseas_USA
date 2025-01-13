import os


class AppConfig:
    """应用配置"""

    # ip
    ip = '127.0.0.1'
    # 目标URL
    TARGET_URL = "https://ais.usvisa-info.com/en-ca/niv/users/sign_in"
    jiankong_relative_excelPath = '../境外美签监控.xlsx'
    jiankong_excelPath = os.path.abspath(jiankong_relative_excelPath)
    print(jiankong_excelPath)
    yuyue_relative_excelPath = '../境外美签客人.xlsx'
    yuyue_excelPath = os.path.abspath(yuyue_relative_excelPath)

    # 日志配置
    LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    LOG_LEVEL = "INFO"
    LOG_FILE = "consul_booking.log"


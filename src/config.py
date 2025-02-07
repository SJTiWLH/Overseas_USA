import os


class AppConfig:
    """应用配置"""

    # ip
    ip = '127.0.0.1'
    task = "加拿大刷美签"


    jiankong_relative_excelPath = '../境外美签监控.xlsx'
    jiankong_excelPath = os.path.abspath(jiankong_relative_excelPath)
    yuyue_relative_excelPath = '../境外美签客人.xlsx'
    yuyue_excelPath = os.path.abspath(yuyue_relative_excelPath)

    # 日志配置
    LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    LOG_LEVEL = "INFO"
    LOG_FILE = "./src/consul_booking.log"

    def getUrl(self,From_GuoJia):
        # 目标URL
        Canada = ('渥太华', '多伦多', '温哥华', '卡尔加里', '哈利法克斯', '蒙特利尔', '魁北克城')
        if "英国" in From_GuoJia :
            TARGET_URL = "https://ais.usvisa-info.com/en-gb/niv/users/sign_in"

        elif "加拿大" in From_GuoJia :
            TARGET_URL = "https://ais.usvisa-info.com/en-ca/niv/users/sign_in"

        elif "阿根廷" in From_GuoJia  :
            TARGET_URL = "https://ais.usvisa-info.com/en-ar/niv/users/sign_in"

        elif "智利" in From_GuoJia:
            TARGET_URL = "https://ais.usvisa-info.com/en-cl/niv/users/sign_in"

        elif "巴西" in From_GuoJia:
            TARGET_URL = "https://ais.usvisa-info.com/en-br/niv/users/sign_in"

        elif "阿联酋" in From_GuoJia:
            TARGET_URL = "https://ais.usvisa-info.com/en-ae/niv/users/sign_in"

        elif "玻利维亚" in From_GuoJia:
            TARGET_URL = "https://ais.usvisa-info.com/en-bo/niv/users/sign_in"

        elif "法国" in From_GuoJia:
            TARGET_URL = "https://ais.usvisa-info.com/en-fr/niv/users/sign_in"

        elif "巴巴多斯" in From_GuoJia:
            TARGET_URL = 'https://ais.usvisa-info.com/en-bb/niv/users/sign_in'

        elif "爱尔兰" in From_GuoJia:
            TARGET_URL = 'https://ais.usvisa-info.com/en-ie/niv/users/sign_in'

        elif "墨西哥" in From_GuoJia:
            TARGET_URL = 'https://ais.usvisa-info.com/en-mx/niv/users/sign_in'
        return TARGET_URL

    # 添加新的国家监控的时候需要在这里添加网站，然后在WatchData里面添加匹配的城市和翻译城市名称

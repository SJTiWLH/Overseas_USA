from dataclasses import dataclass
from typing import Dict


class AppConfig:
    """应用配置"""

    # ip
    ip = '127.0.0.1'
    # 目标URL
    TARGET_URL = "https://ais.usvisa-info.com/en-ca/niv/users/sign_in"
    
    # 日志配置
    LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    LOG_LEVEL = "INFO"
    LOG_FILE = "consul_booking.log" 
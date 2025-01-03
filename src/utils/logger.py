import logging
import sys
from src.config import AppConfig

def setup_logger(name: str) -> logging.Logger:
    """设置并返回logger实例"""
    logger = logging.getLogger(name)
    logger.setLevel(logging.getLevelName(AppConfig.LOG_LEVEL))

    # 创建控制台处理器
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(logging.Formatter(AppConfig.LOG_FORMAT))
    logger.addHandler(console_handler)

    # 创建文件处理器
    file_handler = logging.FileHandler(AppConfig.LOG_FILE)
    file_handler.setFormatter(logging.Formatter(AppConfig.LOG_FORMAT))
    logger.addHandler(file_handler)

    return logger
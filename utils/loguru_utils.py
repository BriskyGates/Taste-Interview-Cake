import os

from loguru import logger


class LoguruUtil():
    def __init__(self, log_site, log_name):
        self.log_site = log_site
        self.log_name = log_name

    def loguru_main(self, log_level='INFO'):
        log_abspath = os.path.join(self.log_site, self.log_name)  # 项目根目录下生成log 文件
        logger.add(log_abspath, encoding='utf-8', level=log_level)
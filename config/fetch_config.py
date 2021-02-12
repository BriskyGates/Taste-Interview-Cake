import os
import configparser

from loguru import logger

from utils.loguru_utils import LoguruUtil

from constants import LOG_DIR, CONFIG_DIR


class CategoryConfig():
    LoguruUtil(LOG_DIR, 'category_item.log').loguru_main(log_level='DEBUG')

    def __init__(self, file_path=CONFIG_DIR):
        self.file_path = file_path
        self.config = configparser.ConfigParser()

    @logger.catch
    def read_config(self, section="category"):
        """
        :param section:配置文件的属性
        :return:读取某个section下的数据, 并且以字典形式返回
        """
        self.config.read(self.file_path, encoding='utf-8')
        file_properties = self.config.items(section)
        new_dic = {k: v for k, v in file_properties}
        # logger.info(new_dic)
        return new_dic

    @logger.catch
    def write_configuration(self, section, option):
        """
        :param section: 配置文件的属性
        :param option:  传入配置文件的字典
        :return:  返回传入的数据
        """
        self.config[section] = option
        value = self.config[section] = option
        with open(self.file_path, 'w', encoding='utf-8') as configfile:
            self.config.write(configfile)
        return value


if __name__ == '__main__':
    cc = CategoryConfig('category_item.cfg')
    cc.read_config('category')
    pass
# print(res_dict)
# sc.read_config('DEFAULT')
# sc.write_configuration("wwww", {"ww": "22"})

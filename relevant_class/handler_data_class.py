import os
import re
from decimal import Decimal

import arrow as arrow
from loguru import logger

from constants import LOG_DIR
from utils.loguru_utils import LoguruUtil


class HandleData():
    LoguruUtil(LOG_DIR, 'handler_data_cluster.log').loguru_main()

    @staticmethod
    def check_no_data(*args):
        """
        实现检查arg 多列表中的各个列表是否存在空列表
        :param data_list:
        :return:
        """
        for i in args:
            i = i.strip() if isinstance(i, str) else i
            if not i:  # 检查i 是否为空列表
                return False
        return True

    def replace_list(self, full_list, half_list, data):
        visit_size = len(full_list)
        for index in range(visit_size):
            data = data.replace(full_list[index], half_list[index])
        return data

    @logger.catch
    def keep_decimal_place(self, data, place):
        # 保留小数点后place位
        if not data:
            return ''
        keep_place = '0.0'.ljust(place + 2, '0')  # 原本占了两位
        new_data = Decimal(data).quantize(Decimal(keep_place))
        # logger.info(new_data)
        return new_data  # 将decimal类型转换成str类型

    def fetch_specific_data(self, data: str, pattern):
        data_res = re.findall(pattern, data, flags=re.I)
        if data_res is not None:
            return data_res
        else:
            return []

    def substract_2date(self, date_settle, date_promotion_coupon):
        """
        date1 为结算日期
        :param date_promotion_coupon:
        :param date_settle:
        :return:
        """
        arrow_promotion_coupon = arrow.get(date_promotion_coupon)
        arrow_settle = arrow.get(date_settle)
        arrow_delta = arrow_settle - arrow_promotion_coupon
        if arrow_delta.days <= 0:
            return True
        return False


if __name__ == '__main__':
    hd = HandleData()
    # date1 = '2013.11.11'
    # date2 = '2014.3.2'
    # hd.substract_2date(date1, date2)
    hd.keep_decimal_place(3083.6123, 2)
    # temp = hd.check_no_data(' ')
    # print(temp)
    # ss = ''.replace('，', ",").replace('‘', "'").replace("’", "'").replace('”', '"').replace('“', '"').replace('：', ':')
    #
    # res = hd.strB2Q('，4123')
    # print(res)
    # container_str1 = "箱型箱量： 20GP加重柜 X    12\n运费条款： "
    # container_str1 = "22MT,1X20’GP\n"
    # container_str1 = "20'GP * 12;\n"
    # container_str1 = "2*40GP SA"
    # container_str1 = "1X20GP+1X40HQ ,FRE"  # 主要分成两种
    # pattern = ['\n', '’', "'", '[\u4e00-\u9fa5]', ' ']
    # hd.delete_useless_sub(container_str1, pattern)
    # hd.keep_decimal_place('12.17', 1)

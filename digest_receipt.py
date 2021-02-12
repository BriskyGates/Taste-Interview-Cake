from functools import reduce

from loguru import logger

from config.fetch_config import CategoryConfig
from relevant_class.cash_class import CashReturn
from relevant_class.handler_data_class import HandleData
from constants import *
from utils.loguru_utils import LoguruUtil

LoguruUtil(LOG_DIR, 'digest_receipt.log').loguru_main()


class DigestReceipt():

    def __init__(self, receipt_info):
        self.receipt_info = receipt_info
        self.hd = HandleData()
        self.promotion_info_dict = {}
        self.coupon_info_list = []
        self.purchase_info_dict = {}
        self.settle_date = ""
        self.cr = None

    def fetch_promotion_info(self):
        promotion_info_list = self.hd.fetch_specific_data(self.receipt_info, PATTERN_PROMOTION_INFO)
        for each_data in promotion_info_list:
            category_name = each_data[-1]
            category_discount = each_data[1]
            # promotion_date = each_data[0]
            self.promotion_info_dict[category_name] = {
                # "promotion_date": promotion_date,  # 暂不考虑日期是否失效
                "good_discount": category_discount,
                # 想在这边添加该分类对应的所有商品
            }

    def fetch_coupon_info(self):
        self.coupon_info_list = self.hd.fetch_specific_data(self.receipt_info, PATTERN_COUPON)

    def fetch_settle_date(self):
        settle_date = self.hd.fetch_specific_data(self.receipt_info, PATTERN_SETTLE)
        if settle_date:
            self.settle_date = settle_date[0]

    @logger.catch
    def fetch_purchase_info(self):
        purchase_info_list = self.hd.fetch_specific_data(self.receipt_info, PATTERN_GOODS_ITEM)
        for each_data in purchase_info_list:
            goodname = each_data[1]  # 需要在此处判断数量,单价等等是否为数值型数据
            self.purchase_info_dict[goodname] = {
                "good_num": each_data[0],
                "good_unit_price": each_data[2],
                "good_discount": "1",  # 默认不打折,后期通过fetch_promotion_info 更新
                "good_sum_price": ""  # 加上打折后的价格
            }
        logger.info(f'提取到的商品列表为{self.purchase_info_dict}')

    def calculate_each_price(self):
        # 计算单件商品的价格
        for key, value in self.purchase_info_dict.items():
            good_num = value['good_num']
            good_discount = value['good_discount']
            good_unit_price = value['good_unit_price']
            value['good_sum_price'] = eval(f'{good_num}*{good_discount}*{good_unit_price}')

    @logger.catch
    def calculate_total_price(self):

        total_price_list = [each_data['good_sum_price'] for each_data in self.purchase_info_dict.values()]
        if not total_price_list:
            logger.error('该用户没有购买任何商品')
            return
        total_price = reduce(lambda x, y: x + y, total_price_list)
        # 保留两份小数
        if self.cr is not None:
            total_price = self.cr.accept_cash(total_price)
        total_price_place2 = self.hd.keep_decimal_place(total_price, 2)

        return total_price_place2

    def deal_purchase_promotion(self):
        """
        如何通过电子大类型 定位到用户的
        :return:
        """
        cc = CategoryConfig()
        category_dict = cc.read_config()  # 所有商品的类别字典
        for key, value in self.promotion_info_dict.items():
            for good_name, good_detail in self.purchase_info_dict.items():
                if good_name in category_dict.get(key):
                    good_detail.update(value)
                else:
                    logger.info(f'用户购买的商品{good_name}没有优惠政策')
        logger.info(f'为商品添加完折扣的数据{self.promotion_info_dict}')

    def deal_settle_coupon(self):
        # 先检查优惠券是否过期
        if not self.coupon_info_list:
            logger.info('现在没有任何优惠信息哦 :<')
            return
        coupon_info_tuple = self.coupon_info_list[0]
        coupon_valid_date = coupon_info_tuple[0]
        coupon_money_condition = coupon_info_tuple[1]
        coupon_money_return = coupon_info_tuple[2]
        substract_res = self.hd.substract_2date(self.settle_date, coupon_valid_date)
        if not substract_res:
            logger.info(f'当前优惠券失效,优惠日期为{coupon_valid_date}')
            return
        self.cr = CashReturn(float(coupon_money_condition), float(coupon_money_return))

    def main(self):
        self.fetch_settle_date()
        self.fetch_coupon_info()
        self.fetch_promotion_info()
        self.fetch_purchase_info()
        self.deal_purchase_promotion()
        self.deal_settle_coupon()
        self.calculate_each_price()
        self.calculate_total_price()


if __name__ == '__main__':
    shopping_receipt = """
    2013.11.11 | 0.7 | 电子 //促销信息，格式为：⽇期 | 折扣 | 产品品类，可有多个，每个⼀⾏，如果没有则保留⼀个空⾏

        1 * ipad : 2399.00
1 * 显示器 : 1799.00
12 * 啤酒 : 25.00
5 * ⾯包 : 9.00
2013.11.11
2014.3.2 1000 200
        """
    #     shopping_receipt="""
    #     3 * 蔬菜 : 5.98
    # 8 * 餐⼱纸 : 3.20
    # 2014.01.01
    # """
    dr = DigestReceipt(shopping_receipt)
    dr.main()

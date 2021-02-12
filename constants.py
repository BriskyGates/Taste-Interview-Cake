import os
import re

SHOPPING_PROJECT_DIR = os.path.dirname(__file__)
LOG_DIR = os.path.join(SHOPPING_PROJECT_DIR, 'log')
CONFIG_DIR=os.path.join(SHOPPING_PROJECT_DIR,'config/category_item.cfg')
PATTERN_PURE_DIGIT = re.compile('(\\d*[.,]?\\d*[,.]?\\d+)')  # 提取纯数字正则模式
PATTERN_GOODS_ITEM = '(\\d+) *\\* *([a-z\u2f00-\u2faf\u4e00-\u9fa5]+) *: *(\\d*[.,]?\\d*[,.]?\\d+)'  # 记得re.I
PATTERN_PROMOTION_INFO = '(\\d{4}\\.\\d+\\.\\d+) *\\| *(\\d*[,.]?\\d+) *\\| *([\u2f00-\u2faf\u4e00-\u9fa5]+)'  # 促销
PATTERN_COUPON = '(\\d{4}\\.\\d+\\.\\d+) *(\\d+) *(\\d+)'  # 优惠券
PATTERN_SETTLE = '(\\d{4}\\.\\d+\\.\\d+) *\\n'  # 结算日期
PATTERN_CN_CH = '[\u2f00-\u2faf\u4e00-\u9fa5]'

if __name__ == '__main__':
    pass

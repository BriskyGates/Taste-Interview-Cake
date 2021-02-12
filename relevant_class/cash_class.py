# 现金收费抽象类
class CashSuper:
    def accept_cash(self, money):
        raise NotImplementedError('请不要直接调用现金收费基类哦')


# 正常收费子类
class CashNormal(CashSuper):
    def accept_cash(self, money):
        return money


# 打折收费子类
class CashRebate(CashSuper):
    def __init__(self, money_rebate):
        self.money_rebate = money_rebate

    def accept_cash(self, money):
        return money * self.money_rebate


# 返利收费子类
class CashReturn(CashSuper):
    def __init__(self, money_condition, money_return):
        self.money_condition = money_condition
        self.money_return = money_return

    def accept_cash(self, money):
        if money >= self.money_condition :
            return money - self.money_return
        return money

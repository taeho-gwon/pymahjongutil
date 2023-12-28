from pymahjongutil.enum.common import YakuEnum
from pymahjongutil.rule.default_rule_dict import DefaultRuleDictFactory
from pymahjongutil.schema.yaku_rule import YakuRule


class RiichiMahjongRule:
    def __init__(self, use_open_tanyao: bool = True):
        self.yaku_rule_dict: dict[YakuEnum, YakuRule] = DefaultRuleDictFactory.create()
        self.use_open_tanyao = use_open_tanyao
        if self.use_open_tanyao:
            self.yaku_rule_dict[YakuEnum.ALL_SIMPLES].han_opened = 1

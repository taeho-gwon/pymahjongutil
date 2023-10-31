from pymahjongutil.enum.common import YakuEnum
from pymahjongutil.rule.riichi_default_rule import RiichiDefaultRule
from pymahjongutil.schema.agari_info import AgariInfo
from pymahjongutil.schema.division import Division


class HanCalculator:
    def __init__(self, rule: RiichiDefaultRule | None = None):
        self.rule = rule or RiichiDefaultRule()

    def calculate_han(
        self, division: Division, agari_info: AgariInfo
    ) -> tuple[int, list[YakuEnum]]:
        yakus = self._calculate_yakus(division, agari_info)
        han = sum(
            self.rule.yaku_rule_dict[yaku].get_han(division.is_opened) for yaku in yakus
        )
        return han, yakus

    def _calculate_yakus(
        self, division: Division, agari_info: AgariInfo
    ) -> list[YakuEnum]:
        yakumans = []
        normal_yakus = []
        for yaku, yaku_rule in self.rule.yaku_rule_dict.items():
            if yaku_rule.is_applied(division, agari_info):
                if yaku_rule.is_yakuman:
                    yakumans.append(yaku)
                else:
                    normal_yakus.append(yaku)

        return yakumans or normal_yakus

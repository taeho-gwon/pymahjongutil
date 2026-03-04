from pymahjongutil.enum.common import YakuEnum
from pymahjongutil.rule.riichi_mahjong_rule import RiichiMahjongRule
from pymahjongutil.schema.agari_info import AgariInfo
from pymahjongutil.schema.division import Division


class HanCalculator:
    def __init__(self, rule: RiichiMahjongRule | None = None):
        self.rule = rule or RiichiMahjongRule()

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
        satisfied_yakus: set[YakuEnum] = set()
        for yaku, checker_cls in self.rule.yaku_checker_dict.items():
            if checker_cls().is_satisfied(division, agari_info):
                satisfied_yakus.add(yaku)

        yakumans = []
        normal_yakus = []
        for yaku, yaku_rule in self.rule.yaku_rule_dict.items():
            if yaku not in satisfied_yakus:
                continue
            if yaku_rule.get_han(division.is_opened) == 0:
                continue
            if any(high_yaku in satisfied_yakus for high_yaku in yaku_rule.high_yakus):
                continue
            if yaku_rule.is_yakuman:
                yakumans.append(yaku)
            else:
                normal_yakus.append(yaku)

        return yakumans or normal_yakus

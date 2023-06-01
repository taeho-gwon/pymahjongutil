from pymahjong.enum.common import YakuEnum
from pymahjong.schema.agari_info import AgariInfo
from pymahjong.schema.division import Division
from pymahjong.yaku_checker.base_yaku import BaseYaku


class HanCalculator:
    def __init__(self):
        pass

    def calculate_han(
        self, division: Division, agari_info: AgariInfo
    ) -> tuple[int, list[YakuEnum]]:
        yakus = self._calculate_yakus(division, agari_info)
        han = 0
        return han, yakus

    def _calculate_yakus(
        self, division: Division, agari_info: AgariInfo
    ) -> list[YakuEnum]:
        yakumans: list[YakuEnum] = []
        yakuman_checkers: list[BaseYaku] = []
        for yakuman in yakuman_checkers:
            if yakuman.is_satisfied(division, agari_info):
                yakumans.append(yakuman.yaku)
        if yakumans:
            return yakumans

        normal_yakus: list[YakuEnum] = []
        normal_yaku_checkers: list[BaseYaku] = []
        for normal_yaku in normal_yaku_checkers:
            if normal_yaku.is_satisfied(division, agari_info):
                normal_yakus.append(normal_yaku.yaku)
        return normal_yakus

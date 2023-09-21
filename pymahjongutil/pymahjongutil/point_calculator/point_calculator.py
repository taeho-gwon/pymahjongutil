from math import ceil

from pymahjongutil.hand_checker.riichi_checker import RiichiChecker
from pymahjongutil.point_calculator.fu_calculator import FuCalculator
from pymahjongutil.point_calculator.han_calculator import HanCalculator
from pymahjongutil.rule.riichi_default_rule import RiichiDefaultRule
from pymahjongutil.schema.agari_info import AgariInfo
from pymahjongutil.schema.hand import Hand
from pymahjongutil.schema.point_info import PointInfo
from pymahjongutil.schema.tile import Tiles


class PointCalculator:
    def __init__(self, rule: RiichiDefaultRule | None = None):
        self.rule = rule or RiichiDefaultRule()
        self.fu_calculator = FuCalculator(self.rule)
        self.han_calculator = HanCalculator(self.rule)

    def calculate_base_point(self, fu: int, han: int, is_yakuman: bool = False):
        if han < 3 or (han == 3 and fu < 70) or (han == 4 and fu < 40):
            return fu * pow(2, 2 + han)
        elif han <= 5:
            return 2000
        elif han <= 7:
            return 3000
        elif han <= 10:
            return 4000
        elif han <= 12:
            return 6000
        else:
            return 8000 * (han // 13 if is_yakuman else 1)

    def _calculate_point_diff(self, agari_info: AgariInfo, base_point: int):
        point1 = ceil(base_point / 100) * 100
        point2 = ceil(base_point * 2 / 100) * 100
        point4 = ceil(base_point * 4 / 100) * 100
        point6 = ceil(base_point * 6 / 100) * 100

        player_idx = agari_info.player_wind_idx - Tiles.WINDS[0]
        loser_idx = agari_info.loser_wind_idx - Tiles.WINDS[0]
        point_diff = [0, 0, 0, 0]
        if agari_info.is_tsumo_agari:
            if agari_info.player_wind_idx == Tiles.WINDS[0]:
                point_diff[0] = 3 * point2
                point_diff[1] = -point2
                point_diff[2] = -point2
                point_diff[3] = -point2
            else:
                point_diff[0] = -point2
                point_diff[1] = -point1
                point_diff[2] = -point1
                point_diff[3] = -point1
                point_diff[player_idx] += point1 * 3 + point2
        else:
            point = point6 if agari_info.player_wind_idx == Tiles.WINDS[0] else point4
            point_diff[player_idx] += point
            point_diff[loser_idx] -= point

        return point_diff

    def calculate_point_info(self, hand: Hand, agari_info: AgariInfo) -> PointInfo:
        hand_checker = RiichiChecker(hand)
        max_base_point = -1
        for division in hand_checker.calculate_divisions(agari_info.is_tsumo_agari):
            fu, fu_reasons = self.fu_calculator.calculate_fu(division, agari_info)
            han, yakus = self.han_calculator.calculate_han(division, agari_info)
            fu = fu if fu == 25 else (fu + 9) // 10 * 10
            base_point = self.calculate_base_point(fu, han)

            if base_point > max_base_point:
                max_base_point = base_point
                point_info = PointInfo(
                    point_diff=self._calculate_point_diff(agari_info, base_point),
                    han=han,
                    fu=fu,
                    yakus=yakus,
                    fu_reasons=fu_reasons,
                )

        return point_info

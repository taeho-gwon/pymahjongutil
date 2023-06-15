from pymahjong.point_calculator.fu_calculator import FuCalculator
from pymahjong.point_calculator.han_calculator import HanCalculator
from pymahjong.rule.riichi_default_rule import RiichiDefaultRule


class PointCalculator:
    def __init__(self, rule: RiichiDefaultRule | None):
        self.rule = rule or RiichiDefaultRule()
        self.fu_calculator = FuCalculator(self.rule)
        self.han_calculator = HanCalculator(self.rule)

    @staticmethod
    def calculate_base_point(fu: int, han: int, is_yakuman: bool = False):
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

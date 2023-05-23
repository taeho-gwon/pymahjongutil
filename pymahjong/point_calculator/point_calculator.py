from pymahjong.point_calculator.fu_calculator import FuCalculator
from pymahjong.point_calculator.han_calculator import HanCalculator
from pymahjong.schema.agari_info import AgariInfo
from pymahjong.schema.division import Division


class PointCalculator:
    def __init__(self):
        self.fu_calculator = FuCalculator()
        self.han_calculator = HanCalculator()

    def calculate_base_point(self, division: Division, agari_info: AgariInfo):
        fu, _ = self.fu_calculator.calculate_fu(division, agari_info)
        han, _ = self.han_calculator.calculate_han(division, agari_info)

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
            return 8000 * (han // 13)

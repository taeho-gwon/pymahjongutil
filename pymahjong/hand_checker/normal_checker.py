from mahjong.shanten import Shanten

from pymahjong.hand_checker.hand_checker import HandChecker
from pymahjong.schema.count import HandCount


class NormalChecker(HandChecker):
    def __init__(self):
        self.shanten_calculator = Shanten()

    def calculate_deficiency(self, hand_count: HandCount) -> int:
        return (
            self.shanten_calculator.calculate_shanten_for_regular_hand(
                hand_count.concealed_count.counts
            )
            + 1
        )

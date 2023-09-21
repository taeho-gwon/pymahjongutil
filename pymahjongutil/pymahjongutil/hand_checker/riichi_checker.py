from pymahjongutil.hand_checker.hand_checker import HandChecker
from pymahjongutil.hand_checker.normal_checker import NormalChecker
from pymahjongutil.hand_checker.seven_pair_checker import SevenPairChecker
from pymahjongutil.hand_checker.thirteen_orphan_checker import ThirteenOrphanChecker
from pymahjongutil.schema.division import Division
from pymahjongutil.schema.hand import Hand
from pymahjongutil.schema.tile import Tile


class RiichiChecker(HandChecker):
    def __init__(self, hand: Hand):
        super().__init__(hand)
        self.normal_checker = NormalChecker(hand)
        self.seven_pair_checker = SevenPairChecker(hand)
        self.thirteen_orphan_checker = ThirteenOrphanChecker(hand)

    def calculate_deficiency(self) -> int:
        return min(
            self.normal_checker.calculate_deficiency(),
            self.seven_pair_checker.calculate_deficiency(),
            self.thirteen_orphan_checker.calculate_deficiency(),
        )

    def _calculate_divisions(
        self, agari_tile: Tile, is_tsumo_agari: bool
    ) -> list[Division]:
        return (
            self.normal_checker.calculate_divisions(is_tsumo_agari)
            + self.seven_pair_checker.calculate_divisions(is_tsumo_agari)
            + self.thirteen_orphan_checker.calculate_divisions(is_tsumo_agari)
        )

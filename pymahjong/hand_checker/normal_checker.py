from pymahjong.hand_checker.hand_checker import HandChecker
from pymahjong.schema.division import Division
from pymahjong.schema.tile import Tile


class NormalChecker(HandChecker):
    def calculate_deficiency(self) -> int:
        return (
            self.shanten_calculator.calculate_shanten_for_regular_hand(
                self.hand_count.concealed_count.counts
            )
            + 1
        )

    def _calculate_divisions(
        self, agari_tile: Tile, is_tsumo_agari: bool
    ) -> list[Division]:
        return []

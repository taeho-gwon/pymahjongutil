from mahjong.shanten import Shanten

from pymahjong.hand_checker.hand_checker import HandChecker
from pymahjong.schema.count import HandCount
from pymahjong.schema.division import Division, DivisionPart
from pymahjong.schema.tile import Tile, Tiles


class ThirteenOrphanChecker(HandChecker):
    def __init__(self):
        self.shanten_calculator = Shanten()

    def calculate_deficiency(self, hand_count: HandCount) -> int:
        return (
            self.shanten_calculator.calculate_shanten_for_kokushi_hand(
                hand_count.concealed_count.counts
            )
            + 1
        )

    def _calculate_divisions(
        self, hand_count: HandCount, agari_tile: Tile, is_tsumo_agari: bool
    ) -> list[Division]:
        head = next(
            tile
            for tile in Tiles.TERMINALS_AND_HONORS
            if hand_count.concealed_count[tile] == 2
        )
        return [
            Division(
                parts=DivisionPart.create_thirteen_orphans(head, is_tsumo_agari),
                agari_tile=agari_tile,
            )
        ]

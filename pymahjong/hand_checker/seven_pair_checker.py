from mahjong.shanten import Shanten

from pymahjong.hand_checker.hand_checker import HandChecker
from pymahjong.schema.count import HandCount
from pymahjong.schema.division import Division, DivisionPart
from pymahjong.schema.tile import Tile, Tiles


class SevenPairChecker(HandChecker):
    def __init__(self):
        self.shanten_calculator = Shanten()

    def calculate_deficiency(self, hand_count: HandCount) -> int:
        return (
            self.shanten_calculator.calculate_shanten_for_chiitoitsu_hand(
                hand_count.concealed_count.counts
            )
            + 1
        )

    def _calculate_divisions(
        self, hand_count: HandCount, agari_tile: Tile, is_tsumo_agari: bool
    ) -> list[Division]:
        parts = [DivisionPart.create_head(agari_tile, is_tsumo_agari)]
        for head in Tiles.DEFAULTS:
            head_count = hand_count.concealed_count[head] // 2
            parts.extend([DivisionPart.create_head(head, True)] * head_count)
        return [Division(parts=parts, agari_tile=agari_tile)]

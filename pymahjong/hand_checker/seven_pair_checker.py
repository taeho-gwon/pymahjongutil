from pymahjong.hand_checker.hand_checker import HandChecker
from pymahjong.schema.division import Division, DivisionPart
from pymahjong.schema.tile import Tile, Tiles


class SevenPairChecker(HandChecker):
    def calculate_deficiency(self) -> int:
        return (
            self.shanten_calculator.calculate_shanten_for_chiitoitsu_hand(
                self.hand_count.concealed_count.counts
            )
            + 1
        )

    def _calculate_divisions(
        self, agari_tile: Tile, is_tsumo_agari: bool
    ) -> list[Division]:
        parts = [DivisionPart.create_head(agari_tile, is_tsumo_agari)]
        for head in Tiles.DEFAULTS:
            head_count = self.hand_count.concealed_count[head] // 2
            parts.extend([DivisionPart.create_head(head, True)] * head_count)
        return [Division(parts=parts, agari_tile=agari_tile)]

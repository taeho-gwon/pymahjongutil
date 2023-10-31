from pymahjongutil.hand_checker.hand_checker import HandChecker
from pymahjongutil.schema.division import Division, DivisionPart
from pymahjongutil.schema.tile import Tile, Tiles


class SevenPairChecker(HandChecker):
    def calculate_deficiency(self) -> int:
        if self.hand.is_opened:
            return 100

        tile_counts = self.hand_count.concealed_count.counts
        num_pairs = sum(1 for x in tile_counts if x > 1)
        num_kinds = sum(1 for x in tile_counts if x > 0)
        return 7 - num_pairs + (0 if num_kinds >= 7 else 7 - num_kinds)

    def _calculate_divisions(
        self, agari_tile: Tile, is_tsumo_agari: bool
    ) -> list[Division]:
        parts = [DivisionPart.create_head(agari_tile.value, is_tsumo_agari)]
        for head_idx in Tiles.DEFAULTS:
            head_count = self.hand_count.concealed_count[head_idx] // 2
            if head_idx == agari_tile.value:
                head_count -= 1
            parts.extend([DivisionPart.create_head(head_idx, True)] * head_count)
        return [Division(parts=parts, agari_tile=agari_tile, is_opened=False)]

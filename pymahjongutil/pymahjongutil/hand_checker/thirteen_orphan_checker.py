from pymahjongutil.hand_checker.hand_checker import HandChecker
from pymahjongutil.schema.division import Division, DivisionPart
from pymahjongutil.schema.tile import Tile, Tiles


class ThirteenOrphanChecker(HandChecker):
    def calculate_deficiency(self) -> int:
        if self.hand.is_opened:
            return 100

        tile_counts = self.hand_count.concealed_count.counts
        is_orphan_pair_exist = any(
            tile_counts[x] > 1 for x in Tiles.TERMINALS_AND_HONORS
        )
        num_orphan_kinds = sum(
            1 for x in Tiles.TERMINALS_AND_HONORS if tile_counts[x] > 0
        )
        return 14 - num_orphan_kinds - int(is_orphan_pair_exist)

    def _calculate_divisions(
        self, agari_tile: Tile, is_tsumo_agari: bool
    ) -> list[Division]:
        head_idx = next(
            tile
            for tile in Tiles.TERMINALS_AND_HONORS
            if self.hand_count.concealed_count[tile] == 2
        )
        return [
            Division(
                parts=[DivisionPart.create_thirteen_orphans(head_idx, is_tsumo_agari)],
                agari_tile=agari_tile,
                is_opened=False,
            )
        ]

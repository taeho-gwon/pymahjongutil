from dataclasses import dataclass

from pymahjongutil.schema.tile_index import TileIndex


@dataclass
class EfficiencyData:
    discard_tile: TileIndex
    ukeire: list[TileIndex]
    num_ukeire: int

    def __lt__(self, other: "EfficiencyData") -> bool:
        if self.num_ukeire != other.num_ukeire:
            return self.num_ukeire > other.num_ukeire
        return self.discard_tile < other.discard_tile

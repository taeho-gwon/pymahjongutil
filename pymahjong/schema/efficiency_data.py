from __future__ import annotations

from pydantic import BaseModel

from pymahjong.schema.tile import Tile


class EfficiencyData(BaseModel):
    discard_tile: Tile
    ukeire: list[Tile]
    num_ukeire: int

    def __lt__(self, other: EfficiencyData) -> bool:
        if self.num_ukeire != other.num_ukeire:
            return self.num_ukeire > other.num_ukeire
        return self.discard_tile < other.discard_tile
